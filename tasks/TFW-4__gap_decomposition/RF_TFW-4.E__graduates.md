# RF_TFW-4.E — Выпускники (Рейтинги и Дипломы)

> **Дата**: 2026-03-13
> **Связанная задача**: TFW-4 Phase E
> **Статус**: 🟢 RF — Ожидает ревью координатора

---

## 1. Сводка

Заключительная фаза декомпозиции GAP Analysis. Документ описывает бизнес-логику перевода обучающегося в статус «Выпускник», заполнения данных о дипломе и формирования отчётных данных для СУР (общежития). Охватывает три целевые сущности ЕПВО:

1. **`GRADUATES`** — полный профиль выпускника (отдельная сущность, не `STUDENT`).
2. **`STUDENT` (update)** — обновление статуса действующего студента → выпускник.
3. **`STUDENT_DIPLOMA_INFO`** — дипломная информация, привязанная к профилю студента.

Дополнительно: описан маппинг сущности **`DORMITORY`** для отчётов СУР по обеспеченности общежитиями.

---

## 2. Жёсткий порядок отправки (Sequencing Contract)

> **⚠️ Race Condition Risk:** Если отправить данные не в том порядке, ЕПВО может отклонить запрос, т.к. статус студента не будет соответствовать ожидаемому.

Отправка данных при выпуске должна выполняться строго последовательно:

```
Шаг 1: TRANSCRIPT (все оценки за финальную сессию)
           ↓
Шаг 2: ORDERS + ORDER_SECTIONS + SECTION_PERSON + ORDER_STUDENT_INFO
        (приказ типа 6 — «Завершение обучения»)
           ↓
Шаг 3: STUDENT update (status = 4, courseNumber = 0)
           ↓
Шаг 4: STUDENT_DIPLOMA_INFO (серия, номер, дата диплома)
           ↓
Шаг 5: GRADUATES (полный профиль выпускника)
```

**Обоснование:** Шаг 1 обязателен перед выпуском — ЕПВО использует транскрипты для вычисления GPA. Приказ (шаг 2) должен быть зарегистрирован до смены статуса студента, иначе возникает orphan-запись. `GRADUATES` отправляется последним, т.к. эта сущность ссылается на `studentId` и ожидает, что студент уже в статусе «Выпускник».

---

## 3. Сущность: GRADUATES (Профиль выпускника)

- **Endpoint:** `/org-data/list/save`
- **typeCode:** `"GRADUATES"`
- **Composite Key:** `GRADUATE_ID_COMPOSITE_KEY` → `{ type, graduateId }`

> Это самая «строгая» сущность в API: ~20 обязательных полей (not null).

### 3.1 Матрица маппинга

| EPVO Field | Type | Req | Logic / Source |
|------------|------|-----|----------------|
| `typeCode` | Str | ✅ | Всегда `"GRADUATES"` |
| `universityId` | Int | ✅ | Системная константа ВУЗа |
| `graduateId` | Int | ✅ | `local.student.id` (совпадает с `studentId` до выпуска) |
| `studentId` | Int | — | `local.student.id` (связь с профилем STUDENT) |
| `firstName` | Str | ✅ | `local.student.firstName` |
| `lastName` | Str | — | `local.student.lastName` |
| `patronymic` | Str | — | `local.student.patronymic` |
| `birthDate` | Date | ✅ | `local.student.birthDate` (ISO 8601) |
| `sexId` | Int | ✅ | `local.student.genderId` |
| `iin` | Str | ⚠️ | `local.student.iinPlt` (см. Правило 1) |
| `nationId` | Int | ✅ | `local.student.nationId` |
| `sitizenshipId` | Int | ✅ | `local.student.sitizenshipId` |
| `professionId` | Int | ⚠️ | `local.student.professionId` (см. Правило 2) |
| `studyFormId` | Int | — | `local.student.studyFormId` |
| `paymentFormId` | Int | ✅ | `local.student.paymentFormId` |
| `studyLanguageId` | Int | ✅ | `local.student.studyLanguageId` |
| `degreeId` | Int | ✅ | `local.student.degreeId` (≠ 0, ≠ 10) |
| `startDate` | Date | ✅ | `local.student.enrollDate` |
| `startOrderNumber` | Str | ✅ | Номер приказа о зачислении из локальной БД |
| `finishOrderNumber` | Str | ✅ | Номер приказа о выпуске (Order Type 6) |
| `finishOrderDate` | Date | ✅ | Дата приказа о выпуске |
| `iacDiplomaNumber` | Str | ✅ | Номер диплома (см. Правило 3) |
| `iacDiplomaSeries` | Str | ✅ | Серия диплома (см. Правило 3) |
| `diplomaDate` | Date | — | Дата выдачи диплома |
| `registrationNumber` | Str | — | Регистрационный номер диплома |
| `diplomaHonor` | Bool | — | Диплом с отличием |
| `gpa` | Dbl | ⚠️ | GPA выпускника (см. Правило 4) |
| `centerProfChecked` | Bool | ✅ | `local.student.centerProfChecked` |
| `enrollYear` | Int | — | Год поступления |
| `graduationYear` | Int | — | Год выпуска (из даты приказа) |
| `specializationId` | Int | ⚠️ | ОП (см. Правило 5) |
| `hasJobId` | Int | — | Тип занятости после выпуска |
| `jobPlaceTypeId` | Int | — | Тип организации трудоустройства |
| `organizationFormId` | Int | — | Вид организации |
| `reasonEmploymentId` | Int | — | Причина (не)трудоустройства |

