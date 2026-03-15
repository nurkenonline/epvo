# RF — TFW-2.4 / Phase B: OrgData Save (Mass UPSERT) API Documentation

> **Дата**: 2026-02-26
> **Автор**: ИИ-Агент
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-2__api_endpoints](HL-TFW-2__api_endpoints.md)
> **TS**: [TS-TFW-2__api_endpoints_phase_b](TS-TFW-2__api_endpoints_phase_b.md)

---

## 1. Что сделано

Создана теоретическая документация для эндпоинта массового сохранения (UPSERT) справочных данных OrgData в ЕПВО.

### Общие заголовки (Headers)
* `Authorization`: Basic Auth (Base64 закодированная строка `username:password`)
* `Content-Type`: `application/json`

---

### 1.1 POST `/org-data/list/save`

Массовое сохранение (создание или обновление) записей OrgData. Этот эндпоинт работает по принципу **UPSERT**: если запись с заданным композитным ключом уже существует — она обновляется, если нет — создаётся новая.

> ⚠️ **Важно (из логов чата ЕПВО):** Одиночный эндпоинт `POST /org-data/save` **не работает** (возвращает 404/Not Found). Всегда используйте `/org-data/list/save` и передавайте массив объектов, даже если требуется сохранить одну запись.

**Query параметры:**
* `universityId` (integer, required): ID университета (например `[ID_ВУЗА]`).

**Request Body:**
Массив JSON-объектов. Каждый объект содержит:
* `typeCode` (string, required): Код справочника OrgData (например `FACULTIES`, `STUDENT`, `CAFEDRA`).
* Далее — все поля DTO конкретного справочника (полный перечень полей см. в [TFW-1 Entity Catalog](../TFW-1__entity_catalog/HL_TFW-1__entity_catalog.md)).

**Пример Request (сохранение двух факультетов):**
```http
POST /org-data/list/save?universityId=[ID_ВУЗА] HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json
```
```json
[
  {
    "typeCode": "FACULTIES",
    "facultyId": 101,
    "nameRu": "Факультет информационных технологий",
    "nameKz": "Ақпараттық технологиялар факультеті",
    "nameEn": "Faculty of Information Technologies",
    "shortNameRu": "ФИТ",
    "shortNameKz": "АТФ",
    "shortNameEn": "FIT",
    "isActive": true
  },
  {
    "typeCode": "FACULTIES",
    "facultyId": 102,
    "nameRu": "Юридический факультет",
    "nameKz": "Заң факультеті",
    "nameEn": "Faculty of Law",
    "shortNameRu": "ЮФ",
    "shortNameKz": "ЗФ",
    "shortNameEn": "FL",
    "isActive": true
  }
]
```

---

### 1.2 Структура ответа (Response)

**Response (200 OK):**

Сервер возвращает объект-обёртку с метаданными обработки:

```json
{
  "requestedElements": 2,
  "savedElements": 1,
  "updatedElements": 1,
  "failedElementsCcount": 0,
  "failedRecords": []
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `requestedElements` | integer | Сколько объектов было передано в запросе |
| `savedElements` | integer | Сколько новых записей создано |
| `updatedElements` | integer | Сколько существующих записей обновлено |
| `failedElementsCcount` | integer | Сколько записей отклонено из-за ошибок валидации |
| `failedRecords` | array | Массив объектов с описанием ошибок (см. ниже) |

> ⚠️ **Предположение:** Название поля `failedElementsCcount` содержит опечатку (двойная буква `C`). Это зафиксировано в OpenAPI-спецификации и, вероятно, является ошибкой в исходном коде бэкенда.

---

### 1.3 Структура `failedRecords` (обработка ошибок)

При частичных ошибках валидации (например, не заполнено обязательное поле) сервер **не отклоняет весь запрос**. Записи, прошедшие валидацию, сохраняются; остальные попадают в массив `failedRecords`.

**Пример ответа с ошибками:**
```json
{
  "requestedElements": 3,
  "savedElements": 1,
  "updatedElements": 1,
  "failedElementsCcount": 1,
  "failedRecords": [
    {
      "record": {
        "typeCode": "STUDENT",
        "studentId": 12345,
        "lastname": "Иванов"
      },
      "errors": [
        "icDepartmentId не должно равняться null",
        "graduatedCountryId не должно равняться null"
      ]
    }
  ]
}
```

> ⚠️ **Предположение:** Точная структура объекта внутри `failedRecords` описана теоретически. Поле `record` содержит исходный DTO, который не прошел валидацию. Поле `errors` содержит массив строк с описаниями ошибок. Структура может незначительно варьироваться (например, `errorMessage` вместо `errors`).

> ⚠️ **Из логов чата (2025-08-26):** Сервер может возвращать HTTP 400 Bad Request **без** подробного тела ответа (только `{"timestamp":"...","status":400,"error":"Bad Request","path":"/isvuz/api/org-data/list/save"}`), если формат запроса в целом некорректен (не массив, неверный `typeCode` и т.п.). Структура `failedRecords` появляется только при валидных запросах с ошибками на уровне отдельных записей.

---

### 1.4 Механизм UPSERT (Создание или Обновление)

ЕПВО определяет, создавать новую запись или обновлять существующую, на основе **композитного ключа** (composite key). Каждый справочник OrgData использует свой тип ключа:

| Справочник | Тип композитного ключа |
|------------|----------------------|
| STUDENT, STUDENT_INFO, STUDENT_DIPLOMA_INFO | `STUDENT_ID_COMPOSITE_KEY` |
| FACULTIES | `FACULTY_ID_COMPOSITE_KEY` |
| CAFEDRA | `CAFEDRA_ID_COMPOSITE_KEY` |
| TUTOR | `TUTOR_ID_COMPOSITE_KEY` |
| GROUPS | `GROUP_ID_COMPOSITE_KEY` |
| PROFESSION | `PROFESSION_ID_COMPOSITE_KEY` |
| BUILDINGS, SPORTS_CONSTRUCTIONS | `BUILDING_ID_COMPOSITE_KEY` |
| Все прочие | `UNIVERSITY_ID_COMPOSITE_KEY` (fallback) |

**Логика:**
1. Сервер извлекает из каждого DTO значение ключевого поля (например, `studentId` для `STUDENT`).
2. Если запись с таким ключом **существует** в БД ЕПВО — обновляет все поля.
3. Если **не существует** — создает новую запись.
4. Если ключ передан некорректно (пустой или null) — запись попадает в `failedRecords` с ошибкой `"Запись о студенте с такими данными уже существует"` или аналогичной.

---

## 2. Ключевые решения
1. **Теоретические примеры:** JSON-формы собраны из OpenAPI 3.0.1 и дополнены инсайтами из логов чата ЕПВО (2025–2026 гг.).
2. **Partial Success:** Сервер поддерживает частичное сохранение — это означает, что клиент должен проверять `failedRecords` после каждого вызова и повторно отправлять исправленные записи.

## 3. Acceptance Criteria
- [x] Описан `POST /org-data/list/save`
- [x] Описана структура `failedRecords`
- [x] Описан механизм UPSERT на базе композитных ключей
- [x] Приведены примеры JSON-запросов и ответов

---

*RF — TFW-2.4 / Phase B: OrgData Save (Mass UPSERT) API Documentation | 2026-02-26*
