# TS — TFW-8: Маппинг данных ППС (преподавателей) для ЕПВО

> **Дата**: 2026-03-18
> **Автор**: Coordinator (AI)
> **Статус**: 🟡 TS — Ожидает апрува
> **Parent HL**: [HL-TFW-8__pps_data_mapping](HL-TFW-8__pps_data_mapping.md)

---

## 1. Цель

Создать исчерпывающий RF-документ `RF_TFW-8__pps_data_mapping.md`, описывающий **все данные**, которые ОВПО должен передавать в ЕПВО по преподавателям (ППС): 9 сущностей, все поля (из OpenAPI + скрытые из чата/инструкций), бизнес-правила маппинга, фильтрацию СУР, и порядок отправки.

## 2. Scope

### In Scope
- Полная матрица маппинга для 9 TUTOR-сущностей + `EMPLOYEE_ORDERS`
- Скрытые поля (не в OpenAPI spec): `tutor.maternity_leave`, `tutor.ftutor`, `tutor.fcountryId`, `tutor_cafedra.type`, `tutor_cafedra.deleted`, `tutor_cafedra.primaryEmploymentId`, `tutor_cafedra.etContractStartDate/FinishDate`, `tutor_cafedra.etByAgreement`
- Бизнес-логика фильтрации ППС для СУР (4 OR-блока)
- SQL-фильтр активных ППС
- Значения справочников: `type` (0/1/2), `primaryEmploymentID` (1/2/3)
- Sequencing Contract (порядок отправки)
- Gotchas из чата (ошибки, удаление TUTOR_CAFEDRA, training directions)
- Анализ PDF-инструкций Адм. отчётов и СУР на предмет ППС

### Out of Scope
- Написание кода интеграции (mapper/ETL)
- Приказы студентов (уже в TFW-5)
- Данные STUDENT/STUDENT_INFO (уже в TFW-4.A)

## 3. Затрагиваемые файлы

| Файл | Действие | Описание |
|------|----------|----------|
| `tasks/TFW-8__pps_data_mapping/RF_TFW-8__pps_data_mapping.md` | CREATE | Итоговый RF — полная спецификация данных ППС |

**Бюджет:** 1 новый файл, 0 модификаций. ✅ В пределах лимита.

## 4. Детальные шаги

### Step 1: Сбор полей — TUTOR (основная карточка)

Составить полную таблицу полей включая:
- OpenAPI spec (из RF_TFW-1.5): `tutorId`, `firstName`, `lastName`, `patronymic`, `birthDate`, `genderId`, `iin`, `nationId`, `sitizenshipId`, `phone`, `email`, `address`, `academicStatusId`, `scientificDegreeId`, `dateOfEmployment`, `dateOfDismissal`, `experience`, `pedagogicalExperience`, `identDocTypeId/Number/Date/OrgId`
- Скрытые поля (чат 2023-H2): `maternity_leave` (bool), `ftutor` (bool), `fcountryId` (int)

Бизнес-правила:
- Правило 1: `sitizenshipId != null` (strict drop)
- Правило 2: `maternity_leave` — для СУР-отчётов
- Правило 3: `ftutor` — для показателя «Иностранные преподаватели» в СУР

### Step 2: Сбор полей — TUTOR_CAFEDRA (привязка к кафедре)

Полная таблица:
- OpenAPI spec: `id`, `tutorId`, `cafedraId`, `positionId`, `rateValue`, `startDate`, `endDate`, `isMainWork`, `isInternalPartTime`
- Скрытые поля (чат): `type` (int: 0=штатный, 1=внутр. совместитель, 2=внешний совместитель), `deleted` (bool), `primaryEmploymentId` (int: 1=ВУЗ отечественный, 2=ВУЗ зарубежный, 3=Организация), `etContractStartDate`, `etContractFinishDate`, `etByAgreement` (bool)

Бизнес-правила:
- Один `tutor` может иметь несколько записей в `TUTOR_CAFEDRA` (разные кафедры/должности)
- Увольнение с кафедры: `deleted = true` (не удалять запись)
- Внешний совместитель из зарубежного ВУЗа: `type=2, primaryEmploymentId=2`

### Step 3: Сбор полей — остальные сущности

- `TUTOR_CAFEDRA_TRAINING_DIRECTIONS`: кардинальность один ко многим (одна tutor_cafedra → несколько directions)
- `TUTOR_POSITIONS`: `isPps` — центральное поле (является ли должность ППС)
- `TUTOR_SUBJECT`: нагрузка (year, term, hours)
- `TUTOR_PUBLICATION`: `pubId`, `tutorId`, `title`, `publicationLevelId`, `publicationTypeId`, `publicationDate`, `doi`
- `TUTOR_QUALIFICATION`: повышение квалификации
- `TUTOR_AWARDS`: награды
- `EMPLOYEE_ORDERS`: `tutorId`, `typeId` (→ `CenterEmployeeOrderType`), `categoryId` (→ `CenterEmployeeOrderCategory`), `date`, `dateOfEmployment`, `fileName`

