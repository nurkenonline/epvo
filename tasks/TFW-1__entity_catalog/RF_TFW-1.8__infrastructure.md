# RF_TFW-1.8 — Инфраструктура

> **Группа:** Корпуса, общежития, аудитории, лаборатории, спортивные сооружения, научные корпуса
> **Сущностей:** 8 | **Composite Key:** `BUILDING_ID_COMPOSITE_KEY`, `DORMITORY_ID_COMPOSITE_KEY`, `EDUC_BUILDING_ID_COMPOSITE_KEY`, `AUDITORY_ID_COMPOSITE_KEY`, `AUDITORY_TYPE_ID_COMPOSITE_KEY`, `LABORATORY_ID_COMPOSITE_KEY`, `UNIVERSITY_ID_COMPOSITE_KEY`

---

## 1. BUILDINGS — Прочие корпуса вуза

**typeCode:** `BUILDINGS`
**Composite Key:** `BUILDING_ID_COMPOSITE_KEY` → `{ type, buildingId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"BUILDINGS"` |
| universityId | int32 | ✅ | ID вуза |
| buildingId | int32 | ✅ | Уникальный ID корпуса |
| buildingName | string | | Название корпуса RU |
| buildingNameKz | string | | Название корпуса KZ |
| buildingNameEn | string | | Название корпуса EN |
| address | string | | Адрес |
| square | double | | Общая площадь (кв.м.) |
| usefull | int32 | | Полезная площадь |
| auditory | int32 | | Кол-во аудиторий |
| service | int32 | | Аудиторный фонд (кв.м.) |
| outOfAuditory | int32 | | Внеаудиторный фонд (кв.м.) |
| floorCount | int32 | | Этажность |
| startDate | date | | Дата ввода в эксплуатацию |
| finishDate | date | | Дата закрытия |
| isAcademic | boolean | | Является учебным корпусом |

**FK-зависимости:** нет

---

## 2. EDUCATION_BUILDINGS — Учебные корпуса

**typeCode:** `EDUCATION_BUILDINGS`
**Composite Key:** `EDUC_BUILDING_ID_COMPOSITE_KEY` → `{ type, educBuildingId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"EDUCATION_BUILDINGS"` |
| universityId | int32 | ✅ | ID вуза |
| educBuildingId | int32 | ✅ | Уникальный ID учебного корпуса |
| buildingName | string | | Название RU |
| buildingNameKz | string | | Название KZ |
| buildingNameEn | string | | Название EN |
| address | string | | Адрес |
| typeBuilding | int32 | | Тип (1-типовое, 2-нетиповое) |
| startDate | date | | Год ввода в эксплуатацию |
| finishDate | date | | Дата вывода из эксплуатации (закрытия корпуса); null = действующий. По аналогии с Buildings.finishDate |
| square | double | | Общая площадь (кв.м.) |
| classroomFund | double | | Аудиторный фонд (кв.м.) |
| extracurricularFund | double | | Внеаудиторный фонд (кв.м.) |
| floorCount | int32 | | Этажность |
| rampCount | int32 | | Кол-во пандусов |
| liftCount | int32 | | Кол-во лифтов |
| elevatorCount | int32 | | Кол-во подъемников |
| hasSpecialToilets | boolean | | Спец. перила для людей с ОУ |
| specialToiletsCount | int32 | | Кол-во оборудованных туалетов |
| hasParking | boolean | | Подъездные пути и автопарковка |

---

## 3. DORMITORY — Общежития

**typeCode:** `DORMITORY`
**Composite Key:** `DORMITORY_ID_COMPOSITE_KEY` → `{ type, dormitoryId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"DORMITORY"` |
| universityId | int32 | ✅ | ID вуза |
| dormitoryId | int32 | ✅ | Код общежития |
| name | string | | Название RU |
| nameKz | string | | Название KZ |
| nameEn | string | | Название EN |
| address | string | | Адрес |
| phone | string | | Телефон |
| type | int32 | | Тип (1-секционный, 2-коридорный) |
| startDate | date | | Год ввода |
| repairDate | date | | Год ремонта |
| finishDate | date | | Дата закрытия общежития; null = действующее. По аналогии с Buildings.finishDate |
| square | double | | Общая площадь |
| beds | int32 | | Кол-во койко-мест |
| payYear | int32 | | Оплата за год |
| floorCount | int32 | | Этажность |
| roomCount | int32 | | Кол-во комнат |
| rampCount | int32 | | Кол-во пандусов |
| liftCount | int32 | | Кол-во лифтов |
| elevatorCount | int32 | | Кол-во подъемников |
| specialToiletsCount | int32 | | Кол-во туалетов для инвалидов |
| hasSpecialToilets | boolean | | Спец. перила |
| hasParking | boolean | | Подъездные пути и парковка |
| rentalType | int32 | | Вид аренды (1-собственное, 2-арендованное) |

