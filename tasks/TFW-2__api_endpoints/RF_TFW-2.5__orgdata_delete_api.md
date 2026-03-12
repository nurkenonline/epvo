# RF — TFW-2.5 / Phase B: OrgData Delete API Documentation

> **Дата**: 2026-02-26
> **Автор**: ИИ-Агент
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-2__api_endpoints](HL-TFW-2__api_endpoints.md)
> **TS**: [TS-TFW-2__api_endpoints_phase_b](TS-TFW-2__api_endpoints_phase_b.md)

---

## 1. Что сделано

Создана теоретическая документация для эндпоинта удаления записей OrgData в ЕПВО. Документ основан на OpenAPI-спецификации и **недокументированном рабочем примере**, извлечённом из логов чата ЕПВО от 14 января 2026 года.

### Общие заголовки (Headers)
* `Authorization`: Basic Auth (Base64 закодированная строка `username:password`)
* `Content-Type`: `application/json`

---

### 1.1 POST `/org-data/{code}/delete`

Удаление записи OrgData по её композитному ключу. Код справочника передаётся прямо в URL (path parameter), а идентификатор записи — в теле запроса (Body).

> ⚠️ **Важно (из логов чата ЕПВО, 2026-01-14):** Несмотря на то, что семантически это операция удаления, фактический HTTP-метод — `POST`, а не `DELETE`. Тело запроса обязательно и содержит тип композитного ключа и значение идентификатора.

**Path параметры:**
* `{code}` (string, required): Код справочника OrgData (например `STUDENT_BENEFIT`, `STUDENT`, `GRADUATES`, `TUTOR_CAFEDRA`).

**Request Body:**

| Поле | Тип | Описание |
|------|-----|----------|
| `type` | string, required | Тип композитного ключа (см. таблицу ниже) |
| `{keyField}` | integer, required | Значение идентификатора записи. Имя поля зависит от типа ключа |

---

### 1.2 Рабочий пример из логов чата ЕПВО

**Источник:** Сообщение от Турмаганбетова Каиржана в чате техподдержки ЕПВО, 14 января 2026 г.

**cURL:**
```bash
curl --location 'https://epvo.kz/isvuz/api/org-data/STUDENT_BENEFIT/delete' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=' \
  --data '{
    "type": "STUDENT_ID_COMPOSITE_KEY",
    "studentId": 704950
  }'
```

**Эквивалент HTTP:**
```http
POST /org-data/STUDENT_BENEFIT/delete HTTP/1.1
Host: epvo.kz
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json

{
  "type": "STUDENT_ID_COMPOSITE_KEY",
  "studentId": 704950
}
```

---

### 1.3 Маппинг Body-полей по типу композитного ключа

Значение поля `type` определяет, какое поле с идентификатором следует передать в Body:

| `type` (composite key) | Поле ID в Body | Пример |
|-------------------------|---------------|--------|
| `STUDENT_ID_COMPOSITE_KEY` | `studentId` | `{ "type": "STUDENT_ID_COMPOSITE_KEY", "studentId": 704950 }` |
| `FACULTY_ID_COMPOSITE_KEY` | `facultyId` | `{ "type": "FACULTY_ID_COMPOSITE_KEY", "facultyId": 101 }` |
| `CAFEDRA_ID_COMPOSITE_KEY` | `cafedraId` | `{ "type": "CAFEDRA_ID_COMPOSITE_KEY", "cafedraId": 55 }` |
| `TUTOR_ID_COMPOSITE_KEY` | `tutorId` | `{ "type": "TUTOR_ID_COMPOSITE_KEY", "tutorId": 3200 }` |
| `GROUP_ID_COMPOSITE_KEY` | `groupId` | `{ "type": "GROUP_ID_COMPOSITE_KEY", "groupId": 87 }` |
| `BUILDING_ID_COMPOSITE_KEY` | `buildingId` | `{ "type": "BUILDING_ID_COMPOSITE_KEY", "buildingId": 12 }` |
| `UNIVERSITY_ID_COMPOSITE_KEY` | `id` | `{ "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": 999 }` |

> ⚠️ **Предположение:** Имена полей ID (`studentId`, `facultyId` и т.д.) выведены из паттерна `{entityName}Id`, подтверждённого единственным рабочим примером из чата (`studentId`). Для менее распространённых ключей (например `TERM_ID_COMPOSITE_KEY`, `PLATOON_ID_COMPOSITE_KEY`) точные имена полей требуют практической верификации.

> ⚠️ **Предположение:** Для типа `UNIVERSITY_ID_COMPOSITE_KEY` (fallback для справочников без собственного ключа) имя ID-поля может быть просто `id`. Требуется практическая проверка.

---

### 1.4 Ответ сервера (Response)

> ⚠️ **Предположение:** Точный формат ответа `/delete` не задокументирован в OpenAPI и не приведён в логах чата. Ниже приведен теоретически ожидаемый ответ.

**Response (200 OK) — успешное удаление:**
```json
{
  "success": true
}
```

**Response (400 Bad Request) — запись не найдена или некорректный ключ:**
```json
{
  "timestamp": "2026-01-14T10:39:06.000+00:00",
  "status": 400,
  "error": "Bad Request",
  "path": "/isvuz/api/org-data/STUDENT_BENEFIT/delete"
}
```

---

### 1.5 Особенности и ограничения

1. **Одна запись за раз.** В отличие от `/list/save`, эндпоинт `/delete` удаляет **одну** запись. Массового удаления нет.

2. **Удаление TUTOR_CAFEDRA.** Из логов чата (2025-11-13, Babur Rustauletov): запрашивали удаление TUTOR_CAFEDRA — было замечено, что удаление для этого справочника может быть временно отключено на стороне ЕПВО:
   > «TUTOR_CAFEDRA убрали удаление?»

3. **Логическое удаление.** Записи, вероятно, не удаляются физически из БД ЕПВО, а помечаются как неактивные (soft delete). Подтверждение этого поведения требует практического тестирования.

---

## 2. Ключевые решения
1. **POST вместо DELETE:** Фактический HTTP-метод — `POST`. Это расхождение с REST-стандартами, но подтверждено рабочим примером из чата.
2. **Composite key в Body:** Тип композитного ключа передается как `type`, а значение — как именованное поле (полиморфная десериализация, характерная для Spring Boot с `@JsonTypeInfo`).
3. **Документация через Gap Analysis:** В OpenAPI 3.0.1 эндпоинт `/delete` описан минимально. Вся практическая информация извлечена из логов чата разработчиков и участников.

## 3. Acceptance Criteria
- [x] Описан `POST /org-data/{code}/delete`
- [x] Приведён рабочий пример cURL из логов чата
- [x] Составлена таблица маппинга `type` → ID-поле
- [x] Описан теоретический формат ответа

---

*RF — TFW-2.5 / Phase B: OrgData Delete API Documentation | 2026-02-26*
