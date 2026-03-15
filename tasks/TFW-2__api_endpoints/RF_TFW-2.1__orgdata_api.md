# RF — TFW-2.1 / Phase A: OrgData API Documentation

> **Дата**: 2026-02-26
> **Автор**: ИИ-Агент
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-2__api_endpoints](HL-TFW-2__api_endpoints.md)
> **TS**: [TS-TFW-2__api_endpoints_phase_a](TS-TFW-2__api_endpoints_phase_a.md)

---

## 1. Что сделано

Создана теоретическая документация для API-эндпоинтов слоя **OrgData** на основе OpenAPI 3.0.1 спецификации ЕПВО.

### Endpoints
Все запросы выполняются к базовому URL: `https://epvo.kz/isvuz/api` (предположительно, на основе репозитория).

#### Общие заголовки (Headers)
* `Authorization`: Basic Auth (Base64 закодированная строка `username:password`)
* `Content-Type`: `application/json`
* **Query Parameter**: `universityId` (Обязателен для идентификации ОВПО, например `?universityId=[ID_ВУЗА]`).

---

### 1.1 GET `/org-data/find-all-pageable`
Получение справочной информации (OrgData) с поддержкой пагинации.

**Query параметры:**
* `category` (string, required): Категория справочника (например `STUDY_FORM`, `TRAINING_DIRECTION`, `ACADEMIC_STATUS` и др.).
* `page` (integer, optional): Номер страницы (начиная с 0).
* `size` (integer, optional): Количество элементов на странице.
* `sort` (string, optional): Критерий сортировки (например `id,asc`).
* `universityId` (integer, required): ID университета.

**Пример Request:**
```http
GET /org-data/find-all-pageable?category=STUDY_FORM&page=0&size=100&universityId=[ID_ВУЗА] HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Пример Response (200 OK):**
```json
{
  "content": [
    {
      "id": 1,
      "ru": "Очная",
      "kz": "Күндізгі",
      "en": "Full-time",
      "category": "STUDY_FORM",
      "parentId": null,
      "code": "1"
    }
  ],
  "pageable": {
    "sort": { "sorted": true, "unsorted": false, "empty": false },
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 100,
    "paged": true,
    "unpaged": false
  },
  "totalPages": 1,
  "totalElements": 1,
  "last": true,
  "size": 100,
  "number": 0,
  "sort": { "sorted": true, "unsorted": false, "empty": false },
  "numberOfElements": 1,
  "first": true,
  "empty": false
}
```

---

### 1.2 GET `/org-data/find-by-id`
Получение конкретной записи OrgData по ID.

**Query параметры:**
* `id` (integer, required): ID записи.
* `universityId` (integer, required): ID университета.

**Пример Request:**
```http
GET /org-data/find-by-id?id=1&universityId=[ID_ВУЗА] HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Пример Response (200 OK):**
```json
{
  "id": 1,
  "ru": "Очная",
  "kz": "Күндізгі",
  "en": "Full-time",
  "category": "STUDY_FORM",
  "parentId": null,
  "code": "1"
}
```

## 2. Ключевые решения
1. **Теоретические примеры:** Приведены JSON-формы, собранные из OpenAPI 3.0.1. В реальности ответ сервера может незначительно отличаться (например, метаданные `Pageable` от Spring Data).

## 3. Acceptance Criteria
- [x] Описан `find-all-pageable`
- [x] Описан `find-by-id`
- [x] Приведены примеры JSON

---

*RF — TFW-2.1 / Phase A: OrgData API Documentation | 2026-02-26*