---

## 4. AUDITORIES — Аудитории

**typeCode:** `AUDITORIES`
**Composite Key:** `AUDITORY_ID_COMPOSITE_KEY` → `{ type, auditoryId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"AUDITORIES"` |
| universityId | int32 | ✅ | ID вуза |
| auditoryId | int32 | ✅ | Уникальный ID аудитории |
| auditoryName | string | | Название RU |
| auditoryNameKz | string | | Название KZ |
| auditoryNameEn | string | | Название EN |
| buildingId | int32 | | ID корпуса (→ Buildings/EducationBuildings) |
| auditoryType | int32 | | Тип аудитории (→ AuditoryType) |
| capacity | int32 | | Вместимость |
| closed | boolean | | Аудитория закрыта |
| area | double | | Площадь (кв.м.) |

**FK-зависимости:** `Buildings`/`EducationBuildings`, `AuditoryType`

---

## 5. AUDITORY_TYPES — Типы аудиторий

**typeCode:** `AUDITORY_TYPES`
**Composite Key:** `AUDITORY_TYPE_ID_COMPOSITE_KEY` → `{ type, typeId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"AUDITORY_TYPES"` |
| universityId | int32 | ✅ | ID вуза |
| typeId | int32 | ✅ | Уникальный ID типа |
| name | string | | Название RU |
| nameKz | string | | Название KZ |
| nameEn | string | | Название EN |
| description | string | | Описание типа |

---

## 6. LABORATORIES — Лаборатории

**typeCode:** `LABORATORIES`
**Composite Key:** `LABORATORY_ID_COMPOSITE_KEY` → `{ type, labId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"LABORATORIES"` |
| universityId | int32 | ✅ | ID вуза |
| labId | int32 | ✅ | Уникальный ID лаборатории |
| nameRu | string | | Название RU |
| nameKz | string | | Название KZ |
| nameEn | string | | Название EN |
| buildingId | int32 | | ID корпуса |
| cafedraId | int32 | | ID кафедры (→ Cafedra) |
| area | double | | Площадь |
| capacity | int32 | | Вместимость |

**FK-зависимости:** `Buildings`, `Cafedra`

---

## 7. SPORTS_CONSTRUCTIONS — Спортивные сооружения

**typeCode:** `SPORTS_CONSTRUCTIONS`
**Composite Key:** `BUILDING_ID_COMPOSITE_KEY` → `{ type, buildingId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"SPORTS_CONSTRUCTIONS"` |
| universityId | int32 | ✅ | ID вуза |
| buildingId | int32 | ✅ | Уникальный ID сооружения |
| buildingName | string | | Название RU |
| buildingNameKz | string | | Название KZ |
| buildingNameEn | string | | Название EN |
| address | string | | Адрес |
| square | double | | Площадь |
| startDate | date | | Дата ввода |

---

## 8. SCIENCE_BUILDINGS — Научные корпуса

**typeCode:** `SCIENCE_BUILDINGS`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"SCIENCE_BUILDINGS"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| nameRu | string | | Название RU |
| nameKz | string | | Название KZ |
| nameEn | string | | Название EN |
| address | string | | Адрес |
| square | double | | Площадь |

---

## ✅ Поля с неясным описанием (заполнены выводами)

| Сущность | Поле | Наш вывод |
|----------|------|----------|
| EDUCATION_BUILDINGS | finishDate | Дата закрытия корпуса (аналогично Buildings.finishDate) |
| DORMITORY | finishDate | Дата закрытия общежития (аналогично Buildings.finishDate) |

---

*Создано: 2026-02-19 | Источник: OpenAPI spec v0 (epvo.kz)*
