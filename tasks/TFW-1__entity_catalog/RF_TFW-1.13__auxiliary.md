# RF_TFW-1.13 — Вспомогательные справочники (org-data)

> **Группа:** Справочники вуза — награды, льготы, виды приказов, типы экзаменов, учёные степени, источники воен. подготовки и т.д.
> **Сущностей:** 8 | **Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY`

---

## 1. AWARDS — Награды

**typeCode:** `AWARDS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"AWARDS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название награды RU |
| nameKz | string | | Название награды KZ |
| nameEn | string | | Название награды EN |

---

## 2. BENEFITS — Льготы

**typeCode:** `BENEFITS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"BENEFITS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название льготы RU |
| nameKz | string | | Название льготы KZ |
| nameEn | string | | Название льготы EN |
| code | string | | Код льготы |

---

## 3. ORDER_TYPE — Типы приказов

**typeCode:** `ORDER_TYPE`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"ORDER_TYPE"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название типа приказа RU |
| nameKz | string | | Название типа приказа KZ |
| nameEn | string | | Название типа приказа EN |

---

## 4. ORDER_CATEGORY — Категории приказов

**typeCode:** `ORDER_CATEGORY`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"ORDER_CATEGORY"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название категории RU |
| nameKz | string | | Название категории KZ |
| nameEn | string | | Название категории EN |
| orderTypeId | int32 | | Тип приказа (→ OrderType) |

**FK-зависимости:** `OrderType`

---

## 5. ACADEMIC_STATUS — Академический статус (ППС)

**typeCode:** `ACADEMIC_STATUS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"ACADEMIC_STATUS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название статуса RU |
| nameKz | string | | Название статуса KZ |
| nameEn | string | | Название статуса EN |

---

## 6. SCIENTIFIC_DEGREE — Учёная степень

**typeCode:** `SCIENTIFIC_DEGREE`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"SCIENTIFIC_DEGREE"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название степени RU |
| nameKz | string | | Название степени KZ |
| nameEn | string | | Название степени EN |

---

## 7. INSTITUTIONS — Организации образования (школы, колледжи)

**typeCode:** `INSTITUTIONS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"INSTITUTIONS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название организации RU |
| nameKz | string | | Название организации KZ |
| nameEn | string | | Название организации EN |
| regionId | int32 | | Регион (→ `CenterRegion`) |
| typeId | int32 | | Тип учебного заведения |
| centerInstitutionId | int32 | | ID из центр. справочника |

**FK-зависимости:** `CenterRegion`

---

## 8. MILITARY_TRAINING_PROGRAMS — Программы военной подготовки

**typeCode:** `MILITARY_TRAINING_PROGRAMS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"MILITARY_TRAINING_PROGRAMS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название программы RU |
| nameKz | string | | Название программы KZ |
| nameEn | string | | Название программы EN |
| code | string | | Код программы |

---

## ❓ Поля с неясным описанием

В данной группе **нет** полей с пустым описанием.

---

*Создано: 2026-02-19 | Источник: OpenAPI spec v0 (epvo.kz)*