### 3.2 Бизнес-правила

**Правило 1 (ИИН выпускника):**
```text
IF local.sitizenshipId == 113 (Казахстан):
    EPVO.iin = MANDATORY (12 цифр, валидация 7-го разряда)
ELSE IF local.icType == "Вид на жительство":
    EPVO.iin = MANDATORY
ELSE:
    EPVO.iin = OPTIONAL
```

**Правило 2 (ГОП vs CenterProfessionCode):**
```text
// Взаимоисключающие поля
IF centerProfChecked == true:
    EPVO.professionId = NULL
    EPVO.centerProfessionCode = local.centerProfCode  // Код из центр. справочника
ELSE:
    EPVO.professionId = local.professionId  // ID из локального справочника
    EPVO.centerProfessionCode = NULL
```
*Обоснование: adm_doc — «professionid предназначено к заполнению, если centerprofessioncode не заполнено», и наоборот.*

**Правило 3 (Серия и номер диплома — Strict Clean):**
```text
// iacDiplomaSeries и iacDiplomaNumber — обязательные (not null)
// Если ВУЗ хранит в одном поле ("ЖБ-Б 0123456"):
series, number = SPLIT(local.diplomaRaw, " ", maxsplit=1)
EPVO.iacDiplomaSeries = TRIM(series)
EPVO.iacDiplomaNumber = TRIM(REPLACE(number, "№", ""))

// Если хранит раздельно:
EPVO.iacDiplomaSeries = TRIM(local.diplomaSeries)
EPVO.iacDiplomaNumber = TRIM(local.diplomaNumber)

// Fallback: если пустые — запись НЕ отправляется (DROP_RECORD)
IF EPVO.iacDiplomaSeries IS EMPTY OR EPVO.iacDiplomaNumber IS EMPTY:
    LOG_ERROR("Диплом не заполнен, запись пропущена")
    DROP_RECORD()
```

**Правило 4 (GPA — условная обязательность):**
```text
IF local.enrollYear >= 2010:
    EPVO.gpa = MANDATORY (double, >= 0.0)
    IF local.gpa IS NULL:
        LOG_ERROR("GPA обязателен для поступивших с 2010 г.")
        DROP_RECORD()
ELSE:
    EPVO.gpa = OPTIONAL
```

**Правило 5 (ОП — условная обязательность):**
```text
IF local.profession.classifier == 2  // ГОП (группа)
    EPVO.specializationId = MANDATORY
    // Если у студента нет привязки к ОП внутри ГОП, это ошибка данных
ELSE:
    EPVO.specializationId = OPTIONAL
```

**Правило 6 (Фильтрация выпускников — Scope):**
```text
// Выпускник попадает в GRADUATES только при выполнении ВСЕХ условий:
IF local.student.status == 4          // Выпускник
   AND local.student.courseNumber == 0
   AND local.degreeId NOT IN (0, 10)  // Не подготовительное отделение
   AND local.iacDiplomaNumber IS NOT EMPTY:
    SEND_TO_EPVO()
ELSE:
    SKIP()
```

