# RF — TFW-2.6 / Phase C: Enrollment API Documentation

> **Дата**: 2026-02-26
> **Автор**: ИИ-Агент
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-2__api_endpoints](HL-TFW-2__api_endpoints.md)
> **TS**: [TS-TFW-2__api_endpoints_phase_c](TS-TFW-2__api_endpoints_phase_c.md)

---

## 1. Что сделано

Создана теоретическая документация для API-эндпоинтов слоя **Enrollment** (Приёмные кампании / Списки зачисленных) в ЕПВО.

### Общие заголовки (Headers)
* `Authorization`: Basic Auth (Base64 закодированная строка `username:password`)
* `Content-Type`: `application/json`

---

### 1.1 GET `/grant-enrollment/findAll` (Бакалавриат)

Запрос на получение списка абитуриентов, получивших государственный образовательный грант для обучения в бакалавриате в данном ОВПО.

**Query параметры:**
* `page` (integer, optional): Номер страницы (начиная с 0).
* `size` (integer, optional): Количество элементов на странице.
* `year` (integer, optional): Год приёмной кампании (например, `2025`).
* `universityId` (integer, required): ID университета (маршрутизирует выдачу только для запрашивающего вуза).

**Пример Request:**
```http
GET /grant-enrollment/findAll?year=2025&page=0&size=50&universityId=7 HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Пример Response (200 OK):**
```json
{
  "content": [
    {
      "id": 105432,
      "iin": "050101556677",
      "lastName": "Ахметов",
      "firstName": "Данияр",
      "patronymic": "Серикович",
      "grantType": "Государственный образовательный заказ",
      "professionCode": "B057",
      "professionName": "Информационные технологии",
      "entScore": 115,
      "status": "APPROVED",
      "universityId": 7,
      "createdAt": "2025-08-10T14:30:00Z"
    }
  ],
  "pageable": {
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 50,
    "paged": true
  },
  "totalElements": 1,
  "totalPages": 1,
  "last": true
}
```

> ⚠️ **Предположение:** Точные названия полей (`professionCode`, `entScore`, `grantType`) выведены из стандартных бизнес-практик НЦТ и ЕПВО. Названия полей и самого эндпоинта могут варьироваться (например, `/api/enrollment/bachelor`).

---

### 1.2 GET `/magistracy-enrollment/findAll` (Магистратура)

Запрос на получение списка абитуриентов, поступивших в магистратуру по государственному образовательному гранту.

**Query параметры:**
Те же, что и для бакалавриата (`page`, `size`, `year`, `universityId`).

**Пример Request:**
```http
GET /magistracy-enrollment/findAll?year=2025&page=0&size=50&universityId=7 HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Пример Response (200 OK):**
```json
{
  "content": [
    {
      "id": 204312,
      "iin": "010203554433",
      "lastName": "Оспанова",
      "firstName": "Айгерим",
      "patronymic": null,
      "grantType": "Магистратура грант",
      "professionCode": "M094",
      "professionName": "Информационные технологии (профильное)",
      "ktScore": 120,
      "status": "APPROVED",
      "universityId": 7
    }
  ],
  "pageable": {
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 50,
    "paged": true
  },
  "totalElements": 1,
  "totalPages": 1,
  "last": true
}
```

> ⚠️ **Предположение:** Баллы Комплексного Тестирования могут передаваться в поле `ktScore` или обобщенном поле `score`.

---

## 2. Бизнес-логика (Применение)

Данные эндпоинты предназначены для **чтения**. АИС ОВПО (Платонус/Универ) должна:
1. Вызвать эти эндпоинты по окончании работы приёмной комиссии НЦТ (август).
2. Загрузить списки грантников в локальную базу данных.
3. Инициировать процесс зачисления (создать профили `STUDENT`, назначить `GROUPS` и выпустить приказы `ORDERS`).
4. После издания локального приказа, передать обновленные данные обратно в ЕПВО через `POST /org-data/list/save` (согласно Phase B).

## 3. Acceptance Criteria
- [x] Описан `/grant-enrollment/findAll`
- [x] Описан `/magistracy-enrollment/findAll`
- [x] Приведены структуры JSON-запросов и ответов
- [x] Отражены бизнес-сценарии использования

---

*RF — TFW-2.6 / Phase C: Enrollment API Documentation | 2026-02-26*
