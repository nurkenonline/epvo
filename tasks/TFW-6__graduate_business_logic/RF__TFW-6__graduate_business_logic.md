# RF — TFW-6: Бизнес-логика перевода обучающегося в статус «Выпускник»

> **Дата**: 2026-03-15
> **Автор**: Executor (AI)
> **Статус**: 🟢 RF — Ожидает ревью
> **Parent TS**: [TS__TFW-6](TS__TFW-6__graduate_business_logic.md)

---

## 1. Scope

### В scope (degreeId)

| degreeId | Уровень обучения |
|:--------:|------------------|
| 1 | Бакалавриат |
| 2 | Магистратура (научно-педагогическое направление) |
| 3 | Магистратура (профильное) |
| 6 | Докторантура PhD |
| 7 | Докторантура (профильное направление) |

### Вне scope

| degreeId | Причина |
|:--------:|---------|
| 4 | Интернатура — исключена из задачи |
| 5 | Резидентура — исключена из задачи |
| 0, 10 | Подготовительное отделение — не является выпуском |

---

## 2. Матрица «Уровень обучения → Тип приказа»

| degreeId | Уровень | orderType | categoryId | Примечание |
|:--------:|---------|:---------:|:----------:|------------|
| 1 | Бакалавриат | **3** | **1** | Отчисление по выпуску (спец. случай) |
| 2 | Магистратура (НПН) | **28** | **160** | Завершение обучения |
| 3 | Магистратура (профил.) | **28** | **160** | Завершение обучения |
| 6 | Докторантура PhD | **28** | **161** | Завершение обучения |
| 7 | Докторантура (профил.) | **28** | **161** | Завершение обучения |

> ⚠️ **Разрешение противоречия orderType=6 vs 28:**
> В `RF_TFW-4.E` §6.1 указан `orderType=6` для приказа о выпуске — **это ошибка**. `orderType=6` = академический отпуск (подтверждено в `RF_TFW-5` §3.4 и `KNOWLEDGE.md` §2.8).
> Корректные значения:
> - **Бакалавриат** → `orderType=3` (отчисление), `categoryId=1` (завершение обучения). Особый случай: формально это «отчисление», но с categoryId=1, что означает выпуск, а не принудительное отчисление.
> - **Магистратура** → `orderType=28`, `categoryId=160`
> - **Докторантура** → `orderType=28`, `categoryId=161`
>
> **Источник:** `RF_TFW-5` §3.10, `toepvo_dict_ORDER_CATEGORY.json`, `RF_TFW-5` Observation #4.

---

## 3. Pipeline (Sequencing Contract)

Отправка данных при выпуске выполняется **строго последовательно** — 5 шагов. Pipeline единый для всех degreeId.

```
Шаг 1: TRANSCRIPT
         ↓
Шаг 2: ORDERS + ORDER_SECTIONS + SECTION_PERSON + ORDER_STUDENT_INFO
         ↓
Шаг 3: STUDENT update
         ↓
Шаг 4: STUDENT_DIPLOMA_INFO
         ↓
Шаг 5: GRADUATES
```

### Шаг 1: TRANSCRIPT

Все оценки за финальную сессию. ЕПВО использует транскрипты для вычисления GPA.

> ⚠️ Если отправить `STUDENT.status=4` **до** загрузки транскриптов, ЕПВО может отклонить записи транскриптов (Race Condition Risk).

### Шаг 2: Приказ о выпуске (4 сущности)

| Сущность | Ключевые поля | Примечание |
|----------|---------------|------------|
| `ORDERS` | `orderTypeId` = 3 или 28 (см. матрицу), `categoryId`, `orderNumber`, `orderDate` | — |
| `ORDER_SECTIONS` | `orderId` → ORDERS, `sectionNumber`, `categoryId` | — |
| `SECTION_PERSON` | `sectionId`, `personId` = studentId, `movementDate` ✅ | movementDate обязательна |
| `ORDER_STUDENT_INFO` | `sectionId`, `studentId`, `degreeId` | — |

**Связь с GRADUATES:**
```text
GRADUATES.finishOrderNumber == ORDERS.orderNumber
GRADUATES.finishOrderDate == ORDERS.orderDate
```

### Шаг 3: STUDENT update

| Поле | Значение | Обоснование |
|------|----------|-------------|
| `status` | `4` | Выпускник (не `3` — `3` = отчислен) |
| `courseNumber` | `0` | Больше не обучается |

> **О поле `status` vs `isStudent`:** Это одно физическое поле. В ОСМС-контексте `isStudent=3` = любой неактивный. В контексте выпуска `status=4` = конкретно выпускник. Источник: `RF_TFW-4.E` §4.1, `RF_TFW-4.A`.