**Правило 7 (Докторантура — дополнительные поля):**
```text
IF local.degreeId IN (6, 7):  // Докторантура PhD, Докторантура по направлениям
    EPVO.doctorDefended = local.doctor_defended  // Защитил ли диссертацию
    IF local.defenseInOtherHpeo == true:
        EPVO.defenseOfDissertationInOtherHpeo = true
        EPVO.defenseOfDissertationOtherHpeoId = local.otherHpeoId  // MANDATORY
        EPVO.dateDissertationDefense = local.defenseDate
ELSE:
    // Поля докторантуры = null
```

**Правило 8 (Интернатура — свидетельство):**
```text
IF local.degreeId == 4:  // Интернатура
    EPVO.internIacDiplomaSeries = local.internDiplomaSeries  // MANDATORY
    EPVO.internIacDiplomaNumber = local.internDiplomaNumber
    EPVO.internProtocolNumber = local.internProtocolNumber
    EPVO.internProtocolDate = local.internProtocolDate
    EPVO.internRegistrationNumber = local.internRegNumber
    EPVO.internDateOfIssue = local.internIssueDate
    EPVO.internHonoursDiploma = local.internHonors
```

---

## 4. Обновление STUDENT при выпуске

- **Endpoint:** `/org-data/list/save`
- **typeCode:** `"STUDENT"`

При выпуске студента его существующий профиль обновляется:

| EPVO Field | Update Value | Обоснование |
|------------|-------------|-------------|
| `status` | `4` | Выпускник (не `3` — у `3` значение «Отчислен» в контексте ОСМС; `4` — Выпускник по OpenAPI spec) |
| `courseNumber` | `0` | Нулевой курс = больше не обучается |

### 4.1 Правило (Разграничение «Отчислен» vs «Выпускник»)

```text
// В STUDENT.status:
// 1 = Обучается
// 2 = Абитуриент
// 3 = Отчислен (без диплома, принудительно)
// 4 = Выпускник (с дипломом, завершение обучения)

// В RF_TFW-4.A поле называлось isStudent, а в OpenAPI — status.
// Уточнение: отправляется ОДНО и ТО ЖЕ поле, но:
//   - isStudent=3 используется для ОСМС (любой «неактивный»)
//   - status=4 — конкретно выпускник в GRADUATES context

// Для выпускника:
EPVO.STUDENT.status = 4
EPVO.STUDENT.courseNumber = 0
```

> **Примечание:** В Phase A (`RF_TFW-4.A`) это поле передавалось как `isStudent` со значениями `1/3`. Значение `4` (выпускник) — дополнительная семантика из OpenAPI спецификации (`RF_TFW-1.3`, строка 34). Интегратор должен убедиться, что для ОСМС-отчёта используется `isStudent=3` (любой неактивный), а для выпускной логики — `status=4`.

---

## 5. Сущность: STUDENT_DIPLOMA_INFO

- **Endpoint:** `/org-data/list/save`
- **typeCode:** `"STUDENT_DIPLOMA_INFO"`
- **Composite Key:** `STUDENT_ID_COMPOSITE_KEY` → `{ type, studentId }`

| EPVO Field | Type | Req | Logic / Source |
|------------|------|-----|----------------|
| `typeCode` | Str | ✅ | `"STUDENT_DIPLOMA_INFO"` |
| `universityId` | Int | ✅ | Системная константа ВУЗа |
| `studentId` | Int | ✅ | `local.student.id` |
| `diplomaNumber` | Str | — | Номер диплома (дублирует `GRADUATES.iacDiplomaNumber`) |
| `diplomaSeries` | Str | — | Серия диплома |
| `diplomaDate` | Date | — | Дата выдачи |
| `registrationNumber` | Str | — | Регистрационный номер диплома |
| `honor` | Bool | — | Диплом с отличием |
| `iacProtocol` | Str | — | Номер протокола ГАК/ГЭК |

