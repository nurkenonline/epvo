# TS — TFW-2 / Phase B: OrgData Save & Delete Endpoints

> **Дата**: 2026-02-26
> **Автор**: ИИ-Агент
> **Статус**: 🟢 TS — Утверждён
> **Parent HL**: [HL-TFW-2__api_endpoints](HL-TFW-2__api_endpoints.md)

---

## 1. Цель
Задокументировать методы записи в слой OrgData ЕПВО: массовое сохранение (UPSERT) через `/list/save` и удаление записей через `/delete`. Описать структуру ответов от сервера, включая обработку ошибок (`failedRecords`).

## 2. Scope

### In Scope
- Документирование эндпоинта массового сохранения: `POST /org-data/list/save`.
- **ВАЖНО**: По данным логов чата от поддержки ЕПВО, следует использовать именно `POST /org-data/list/save` и передавать массив DTO, так как одиночный `/save` возвращает 404/Not Found или 400 Bad Request.
- Детальный разбор структуры ответа от `/list/save`: параметры `requestedElements`, `savedElements`, `updatedElements`, `failedElementsCcount` и массив `failedRecords`.
- Документирование эндпоинта логического удаления: `POST /org-data/{code}/delete`.
- **ВАЖНО**: Из логов чата получен точный, недокументированный в OpenAPI пример рабочего запроса на удаление. Он отправляется методом `POST` (в виде cURL), а не `DELETE`, и требует передачи `type` (композитного ключа) и `id` (например, `studentId`) в теле запроса (Body).
- Теоретическое описание поведения UPSERT (по какому ключу система решает обновлять или создавать).

### Out of Scope
- Практическое тестирование сохранения (нет доступа к тестовому контуру).
- Написание скриптов миграции (это следующие задачи).
- Эндпоинты Enrollment и File API (Phase C).

## 3. Затрагиваемые файлы

| Файл | Действие | Описание |
|------|----------|----------|
| `tasks/TFW-2__api_endpoints/RF_TFW-2.4__orgdata_save_api.md` | CREATE | Документация массового сохранения `/save` и обработки ошибок |
| `tasks/TFW-2__api_endpoints/RF_TFW-2.5__orgdata_delete_api.md` | CREATE | Документация эндпоинта `/delete` |

**Бюджет:** 2 новых файла.

## 4. Детальные шаги

### Step 1: Проектирование RF_TFW-2.4__orgdata_save_api.md
* Описать `POST /org-data/list/save?category=...&universityId=...`.
* Привести пример Request Body — массив объектов (например, факультетов или студентов).
* Привести подробный пример Response оборачиваемого в объект метаданных (подробно разобрать структуру `FailedRecordsList`).
* Объяснить, как работает UPSERT на базе композитных ключей (описанных в TFW-1).

### Step 2: Проектирование RF_TFW-2.5__orgdata_delete_api.md
* Описать `POST /org-data/{code}/delete`.
* Использовать точный рабочий пример из логов чата (от 14 января 2026 г.):
  `curl --location 'https://epvo.kz/isvuz/api/org-data/STUDENT_BENEFIT/delete' --header 'Content-Type: application/json' --header 'Authorization: Basic УДАЛЕНО' --data '{ "type": "STUDENT_ID_COMPOSITE_KEY", "studentId": 704950 }'`
* Обратить внимание, что удаление требует передачи названия композитного ключа в параметре `type` (например, `STUDENT_ID_COMPOSITE_KEY`).
* Привести формат ожидаемого отклика сервера.

## 5. Acceptance Criteria

- [ ] Создан файл `RF_TFW-2.4__orgdata_save_api.md` с описанием `/list/save` и механизма обработки `failedRecords`.
- [ ] Создан файл `RF_TFW-2.5__orgdata_delete_api.md` с описанием `/delete`.
- [ ] Приведены примеры JSON-запросов и ответов для обоих методов.

## 6. Риски фазы

| Риск | Mitigation |
|------|------------|
| Неполнота информации об UPSERT механизмах | В TFW-1 мы задокументировали композитные ключи. В RF нужно будет явно указать, что ЕПВО обновляет запись при совпадении primary_key полей, иначе создает новую. |
| Точный формат ответа `/delete` неизвестен из OpenAPI | Описать теоретический стандартный ответ REST API (обычно 200 OK без тела или с boolean флагом), пометитив как Предположение, но опираться на найденный пример запроса `POST`. |

---

*TS — TFW-2 / Phase B: OrgData Save & Delete Endpoints | 2026-02-26*
