# RF_TFW-1.11 — Международное сотрудничество

> **Группа:** Зарубежные вузы, соглашения, дисциплины мобильности, источники финансирования, форма ДСПИТ-3
> **Сущностей:** 6 | **Composite Key:** `TRANSFER_ID_COMPOSITE_KEY`, `UNIVERSITY_ID_COMPOSITE_KEY`

---

## 1. FOREIGN_UNIVERSITIES — Зарубежные вузы

**typeCode:** `FOREIGN_UNIVERSITIES`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"FOREIGN_UNIVERSITIES"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный код |
| nameRu | string | | Название вуза RU |
| nameKz | string | | Название вуза KZ |
| nameEn | string | | Название вуза EN |
| countryId | int32 | | Страна зарубежного вуза (→ `CenterCountry`) |
| rating | int32 | | Рейтинг |
| centerUniversityId | int32 | | ID из центр. справочника ОВПО |

**FK-зависимости:** `CenterCountry` (countryId)

---

## 2. FOREIGN_UNIVERSITIES_AGREEMENT — Соглашения по обмену

**typeCode:** `FOREIGN_UNIVERSITIES_AGREEMENT`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"FOREIGN_UNIVERSITIES_AGREEMENT"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | ID соглашения |
| foreignUniversityId | int32 | | ID зарубежного вуза (→ ForeignUniversities) |
| agreementNumber | string | | Номер меморандума |
| startDate | date | | Дата начала |
| finishDate | date | | Дата окончания |

**FK-зависимости:** `ForeignUniversities`

---

## 3. FOREIGN_SUBJECTS — Дисциплины акад. мобильности

**typeCode:** `FOREIGN_SUBJECTS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"FOREIGN_SUBJECTS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID записи |
| transferId | int32 | | ID мобильности (→ StudentTransfer) |
| subjectName | string | | Название дисциплины |
| rk | int32 | | Кредиты |
| ects | int32 | | Кредиты ECTS |
| getsDegree | string | | Учёная степень |
| fio | string | | ФИО преподавателя |
| moneySource | string | | Источник финансирования мобильности (грант, бюджет, личные средства и т.д.) |
| moneySpent | string | | Сумма затрат на мобильность (текстом, может содержать валюту) |
| profession | string | | ГОП / специальность обучающегося (текстом для отчётности) |
| program | string | | Программа академического обмена (текстом: Erasmus+, Bolashak и т.д.) |

**FK-зависимости:** `StudentTransfer`

---

## 4. FOREIGN_LANG_CERTIFICATE — Международные сертификаты по ин. языку

**typeCode:** `FOREIGN_LANG_CERTIFICATE`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"FOREIGN_LANG_CERTIFICATE"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| name | string | | Наименование сертификата |
| language | int32 | | Язык сдачи (→ `CenterStudyLanguages`) |
| minScore | double | | Минимальный (пороговый) балл |
| maxScore | double | | Максимальный балл |
| scoreType | int32 | | Тип вводимых данных |

**FK-зависимости:** `CenterStudyLanguages`

---

## 5. FINANCING_SOURCE_ACADEMIC_MOBILITY — Источники финансирования мобильности

**typeCode:** `FINANCING_SOURCE_ACADEMIC_MOBILITY`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"FINANCING_SOURCE_ACADEMIC_MOBILITY"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID записи |
| nameRu | string | | Название RU |
| nameKz | string | | Название KZ |
| nameEn | string | | Название EN |

---

## 6. DSPIT_FORM_3 — Форма ДСПИТ-3 (международные проекты)

**typeCode:** `DSPIT_FORM_3`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"DSPIT_FORM_3"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| docCount | int32 | | Кол-во международных договоров/проектов |
| docName | string | | Наименование договора/проекта |
| partnerName | string | | Наименование вуза-партнёра |
| docDate | date | | Дата заключения |
| startDate | date | | Дата начала |
| endDate | date | | Дата окончания |
| country | int32 | | Страна (→ `CenterCountry`) |
| termless | boolean | | Бессрочный |

**FK-зависимости:** `CenterCountry`

---

## ✅ Поля с неясным описанием (заполнены выводами)

| Сущность | Поле | Наш вывод |
|----------|------|----------|
| FOREIGN_UNIVERSITIES | countryId | Страна зарубежного вуза (FK → CenterCountry) |
| FOREIGN_SUBJECTS | moneySource | Источник финансирования мобильности |
| FOREIGN_SUBJECTS | moneySpent | Сумма затрат на мобильность |
| FOREIGN_SUBJECTS | profession | ГОП / специальность обучающегося |
| FOREIGN_SUBJECTS | program | Программа академического обмена |

---

*Создано: 2026-02-19 | Источник: OpenAPI spec v0 (epvo.kz)*