### Шаг 4: STUDENT_DIPLOMA_INFO

- **typeCode:** `"STUDENT_DIPLOMA_INFO"`
- **Composite Key:** `STUDENT_ID_COMPOSITE_KEY` → `{ type, studentId }`

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `studentId` | int | ✅ | ID обучающегося |
| `diplomaNumber` | string | — | Номер диплома |
| `diplomaSeries` | string | — | Серия диплома |
| `diplomaDate` | date | — | Дата выдачи |
| `registrationNumber` | string | — | Регистрационный номер |
| `honor` | bool | — | Диплом с отличием |
| `iacProtocol` | string | — | Номер протокола ГАК/ГЭК |

**Источник:** `RF_TFW-1.9` §5, `RF_TFW-4.E` §5.

### Шаг 5: GRADUATES

- **typeCode:** `"GRADUATES"`
- **Composite Key:** `GRADUATE_ID_COMPOSITE_KEY` → `{ type, graduateId }`

> Самая «строгая» сущность API: ~20 обязательных (not null) полей.

#### Полная таблица полей GRADUATES

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `typeCode` | string | ✅ | Всегда `"GRADUATES"` |
| `universityId` | int | ✅ | ID вуза |
| `graduateId` | int | ✅ | Код выпускника (= `studentId`) |
| `studentId` | int | — | Связь с профилем STUDENT |
| `firstName` | string | ✅ | Имя |
| `lastName` | string | — | Фамилия |
| `patronymic` | string | — | Отчество |
| `birthDate` | date | ✅ | Дата рождения (ISO 8601) |
| `sexId` | int | ✅ | Пол (→ `Sex`) |
| `iin` | string | ⚠️ | ИИН (условно обяз., см. Правило 2) |
| `nationId` | int | ✅ | Национальность (→ `CenterNationality`) |
| `sitizenshipId` | int | ✅ | Гражданство (→ `CenterCountry`) |
| `professionId` | int | ⚠️ | ГОП (условно, см. Правило 3) |
| `studyFormId` | int | — | Форма обучения |
| `paymentFormId` | int | ✅ | Форма оплаты |
| `studyLanguageId` | int | ✅ | Язык обучения |
| `degreeId` | int | ✅ | Академическая степень (≠ 0, ≠ 10) |
| `startDate` | date | ✅ | Дата зачисления |
| `startOrderNumber` | string | ✅ | Номер приказа о зачислении |
| `finishOrderNumber` | string | ✅ | Номер приказа о выпуске |
| `finishOrderDate` | date | ✅ | Дата приказа о выпуске |
| `iacDiplomaNumber` | string | ✅ | Номер диплома |
| `iacDiplomaSeries` | string | ✅ | Серия диплома |
| `diplomaDate` | date | — | Дата выдачи диплома |
| `registrationNumber` | string | — | Регистрационный номер диплома |
| `diplomaHonor` | bool | — | Диплом с отличием |
| `gpa` | double | ⚠️ | GPA (условно обяз., см. Правило 1) |
| `centerProfChecked` | bool | ✅ | Проверка центр. справочника ГОП |
| `enrollYear` | int | — | Год поступления |
| `graduationYear` | int | — | Год выпуска |
| `specializationId` | int | ⚠️ | ОП (условно обяз., см. Правило 6) |
| `hasJobId` | int | — | Тип занятости после выпуска |
| `jobPlaceTypeId` | int | — | Тип организации трудоустройства |
| `organizationFormId` | int | — | Вид организации |
| `reasonEmploymentId` | int | — | Причина (не)трудоустройства |
| `placeOfFurtherEducationId` | int | — | Место дальнейшего обучения |

**FK-зависимости:** `Sex`, `CenterNationality`, `CenterCountry`, `Profession`, `StudyForms`, `PaymentForms`, `CenterStudyLanguages`, `DegreeTypes`, `HasJobs`, `JobPlaceType`, `OrganizationForms`, `DicReasonEmployment`, `PlaceOfFurtherEducation`, `Specializations`, `Student`

**Источник:** `RF_TFW-1.9` §1, `RF_TFW-4.E` §3.

---

## 4. Условные поля GRADUATES по degreeId

### degreeId 1, 2, 3 — Стандартный набор

Все поля из таблицы в §3 (Шаг 5). Дополнительных полей нет.

### degreeId 6, 7 — Докторантура

Дополнительно обязательны:

