# TASK — EPVO API Research & Integration

## Scope

Исследование API ЕПВО (Единой Платформы Высшего Образования) для понимания механизмов передачи данных и подключения различных информационных систем вузов.

## Boundaries

### In Scope
- ✅ Документирование всех API-эндпоинтов ЕПВО (OrgData, CommonDictionary, Enrollment)
- ✅ Каталогизация ~90+ справочников организационных данных с JSON-схемами
- Создание универсальных маппингов данных для типичных АИС

### Out of Scope (for now)
- Разработка инструментов и скриптов (Python/TypeScript) для интеграции
- Практическое тестирование API-эндпоинтов на сервере ЕПВО
- Интеграция с конкретной АИС (esuvoapi, Univer, и т.д.)
- Автоматический scheduled sync
- UI/dashboard
- Deployment в продакшн

## Key Entities (OrgDataDictionaryCode)

Priority entities for research:

| Priority | Code | Description |
|----------|------|-------------|
| High | FACULTIES | Факультеты |
| High | CAFEDRA | Кафедры |
| High | STUDENT | Обучающиеся |
| High | STUDENT_INFO | Информация об обучающихся |
| High | TUTOR | Преподаватели (ППС) |
| High | PROFESSION | Специальности/ОП |
| High | GROUPS | Академические группы |
| Medium | ORDERS | Приказы |
| Medium | TRANSCRIPT | Транскрипты |
| Medium | GRADUATES | Выпускники |
| Medium | TUTOR_CAFEDRA | Преподаватель-кафедра связь |
| Low | BUILDINGS | Корпуса |
| Low | DORMITORY | Общежития |

## Definition of Done (DoD)

1. ✅ Все API-эндпоинты (OrgData, CommonDictionary) задокументированы теоретически
2. ✅ JSON-схемы всех ключевых справочников описаны (TFW-1 complete)
3. ✅ Универсальный маппинг-гайд создан для подключения новых ИС
4. ✅ Системные справочники (CommonDictionary) каталогизированы

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| EPVO API changes without notice | High | Pin OpenAPI spec version; monitor `/v3/api-docs` |
| Authentication mechanism unclear | High | Document theoretical process based on standard Basic Auth |
| No sandbox/test environment | High | Focus strictly on reading specs and theoretical mapping |
| Composite key complexity | Medium | Document per-entity composite key rules |

## Open Questions (Resolved during TFW-2)

1. ~~**Batch size limits**: Максимальный размер batch для `/org-data/list/save`?~~ — *(Теоретически не ограничено жестко, используется стандартный Spring Boot list binding, но на практике лучше отправлять пакетами).*
2. ~~**Error handling**: Как ЕПВО обрабатывает частичные ошибки в batch?~~ — *(Возвращает 200 OK со структурой `failedRecords` внутри тела, описывающей какие конкретно объекты не прошли валидацию).*
3. ~~**ID management**: Кто управляет ID сущностей — вуз или ЕПВО?~~ — *(Управляет ВУЗ. Формируется композитный ключ (например `STUDENT_ID_COMPOSITE_KEY`) с передачей локального ID вуза).*
4. ~~**File upload**: Как загружать файлы (приказы, документы)?~~ — *(Через `POST /v1/file/upload` `multipart/form-data`, получая в ответ `fileId` для привязки к OrgData).*
5. **Трёхъязычность**: Стратегия для полей `nameRu/nameKz/nameEn` при отсутствии данных? — Ожидает решения.

## Technical Notes

- EPVO API is OpenAPI 3.0.1, Spring Boot backend
- Entities use discriminator-based polymorphism (`typeCode` for entity type, `type` for primary keys)
- Composite keys vary by entity (e.g., `CAFEDRA_ID_COMPOSITE_KEY`, `STUDENT_ID_COMPOSITE_KEY`)
- System dictionaries (`/common-dictionary/`) are read-only reference data
- Auth: Basic Auth, credentials via env vars
- universityId required for OrgData requests