### Step 4: Бизнес-логика фильтрации ППС для СУР

Документировать 4-блочную OR-конструкцию (источник: Айдар Буранбаев, 30.04.2025):

```
BLOCK 1 (Внешний совместитель из зарубежного ВУЗа):
  tutor_cafedra.type = 2
  AND tutor_cafedra.primaryEmploymentID = 2
  AND tutor_cafedra.deleted IS NOT TRUE
  AND tutor.maternity_leave IS NOT TRUE

BLOCK 2 (Штатный иностранец):
  tutor_cafedra.type = 0
  AND tutor.citizenshipid <> 113
  AND tutor_cafedra.deleted IS NOT TRUE
  AND tutor.maternity_leave IS NOT TRUE

BLOCK 3 (Уволенный, но период работы пересекается с периодом СУР):
  tutor_cafedra.deleted = TRUE
  AND период работы ∩ период сбора данных ≠ ∅

BLOCK 4 (Иностранный преподаватель по признаку ftutor):
  tutor_cafedra.deleted IS NOT TRUE
  AND tutor.maternity_leave IS NOT TRUE
  AND tutor.ftutor = TRUE
```

Также: базовый фильтр активных ППС (чат, 2023-H2): `tc.deleted = false AND tc.type IS NOT NULL AND (maternity_leave = false OR maternity_leave IS NULL)`

### Step 5: Sequencing Contract + JSON-примеры

Определить порядок передачи:
1. `TUTOR_POSITIONS` — справочник должностей
2. `TUTOR` — основная карточка преподавателя
3. `TUTOR_CAFEDRA` — привязка к кафедре (зависит от TUTOR, CAFEDRA, TUTOR_POSITIONS)
4. `TUTOR_CAFEDRA_TRAINING_DIRECTIONS` — направления (зависит от TUTOR_CAFEDRA)
5. `TUTOR_SUBJECT` — нагрузка
6. `TUTOR_PUBLICATION`, `TUTOR_QUALIFICATION`, `TUTOR_AWARDS` — дополнительные данные
7. `EMPLOYEE_ORDERS` — приказы по сотрудникам

Привести JSON-примеры для `TUTOR` и `TUTOR_CAFEDRA` с полным набором скрытых полей.

### Step 6: Gotchas и Observations

На основе чата задокументировать:
- `TUTOR_CAFEDRA` delete может быть временно отключен (Babur Rustauletov, 13.11.2025)
- `TUTOR_CAFEDRA_TRAINING_DIRECTIONS` — 500 ошибка при некорректных `trainingDirectionId`
- `primaryEmploymentID=0` не работает корректно (нужно 1 или 2)
- `ftutor=false/0` + все `f*`-поля не заполнять, если ППС не иностранный
- `ftutor` **не единственный** критерий «иностранности» — ЕПВО дополнительно проверяет `citizenshipid <> 113` у штатных

### Step 7: Анализ PDF-инструкций (Адм. отчёты, СУР)

Изучить:
- `Инструкция_Адм_отчеты_описание_таблиц_011025.pdf` — таблицы ППС
- `Инструкция_Показатели_СУР_описание_таблиц_29092025.pdf` — показатели по иностранным преподавателям

Извлечь дополнительные требования к полям и добавить в RF.

## 5. Acceptance Criteria

- [ ] RF содержит полную матрицу маппинга для 9 сущностей (OpenAPI + скрытые поля)
- [ ] Описана бизнес-логика фильтрации ППС для СУР (все 4 OR-блока)
- [ ] Значения `type`, `primaryEmploymentID` документированы с источниками
- [ ] Sequencing Contract определён
- [ ] JSON-примеры для TUTOR и TUTOR_CAFEDRA содержат все скрытые поля
- [ ] Gotchas из чата (минимум 5) задокументированы со ссылками на источники
- [ ] Данные из PDF-инструкций Адм. отчётов и СУР включены

## 6. Риски фазы

| Риск | Mitigation |
|------|------------|
| PDF-инструкции содержат новые, не найденные в чате, поля | Добавить как «требует верификации» |
| Значения `primaryEmploymentID` изменились (инструкция 2024 vs 2023) | Использовать подтверждённые Бахтияром значения (1=Отечеств., 2=Заруб.) |
| `CenterEmployeeOrderType` — ограниченное число типов | Документировать как limitation |

---

*TS — TFW-8: Маппинг данных ППС для ЕПВО | 2026-03-18*
