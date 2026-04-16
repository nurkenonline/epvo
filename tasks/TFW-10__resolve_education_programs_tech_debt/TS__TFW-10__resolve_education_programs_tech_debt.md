# TS — TFW-10: Разрешение технического долга по Реестру ОП

> **Дата**: 2026-04-15
> **Автор**: Coordinator (AI)
> **Статус**: 🟡 TS — Ожидает апрува
> **Parent HL**: [HL-TFW-10__resolve_education_programs_tech_debt](HL-TFW-10__resolve_education_programs_tech_debt.md)

---

## 1. Цель
Реализовать исправления в существующих артефактах базы знаний и каталогов спецификаций в соответствии с планом TFW-10 для закрытия накопившегося техдолга (TD-21 — TD-25). 

## 2. Scope

| Долг | Затрагиваемый Файл | Что сделать |
|------|--------------------|-------------|
| **TD-21** | `tasks/TFW-1__entity_catalog/RF_TFW-1.2__education_programs.md` §2 (SPECIALIZATIONS) | Добавить в таблицу полей SPECIALIZATIONS недостающие 20+ полей из `adm_doc` (statusep, eduprogtype, is_interdisciplinary, joint/partner поля, trainingformatid, ignore_rms и др.). Добавить пометку о том, что OpenAPI spec является неполным. Указать ссылку: `*(Обновлено в рамках TFW-10: TD-21)*`. |
| **TD-22** | `tasks/TFW-1__entity_catalog/RF_TFW-1.2__education_programs.md` §2 и Граф | Исправить `professionId` (описание: "ГОП (→ Profession)") на `prof_caf_id`. Обновить Mermaid-граф для правильной визуализации моста `SPECIALIZATIONS --> PROFESSION_CAFEDRA`. Указать ссылку: `*(Исправлено: TD-22)*`. |
| **TD-23** | `tasks/TFW-4__gap_decomposition/RF_TFW-4.B__admissions_registries.md` §3.1, §3.2 | Добавить Alert-блок `> [!WARNING]` под таблицей маппинга и над правилом 2: описать проблему с расхождением юнитов. В `EducationProgram/SPECIALIZATIONS` API принимает `duration` в месяцах, а в `PROFESSION` используется `studyPeriod` в семестрах. Указать ссылку: `*(TD-23)*`. |
| **TD-25** | `tasks/TFW-4__gap_decomposition/RF_TFW-4.B__admissions_registries.md` §3 | В заголовок §3 и текст добавить уточнение: `*(В API ЕПВО фактический typeCode = "SPECIALIZATIONS")*` для устранения неоднозначности терминологии. |
| **TD-24** | `KNOWLEDGE.md` | Создать новую секцию `## 2.3 Реестр образовательных программ`. Включить базовые архитектурные правила: `classifier` (ГОП/специальность), мостовая связь (`prof_caf_id`), отключение ОП от СУР (`ignore_rms`) и статус ОП `statusep`. |
| N/A | `TECH_DEBT.md` | Изменить статус TD-21 — TD-25 на `✅ Resolved (TFW-10)`. |

### Out of Scope
- Не производить полный рерайт старых файлов, только точечные вставки/патчи. 
- Не писать код интеграции.

## 3. Затрагиваемые файлы

| Файл | Действие | Описание |
|------|----------|----------|
| `tasks/TFW-1__entity_catalog/RF_TFW-1.2__education_programs.md` | MODIFY | Патч таблицы SPECIALIZATIONS и графа. |
| `tasks/TFW-4__gap_decomposition/RF_TFW-4.B__admissions_registries.md` | MODIFY | Добавление аннотаций в секцию §3. |
| `KNOWLEDGE.md` | MODIFY | Создание секции §2.3. |
| `TECH_DEBT.md` | MODIFY | Смена статусов 5 позиций. |
| `RF__TFW-10__resolve_education_programs_tech_debt.md` | CREATE | Пустой RF-отчет, подтверждающий изменения. |

**Бюджет файлов:** 4 файла модифицированы, 1 новый.

## 4. Детальные шаги для Executor'a