| Поле | Тип | Условие | Описание |
|------|-----|---------|----------|
| `doctorDefended` | bool | Всегда для degreeId 6,7 | Защитил ли диссертацию |
| `defenseOfDissertationInOtherHpeo` | bool | Если защита в другом вузе | `true` = защита в другом вузе |
| `defenseOfDissertationOtherHpeoId` | int | Если `defenseOfDissertationInOtherHpeo=true` | ID вуза, где защищался |
| `dateDissertationDefense` | date | Если `defenseOfDissertationInOtherHpeo=true` | Дата защиты |

```text
IF degreeId IN (6, 7):
    GRADUATES.doctorDefended = local.doctor_defended
    IF local.defenseInOtherHpeo == true:
        GRADUATES.defenseOfDissertationInOtherHpeo = true
        GRADUATES.defenseOfDissertationOtherHpeoId = local.otherHpeoId  // MANDATORY
        GRADUATES.dateDissertationDefense = local.defenseDate
```

**Источник:** `RF_TFW-4.E` §3.2, Правило 7.

---

## 5. Три точки ввода дипломных данных

Серия и номер диплома отправляются в **три** сущности:

| Сущность | Поля диплома | Обязательность |
|----------|-------------|:--------------:|
| `GRADUATES` | `iacDiplomaSeries`, `iacDiplomaNumber`, `diplomaDate` | ✅ not null |
| `STUDENT_DIPLOMA_INFO` | `diplomaSeries`, `diplomaNumber`, `diplomaDate` | — |
| `STUDENT_INFO` | `diplomaSeries`, `diplomaNumber`, `diplomaDate` | — |

### Правило согласованности

```text
GRADUATES.iacDiplomaSeries == STUDENT_DIPLOMA_INFO.diplomaSeries == STUDENT_INFO.diplomaSeries
GRADUATES.iacDiplomaNumber == STUDENT_DIPLOMA_INFO.diplomaNumber == STUDENT_INFO.diplomaNumber
GRADUATES.diplomaDate == STUDENT_DIPLOMA_INFO.diplomaDate == STUDENT_INFO.diplomaDate
GRADUATES.diplomaHonor == STUDENT_DIPLOMA_INFO.honor
```

> ⚠️ **Рассогласование** между тремя сущностями вызовет конфликт при проверке дипломов на `https://epvo.kz/#/verification_education_document`. Источник данных должен быть **единым**. (TD-PHASE-E-2 из REVIEW PhaseE)

---

## 6. Бизнес-правила

### Правило 1: GPA (условная обязательность)

```text
IF enrollYear >= 2010:
    GRADUATES.gpa = MANDATORY (double, >= 0.0)
    IF gpa IS NULL:
        LOG_ERROR("GPA обязателен для поступивших с 2010 г.")
        DROP_RECORD()
ELSE:
    GRADUATES.gpa = OPTIONAL
```

### Правило 2: ИИН выпускника

```text
IF citizenshipId == 113 (Казахстан):
    GRADUATES.iin = MANDATORY (12 цифр, валидация 7-го разряда)
ELSE IF icType == "Вид на жительство":
    GRADUATES.iin = MANDATORY
ELSE:
    GRADUATES.iin = OPTIONAL
```

Для граждан РК с нестандартным ИИН: в `GRADUATES` передать `iin_gived_by_government = true`. Источник: `KNOWLEDGE.md` §2.7.

### Правило 3: ГОП vs CenterProfessionCode

```text
IF centerProfChecked == true:
    GRADUATES.professionId = NULL
    GRADUATES.centerProfessionCode = local.centerProfCode
ELSE:
    GRADUATES.professionId = local.professionId
    GRADUATES.centerProfessionCode = NULL
```

Поля **взаимоисключающие**. Источник: `RF_TFW-4.E` §3.2, Правило 2.

### Правило 4: Фильтрация (кто попадает в GRADUATES)

```text
IF student.status == 4
   AND student.courseNumber == 0
   AND degreeId NOT IN (0, 10)
   AND iacDiplomaNumber IS NOT EMPTY:
    SEND_TO_EPVO()
ELSE:
    SKIP()
```

### Правило 5: Серия/номер диплома (Strict Clean)

```text
IF iacDiplomaSeries IS EMPTY OR iacDiplomaNumber IS EMPTY:
    LOG_ERROR("Диплом не заполнен, запись пропущена")
    DROP_RECORD()
```

Если ВУЗ хранит серию и номер в одном поле (например, `"ЖБ-Б 0123456"`):
```text
series, number = SPLIT(raw, " ", maxsplit=1)
GRADUATES.iacDiplomaSeries = TRIM(series)
GRADUATES.iacDiplomaNumber = TRIM(REPLACE(number, "№", ""))
```

### Правило 6: ОП (specializationId)