### 5.1 Правило (Согласованность с GRADUATES)
```text
// Данные в STUDENT_DIPLOMA_INFO ДОЛЖНЫ совпадать с GRADUATES:
EPVO.STUDENT_DIPLOMA_INFO.diplomaNumber == EPVO.GRADUATES.iacDiplomaNumber
EPVO.STUDENT_DIPLOMA_INFO.diplomaSeries == EPVO.GRADUATES.iacDiplomaSeries
EPVO.STUDENT_DIPLOMA_INFO.diplomaDate == EPVO.GRADUATES.diplomaDate
EPVO.STUDENT_DIPLOMA_INFO.honor == EPVO.GRADUATES.diplomaHonor

// Логика: оба payload формируются из одного источника (local.diploma_*)
```

---

## 6. Приказ о выпуске (Order Type 6)

Структура приказа полностью следует композитному дереву из `RF_TFW-4.C`.

### 6.1 Маппинг специфичных полей

| Сущность | EPVO Field | Value |
|----------|-----------|-------|
| `Order` | `orderType` | `6` (Завершение обучения / Выпуск) |
| `Order` | `orderNumber` | Номер приказа о выпуске из локальной БД |
| `Order` | `orderDate` | Дата приказа о выпуске (ISO 8601) |
| `SectionPerson` | `personId` | `local.student.id` |
| `SectionPerson` | `movementDate` | Дата вступления приказа в силу |
| `OrderStudentInfo` | `degreeId` | Академическая степень на момент выпуска |

### 6.2 Правило (Привязка приказа к GRADUATES)
```text
// finishOrderNumber и finishOrderDate в GRADUATES
// ДОЛЖНЫ совпадать с Order.orderNumber и Order.orderDate:
EPVO.GRADUATES.finishOrderNumber == EPVO.Order.orderNumber
EPVO.GRADUATES.finishOrderDate == EPVO.Order.orderDate

// Если приказ ещё не загружен в ЕПВО, сначала отправить приказ (Шаг 2),
// затем GRADUATES (Шаг 5)
```

---

## 7. Данные СУР: Общежития (DORMITORY)

Для отчёта «Обеспеченность общежитиями» (ВП-7 по adm_doc) ЕПВО агрегирует данные из двух источников:
1. Таблица `DORMITORY` — физические характеристики общежития.
2. Поля профиля `STUDENT` — статус обеспеченности студента.

### 7.1 Маппинг DORMITORY

- **Endpoint:** `/org-data/list/save`
- **typeCode:** `"DORMITORY"`
- **Composite Key:** `DORMITORY_ID_COMPOSITE_KEY` → `{ type, dormitoryId }`

| EPVO Field | Type | Req | Logic / Source |
|------------|------|-----|----------------|
| `typeCode` | Str | ✅ | `"DORMITORY"` |
| `universityId` | Int | ✅ | Системная константа ВУЗа |
| `dormitoryId` | Int | ✅ | Уникальный ID общежития из локальной БД |
| `name` | Str | ✅ | Наименование на русском |
| `nameKz` | Str | ✅ | Наименование на казахском |
| `nameEn` | Str | ✅ | Наименование на английском |
| `address` | Str | ✅ | Адрес общежития |
| `phone` | Str | ✅ | Телефон общежития |
| `type` | Int | ✅ | 1 — Секционный, 2 — Коридорный |
| `startDate` | Date | ✅ | Дата начала работы |
| `finishDate` | Date | — | `null` = действующее. Если заполнено — общежитие закрыто и не попадает в отчёт СУР |
| `repairDate` | Date | — | Дата последнего ремонта |
| `square` | Dbl | ✅ | Общая площадь (кв.м.) |
| `beds` | Int | ✅ | Количество койко-мест |
| `payYear` | Int | ✅ | Стоимость за год |
| `floorCount` | Int | ✅ | Этажность |
| `roomCount` | Int | ✅ | Количество комнат |
| `rampCount` | Int | ✅ | Количество пандусов |
| `liftCount` | Int | ✅ | Количество лифтов |
| `elevatorCount` | Int | ✅ | Количество подъемников |
| `specialToiletsCount` | Int | ✅ | Количество оборудованных туалетов для инвалидов |
| `hasSpecialToilets` | Bool | ✅ | Спец. перила на входах |
| `hasParking` | Bool | ✅ | Подъездные пути, автопарковка |
| `rentalType` | Int | ✅ | 1 — Собственное, 2 — Арендованное |

### 7.2 Поля STUDENT для отчёта по общежитиям