### 1️⃣ Патч `RF_TFW-1.2` (TD-21, TD-22)
1. В секции `## 2. SPECIALIZATIONS` модифицировать матрицу полей. Текущие ~10 полей дополнить полями, взятыми из `RF_TFW-9` для полноты.
2. Там же: строку `professionId` удалить. Добавить: `prof_caf_id | int32 | | ID мостовой связи (→ PROFESSION_CAFEDRA)`. Сделать примечание: `⚠️ OpenAPI v3 ошибочно документирует прямую fk professionId. Фактически требуется prof_caf_id.` *(TD-22)*.
3. В `Граф зависимостей группы` внизу файла обновить стрелки: `SPECIALIZATIONS --> PROFESSION_CAFEDRA` и удалить прямое `SPECIALIZATIONS --> PROFESSION` если оно там есть. Сделать пометку об обновлении.

### 2️⃣ Аннотирование `RF_TFW-4.B` (TD-23, TD-25)
1. Изменить заголовок `## 3. Сущность: EducationProgram (Образовательная программа)` добавив рядом `(typeCode: SPECIALIZATIONS)`. Добавить комментарий после заголовка *(TD-25)*.
2. В секции `3.2. Бизнес-правила` добавить блок:
```markdown
> [!WARNING]
> **Семантический конфликт (TD-23)**:
> В `EducationProgram` (`SPECIALIZATIONS`) сроком обучения является поле `duration`, которое следует передавать в **месяцах**. В сущности `PROFESSION` (ГОП) есть поле `studyPeriod`, которое измеряется исключительно в **семестрах**. Будьте осторожны при маппинге.
```

### 3️⃣ Обновление `KNOWLEDGE.md` (TD-24)
Добавить следующую секцию (в блок `2. Архитектурные решения`):
```markdown
## 2.3 Реестр образовательных программ (TFW-9, TFW-10)

Система ЕПВО различает Группы образовательных программ (ГОП) и сами ОП.
*   **Два типа ГОП**: В одной таблице `PROFESSION` лежат и старые специальности (`classifier=1`) и новые ГОП (`classifier=2`).
*   **Иерархия (JOIN-путь)**: ОП (`SPECIALIZATIONS`) не ссылается напрямую на ГОП. Она привязана к мостовой таблице `PROFESSION_CAFEDRA` через `prof_caf_id`. 
    Логическая связь: `SPECIALIZATIONS.prof_caf_id → PROFESSION_CAFEDRA.id → PROFESSION.professionid`.
*   **Статусы Реестра**: Отправка по API `statusep=1` НЕ включает физически ОП в реестр. Требуется официальная заявка через [enic-kazakhstan.edu.kz](https://enic-kazakhstan.edu.kz/ru/reestr-op/ovpo-1).
*   **Скрытие из расчетов (СУР)**: Управление параметрами устойчивого развития (рейтингами) осуществляется флагом `ignore_rms`.
*   **Правило Full Replace**: При обновлении `PROFESSION` или `SPECIALIZATIONS` через `/org-data/list/save` необходимо передавать ВСЕ поля объекта, иначе пропущенные поля будут сброшены в `null`.
```

### 4️⃣ Разрешение `TECH_DEBT.md`
Найти строки TD-21, TD-22, TD-23, TD-24, TD-25 в колонке `Action` (или `Status` если он так называется в строке) заменить `→ backlog` (или `⬜ Backlog`) на `✅ Resolved (TFW-10)`.

## 5. Acceptance Criteria

- [ ] В `RF_TFW-1.2` секция `SPECIALIZATIONS` имеет 30+ полей, а граф учитывает `PROFESSION_CAFEDRA`. Добавлена отметка об обновлении (TD-21, TD-22).
- [ ] В `RF_TFW-4.B` присутствуют предупреждения о единицах измерения (duration vs studyPeriod) и typeCode `SPECIALIZATIONS` (TD-23, TD-25).
- [ ] В `KNOWLEDGE.md` появился новый подпункт §2.3, кратко описывающий логику ОП (TD-24).
- [ ] Статусы 5 пунктов долга в `TECH_DEBT.md` изменены на `✅ Resolved (TFW-10)`.
- [ ] Написан `RF__TFW-10__resolve_education_programs_tech_debt.md` со списком измененных файлов и ссылками на закрытые TD.

## 6. Риски
- Mermaid-граф в `RF_TFW-1.2` может содержать другие узлы. Редактировать нужно аккуратно, чтобы не сломать рендер графа по Markdown.

---
*TS — TFW-10: Разрешение технического долга по Реестру ОП | 2026-04-15*
