# RF — TFW-2.7 / Phase C: File API Documentation

> **Дата**: 2026-02-26
> **Автор**: ИИ-Агент
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-2__api_endpoints](HL-TFW-2__api_endpoints.md)
> **TS**: [TS-TFW-2__api_endpoints_phase_c](TS-TFW-2__api_endpoints_phase_c.md)

---

## 1. Что сделано

Создана теоретическая документация для API-эндпоинтов слоя **File API** в ЕПВО. Эти эндпоинты предназначены для загрузки и чтения прикрепленных файлов (например, электронных документов, приказов, сертификатов об инвалидности, сертификатов ЕНТ и т.д.).

### Общие заголовки (Headers)
* `Authorization`: Basic Auth (Base64 закодированная строка `username:password`)

---

### 1.1 GET `/v1/file/{fileId}` (Скачивание файла)

Метод для получения бинарного содержимого файла, предварительно загруженного в ЕПВО (или сгенерированного платформой).

**Path параметры:**
* `fileId` (string, required): Уникальный идентификатор файла (обычно UUID).

**Пример Request:**
```http
GET /v1/file/123e4567-e89b-12d3-a456-426614174000 HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Пример Response (200 OK):**
```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="order_125_2025.pdf"
Content-Length: 1048576

[Binary file stream...]
```

> **Ошибки:**
> * `404 Not Found` — файл не найден по указанному ID.
> * `403 Forbidden` — отсутствие прав доступа на чтение файла.

---

### 1.2 POST `/v1/file/upload` (Загрузка файла)

Метод загрузки файла в хранилище ЕПВО. После загрузки сервер возвращает уникальный идентификатор файла (`fileId`), который далее можно привязывать к конкретным записям OrgData (например, `student_info.documentId` или `orders.fileId`).

**Заголовки (Headers):**
* `Content-Type`: `multipart/form-data`
* `Authorization`: Basic Auth

**Form-Data параметры:**
* `file` (file, required): Бинарный файл.
* `filename` (string, optional): Оригинальное имя файла.
* `universityId` (integer, required): ID университета, к которому привязывается файл.

**Пример Request:**
```http
POST /v1/file/upload HTTP/1.1
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="universityId"

7
----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="order_125.pdf"
Content-Type: application/pdf

[... binary data ...]
----WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**Пример Response (200 OK):**
```json
{
  "fileId": "123e4567-e89b-12d3-a456-426614174000",
  "fileName": "order_125.pdf",
  "size": 1048576,
  "mimeType": "application/pdf"
}
```

> ⚠️ **Предположение:** ЕПВО использует стандартный Multipart конфигуратор для загрузки файлов. Структура ответа содержит хотя бы `fileId`, необходимый для связей в OrgData таблицах. Названия `/v1/file/upload` или `/api/file/upload` могут варьироваться в зависимости от префиксов (в OpenAPI это описано слабо).

---

## 2. Бизнес-логика связывания файлов

При отправке данных по приказам (`ORDERS`) согласно бизнес-логике gap-анализа, в некоторых случаях к приказу необходимо прикрепить обосновывающий скан документа.
1. ИС ОВПО отправляет файл через `POST /v1/file/upload`.
2. ЕПВО возвращает `fileId`.
3. ИС ОВПО делает массовое сохранение приказа `POST /org-data/list/save`, передавая полученный `fileId` в объекте `typeCode="ORDERS"`.

## 3. Acceptance Criteria
- [x] Описан `GET /v1/file/{fileId}`
- [x] Описан `POST /v1/file/upload`
- [x] Приведены структуры HTTP/JSON-запросов и ответов
- [x] Отражены бизнес-сценарии использования (например, для приказов)

---

*RF — TFW-2.7 / Phase C: File API Documentation | 2026-02-26*
