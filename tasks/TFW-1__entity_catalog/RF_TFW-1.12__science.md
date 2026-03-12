# RF_TFW-1.12 — Наука

> **Группа:** Научные проекты, стипендияты, научная деятельность, НИР
> **Сущностей:** 5 | **Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY`, `SCIENCE_PROJECT_ID_COMPOSITE_KEY`

---

## 1. SCIENCE_PROJECTS — Научные проекты

**typeCode:** `SCIENCE_PROJECTS`
**Composite Key:** `SCIENCE_PROJECT_ID_COMPOSITE_KEY` → `{ type, projectId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"SCIENCE_PROJECTS"` |
| universityId | int32 | ✅ | ID вуза |
| projectId | int32 | ✅ | Уникальный ID проекта |
| nameRu | string | | Название проекта RU |
| nameKz | string | | Название проекта KZ |
| nameEn | string | | Название проекта EN |
| managerId | int32 | | Руководитель проекта (→ Tutor) |
| startDate | date | | Дата начала |
| finishDate | date | | Дата окончания |
| totalAmount | double | | Общая сумма финансирования |
| sourceId | int32 | | Источник финансирования |
| statusId | int32 | | Статус проекта |

**FK-зависимости:** `Tutor`

---

## 2. SCIENCE_PROJECTS_MEMBERS — Участники научных проектов

**typeCode:** `SCIENCE_PROJECTS_MEMBERS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"SCIENCE_PROJECTS_MEMBERS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID записи |
| projectId | int32 | | ID проекта (→ ScienceProjects) |
| tutorId | int32 | | ID преподавателя (→ Tutor) |
| roleId | int32 | | Роль в проекте |

**FK-зависимости:** `ScienceProjects`, `Tutor`

---

## 3. STIPENDIATY — Стипендиаты (государственные программы)

**typeCode:** `STIPENDIATY`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"STIPENDIATY"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID записи |
| studentId | int32 | | ID обучающегося (→ Student) |
| scholarshipName | string | | Название стипендии |
| year | int32 | | Учебный год |
| amount | double | | Сумма |

**FK-зависимости:** `Student`

---

## 4. DSPIT_FORM_1 — Форма ДСПИТ-1 (научная деятельность)

**typeCode:** `DSPIT_FORM_1`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"DSPIT_FORM_1"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Тематика НИР RU |
| nameKz | string | | Тематика НИР KZ |
| nameEn | string | | Тематика НИР EN |
| managerName | string | | ФИО руководителя |
| totalMoney | double | | Общее финансирование |
| budgetMoney | double | | Бюджетное финансирование |
| extraBudgetMoney | double | | Внебюджетное финансирование |

---

## 5. DSPIT_FORM_2 — Форма ДСПИТ-2 (международные услуги)

**typeCode:** `DSPIT_FORM_2`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"DSPIT_FORM_2"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Наименование вида услуг RU |
| nameKz | string | | Наименование вида услуг KZ |
| nameEn | string | | Наименование вида услуг EN |
| countryId | int32 | | Страна  (→ `CenterCountry`) |
| countryExecutorName | string | | Страна и название исполнителя |
| amountInKzt | double | | Стоимость в тенге |
| amountInUsd | double | | Стоимость в долларах |

**FK-зависимости:** `CenterCountry`

---

## ❓ Поля с неясным описанием

В данной группе **нет** полей с пустым описанием.

---

*Создано: 2026-02-19 | Источник: OpenAPI spec v0 (epvo.kz)*