```text
IF profession.classifier == 2:  // ГОП (группа)
    GRADUATES.specializationId = MANDATORY
ELSE:
    GRADUATES.specializationId = OPTIONAL
```

---

## 7. Побочные эффекты на STUDENT при выпуске

| orderType | status | courseNumber | Другие поля |
|:---------:|:------:|:-----------:|-------------|
| 3 cat=1 (бакалавриат) | → 4 | → 0 | — |
| 28 cat=160 (магистратура) | → 4 | → 0 | + `GRADUATES`, `STUDENT_DIPLOMA_INFO` |
| 28 cat=161 (докторантура) | → 4 | → 0 | + `GRADUATES`, `STUDENT_DIPLOMA_INFO`, поля diссертации |

> ⚠️ Нельзя: отправить приказ о выпуске, оставив `status=1`. Источник: `KNOWLEDGE.md` §2.6.

---

## 8. Нострификация (для выпускников с зарубежным предыдущим образованием)

```text
IF educational_institution == "Зарубежное ОУ":
    GRADUATES.nostrificationCertificateDate = MANDATORY
    GRADUATES.nostrificationCertificateNumber = MANDATORY
ELSE:
    // поля = null
```

Источник: `RF_TFW-4.E` §8.

---

## 9. Дубликаты дипломов (DIPLOMA_DUPLICATES)

- **typeCode:** `"DIPLOMA_DUPLICATES"`
- **Composite Key:** `DIPLOMA_DUPLICATE_ID_COMPOSITE_KEY`

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `diplomaDuplicateId` | int | ✅ | Уникальный ID записи |
| `graduateId` | int | — | ID выпускника |
| `studentId` | int | — | ID обучающегося |
| `seriesNumber` | string | — | Серия и номер дубликата |
| `registrationNumber` | string | — | Регистрационный номер |
| `issueDate` | date | — | Дата выдачи |

```text
IF diplom_duplicate_given == true:
    DIPLOMA_DUPLICATES.seriesNumber = MANDATORY
    DIPLOMA_DUPLICATES.registrationNumber = MANDATORY
    DIPLOMA_DUPLICATES.issueDate = MANDATORY
```

Источник: `RF_TFW-4.E` §9, `RF_TFW-1.9` §2.

---

## 10. Сводка источников

| Раздел RF | Основной источник | Дополнительный |
|-----------|-------------------|----------------|
| §2 Матрица | `RF_TFW-5` §3.10, `toepvo_dict_ORDER_CATEGORY.json` | `RF_TFW-5` Observation #4 |
| §3 Pipeline | `RF_TFW-4.E` §2 (Sequencing Contract) | `KNOWLEDGE.md` §2.11 |
| §3 Поля GRADUATES | `RF_TFW-1.9` §1 (OpenAPI) | `RF_TFW-4.E` §3.1 (маппинг) |
| §4 Условные поля | `RF_TFW-4.E` §3.2, Правила 7-8 | — |
| §5 Три точки ввода | `KNOWLEDGE.md` §2.12 | `REVIEW__PhaseE` TD-PHASE-E-2 |
| §6 Бизнес-правила | `RF_TFW-4.E` §3.2, Правила 1-6 | `KNOWLEDGE.md` §2.7 |
| §7 Побочные эффекты | `RF_TFW-5` §4 (таблица) | `KNOWLEDGE.md` §2.6 |

---

## 11. Observations (out-of-scope, not modified)

| # | File | Type | Description |
|---|------|------|-------------|
| 1 | `RF_TFW-4.E` §6.1 | inconsistency | `orderType=6` для приказа о выпуске — ошибка. Зафиксировано в `RF_TFW-5` Observation #4, но не исправлено в самом `RF_TFW-4.E`. Рекомендуется обновить §6.1, заменив `6` на `28` (маг./докт.) / `3 cat=1` (бак.) |
| 2 | `RF_TFW-4.E` §4.1 | inconsistency | Указано `isStudent=3` для ОСМС, но не упомянуто, что `status=4` — отдельное значение для выпускников в контексте GRADUATES. Рекомендуется добавить явное указание |
| 3 | `KNOWLEDGE.md` §2.11 | improvement | Sequencing Contract упоминает `orderType=6` (из RF_TFW-4.E). Рекомендуется обновить на корректные значения (type=3 cat=1 / type=28) |
| 4 | `RF_TFW-5` §3.10 | observation | Для бакалавриата используется `orderType=3 cat=1`, что семантически конфликтует с другими categoryId отчисления (cat=2-9 — принудительное). Рекомендуется добавить явное примечание в RF_TFW-5 |

---

*RF — TFW-6: Бизнес-логика перевода обучающегося в статус «Выпускник» | 2026-03-15*