Для корректной генерации отчёта ВП-7 (обеспеченность общежитиями) в профиле `STUDENT` должны быть заполнены:

| EPVO Field | Type | Logic / Source |
|------------|------|----------------|
| `dormStateId` | Int | Статус обеспеченности: `2` — нуждается, `3` — обеспечен |
| `sitizenshipId` | Int | Для фильтрации иностранных студентов (`!= 113`) |
| `local` | Bool | `false` = иногородний (нуждается в общежитии) |

**Правило (Scope ВП-7 — кто попадает в отчёт):**
```text
// Учитываются ТОЛЬКО:
// 1. Активные студенты (status == 1)
// 2. Иногородние (local == false) ИЛИ Иностранные (sitizenshipId != 113)
// 3. Нуждающиеся (dormStateId IN (2, 3))

// Общежития учитываются ТОЛЬКО открытые (finishDate IS NULL)
```

---

## 8. Нострификация и предыдущее образование

Для выпускников, окончивших зарубежное образовательное учреждение, обязательно передаются данные свидетельства о нострификации:

```text
IF local.educational_institution == "Зарубежное ОУ":
    EPVO.nostrificationCertificateDate = MANDATORY
    EPVO.nostrificationCertificateNumber = MANDATORY
ELSE:
    EPVO.nostrificationCertificateDate = NULL
    EPVO.nostrificationCertificateNumber = NULL
```

Это гарантирует, что отчёты СУР по предыдущему образованию не будут содержать пробелов для студентов с иностранным предыдущим образованием.

---

## 9. Дубликаты дипломов (DIPLOMA_DUPLICATES)

- **Endpoint:** `/org-data/list/save`
- **typeCode:** `"DIPLOMA_DUPLICATES"`
- **Composite Key:** `DIPLOMA_DUPLICATE_ID_COMPOSITE_KEY`

Если выпускнику выдан дубликат диплома:

| EPVO Field | Type | Logic / Source |
|------------|------|----------------|
| `diplomaDuplicateId` | Int | Уникальный ID записи |
| `graduateId` | Int | ID выпускника |
| `studentId` | Int | ID обучающегося |
| `seriesNumber` | Str | Серия и номер дубликата |
| `registrationNumber` | Str | Регистрационный номер дубликата |
| `issueDate` | Date | Дата выдачи дубликата |

```text
IF local.diplom_duplicate_given == true:
    EPVO.DIPLOMA_DUPLICATES.seriesNumber = MANDATORY
    EPVO.DIPLOMA_DUPLICATES.registrationNumber = MANDATORY
    EPVO.DIPLOMA_DUPLICATES.issueDate = MANDATORY
```

---

## 10. Observations & Risks

| # | Type | Description |
|---|------|-------------|
| 1 | **risk** | **Race Condition (Шаг 2→5):** Изменение `STUDENT.status` до загрузки `TRANSCRIPT` за последнюю сессию может привести к отклонению транскриптов ЕПВО. Строго соблюдать Sequencing Contract (раздел 2). |
| 2 | **risk** | **Дублирование полей диплома:** Номер и серия диплома отправляются в три сущности (`GRADUATES`, `STUDENT_DIPLOMA_INFO`, `STUDENT_INFO`). Рассогласование вызовет конфликт при проверке дипломов на `https://epvo.kz/#/verification_education_document`. Источник данных должен быть единым. |
| 3 | **observation** | **Поле `status` vs `isStudent`:** OpenAPI spec определяет `status` (значения 1-4), а ОСМС-логика использует `isStudent` (значения 1, 0, 3). Это одно и то же поле в разных контекстах. Интегратор должен проверить, какое имя ключа принимает API для конкретного ВУЗа. |
| 4 | **risk** | **Объём данных GRADUATES:** Массовая выгрузка выпускников (июнь-июль) может содержать тысячи записей. Рекомендуется батчинг по 100-200 записей на один HTTP POST. |
| 5 | **observation** | **Doctorants & Internship fields:** Поля для докторантуры и интернатуры (раздел 3.2, Правила 7-8) являются условно обязательными и зависят от `degreeId`. Скрипт должен динамически включать их в payload. |

---

*RF_TFW-4.E — Выпускники (Рейтинги и Дипломы) | 2026-03-13*
