# RF — TFW-2.2 / Phase A: CommonDictionary API Documentation

> **Дата**: 2026-02-26
> **Автор**: ИИ-Агент
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-2__api_endpoints](HL-TFW-2__api_endpoints.md)
> **TS**: [TS-TFW-2__api_endpoints_phase_a](TS-TFW-2__api_endpoints_phase_a.md)

---

## 1. Что сделано

Создана теоретическая документация для API-эндпоинта **CommonDictionary** на основе OpenAPI 3.0.1 спецификации ЕПВО.

### Endpoints
Базовый URL: `https://epvo.kz/isvuz/api`

#### Общие заголовки (Headers)
* `Authorization`: Basic Auth
* `Content-Type`: `application/json`
* **Query Parameter**: `universityId` (Обязателен для идентификации ОВПО).

---

### 1.1 GET `/common-dictionary/find-all`
Получение полного списка записей для глобальных справочников (без пагинации).

**Query параметры:**
* `category` (string, required): Категория справочника (например `COUNTRY`, `REGION`, `KATO`, `BANK` и др.).
* `universityId` (integer, required): ID университета.

**Пример Request:**
```http
GET /common-dictionary/find-all?category=COUNTRY&universityId=[ID_ВУЗА] HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Пример Response (200 OK):**
*В отличие от OrgData, метод возвращает обычный массив объектов, а не Pageable структуру.*
```json
[
  {
    "id": 1,
    "ru": "Казахстан",
    "kz": "Қазақстан",
    "en": "Kazakhstan",
    "category": "COUNTRY",
    "parentId": null,
    "code": "KZ"
  },
  {
    "id": 2,
    "ru": "Россия",
    "kz": "Ресей",
    "en": "Russia",
    "category": "COUNTRY",
    "parentId": null,
    "code": "RU"
  }
]
```

## 2. Ключевые решения
1. **Отсутствие пагинации:** Согласно OpenAPI спецификации, эндпоинт `/find-all` для CommonDictionary возвращает `Array of CommonDictionary`, поэтому в примере ответа приведен чистый JSON массив, а класс `Pageable` не используется.

## 3. Acceptance Criteria
- [x] Описан `find-all` для CommonDictionary
- [x] Приведены примеры JSON
- [x] Указаны заголовки и Auth

---

*RF — TFW-2.2 / Phase A: CommonDictionary API Documentation | 2026-02-26*
