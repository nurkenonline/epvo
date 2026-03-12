# RF_TFW-1.9 — Выпускники

> **Группа:** Выпускники, дубликаты дипломов, трудоустройство
> **Сущностей:** 3 | **Composite Key:** `GRADUATE_ID_COMPOSITE_KEY`, `DIPLOMA_DUPLICATE_ID_COMPOSITE_KEY`, `UNIVERSITY_ID_COMPOSITE_KEY`

---

## 1. GRADUATES — Выпускники

**typeCode:** `GRADUATES`
**Composite Key:** `GRADUATE_ID_COMPOSITE_KEY` → `{ type, graduateId }`

> ⚠️ Множество обязательных (not null) полей — самая «строгая» сущность в API.

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ (not null) | `"GRADUATES"` |
| universityId | int32 | ✅ (not null) | ID вуза |
| graduateId | int32 | ✅ (not null) | Код выпускника |
| firstName | string | ✅ (not null) | Имя |
| lastName | string | | Фамилия |
| patronymic | string | | Отчество |
| birthDate | date | ✅ (not null) | Дата рождения |
| sexId | int32 | ✅ (not null) | Пол (→ `Sex`) |
| iin | string | | ИИН |
| nationId | int32 | ✅ (not null) | Национальность (→ `CenterNationality`) |
| sitizenshipId | int32 | ✅ (not null) | Гражданство (→ `CenterCountry`) |
| professionId | int32 | | ГОП (→ Profession) |
| studyFormId | int32 | | Форма обучения (→ StudyForms) |
| paymentFormId | int32 | ✅ (not null) | Форма оплаты (→ `PaymentForms`) |
| studyLanguageId | int32 | ✅ (not null) | Язык обучения (→ `CenterStudyLanguages`) |
| degreeId | int32 | ✅ (not null) | Академическая степень (→ `DegreeTypes`) |
| startDate | date | ✅ (not null) | Дата зачисления |
| startOrderNumber | string | ✅ (not null) | Номер приказа о зачислении |
| finishOrderNumber | string | ✅ (not null) | Номер приказа о выпуске |
| finishOrderDate | date | ✅ (not null) | Дата приказа о выпуске |
| iacDiplomaNumber | string | ✅ (not null) | Номер диплома |
| iacDiplomaSeries | string | ✅ (not null) | Серия диплома |
| centerProfChecked | boolean | ✅ (not null) | Проверка центр. справочника ГОП |
| diplomaDate | date | | Дата выдачи диплома |
| diplomaHonor | boolean | | Диплом с отличием |
| hasJobId | int32 | | Метка трудоустройства (→ `HasJobs`) |
| jobPlaceTypeId | int32 | | Тип организации трудоустройства (→ `JobPlaceType`) |
| organizationFormId | int32 | | Вид организации (→ `OrganizationForms`) |
| reasonEmploymentId | int32 | | Причина трудоустройства/нетрудоустройства (→ `DicReasonEmployment`) |
| placeOfFurtherEducationId | int32 | | Место дальнейшего обучения (→ `PlaceOfFurtherEducation`) |
| gpa | double | | GPA |
| enrollYear | int32 | | Год поступления |
| graduationYear | int32 | | Год выпуска |
| registrationNumber | string | | Регистрационный номер диплома |
| specializationId | int32 | | ОП (→ Specializations) |
| studentId | int32 | | ID обучающегося (→ Student) |

**FK-зависимости:** `Sex`, `CenterNationality`, `CenterCountry`, `Profession`, `StudyForms`, `PaymentForms`, `CenterStudyLanguages`, `DegreeTypes`, `HasJobs`, `JobPlaceType`, `OrganizationForms`, `DicReasonEmployment`, `PlaceOfFurtherEducation`, `Specializations`, `Student`

---

## 2. DIPLOMA_DUPLICATES — Дубликаты дипломов

**typeCode:** `DIPLOMA_DUPLICATES`
**Composite Key:** `DIPLOMA_DUPLICATE_ID_COMPOSITE_KEY` → `{ type, diplomaDuplicateId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"DIPLOMA_DUPLICATES"` |
| universityId | int32 | ✅ | ID вуза |
| diplomaDuplicateId | int32 | ✅ | ID дубликата |
| studentId | int32 | | ID обучающегося (→ Student) |
| graduateId | int32 | | ID выпускника (→ Graduates) |
| seriesNumber | string | | Серия и номер |
| registrationNumber | string | | Регистрационный номер |
| issueDate | date | | Дата выдачи (`yyyy-MM-dd`) |

**FK-зависимости:** `Student`, `Graduates`

---

## 3. RETIRES — Отчисленные

**typeCode:** `RETIRES`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"RETIRES"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| studentId | int32 | | ID обучающегося (→ Student) |
| reason | string | | Причина отчисления |
| orderNumber | string | | Номер приказа |
| orderDate | date | | Дата приказа |
| courseNumber | int32 | | Курс на момент отчисления |

**FK-зависимости:** `Student`

---

## ❓ Поля с неясным описанием

В данной группе **нет** полей с пустым описанием.

---

*Создано: 2026-02-19 | Источник: OpenAPI spec v0 (epvo.kz)*
