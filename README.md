# ЕПВО — Исследование API для интеграции информационных систем (epvo)

Документация для ИИ по интеграции ИС ОВПО с ЕПВО МНВО РК

## Назначение

Исследование API **Единой Платформы Высшего Образования (ЕПВО)** для подключения различных информационных систем вузов и миграции их данных в ЕПВО.

ЕПВО разработана компанией **Platonus** и предоставляет REST API для приёма данных от вузов. Данный проект направлен на глубокое понимание API, документирование его возможностей и создание универсальных инструментов интеграции.

## Проблема

Вузы Казахстана обязаны передавать актуальные данные (факультеты, кафедры, студенты, преподаватели, учебные планы, приказы и др.) в ЕПВО. Для этого необходимо:
- Понять OpenAPI-спецификацию ЕПВО (`https://epvo.kz/isvuz/api`)
- Документировать все эндпоинты, справочники и механизмы
- Создать универсальные маппинги данных (без написания кода интеграции)

## Основные API-операции ЕПВО

| Метод | Эндпоинт | Назначение |
|-------|----------|------------|
| GET | `/org-data/find-all-pageable` | Чтение записей справочника (пагинация, `?category=...`) |
| GET | `/org-data/find-by-id` | Поиск записи по ID (`?id=...`) |
| POST | `/org-data/list/save` | Массовое создание/обновление записей (UPSERT) |
| POST | `/org-data/{code}/delete` | Логическое удаление записи по композитному ключу (через Body) |
| GET | `/common-dictionary/find-all` | Системные справочники (`?category=...`) |

> **Внимание (Gap Analysis):** OpenAPI-спецификация ЕПВО описывает лишь базовые CRUD-операции. Реальная же бизнес-логика (например, маппинг 60+ структур контингента, стипендий, СУР) не документирована в OpenAPI и требует сложных внутренних трансформаций (Сверка/Reconciliation), описанных в исторических инструкциях по интеграции (АдмОтчеты, модули Финансирования).

## Справочники организационных данных (OrgDataDictionaryCode)

Полный перечень: FACULTIES, CAFEDRA, STUDENT, STUDENT_INFO, STUDENT_DIPLOMA_INFO, TUTOR, TUTOR_CAFEDRA, PROFESSION, GROUPS, ORDERS, TRANSCRIPT, GRADUATES и ещё ~80 справочников (см. RF-файлы в `tasks/TFW-1__entity_catalog/`).

## Быстрый старт

1. Прочитать `AGENTS.md` → `STEPS.md` → `TASK.md`
2. Прочитать `.tfw/conventions.md` и `.tfw/glossary.md`
3. Изучить RF-файлы каталога сущностей в `tasks/TFW-1__entity_catalog/`
4. Начать с планирования задачи через `.tfw/workflows/plan.md`

## Методология

Проект ведётся по **Trace-First Workflow (TFW v3)**:
- Все решения фиксируются в трассируемых артефактах
- Каждый ответ агента заканчивается строкой Summary
- Артефакты: `HL__` (контекст), `TS__` (задачи), `ONB__` (онбординг), `RF__` (результаты), `REVIEW__` (ревью)
- Прогресс: `STEPS.md`
- Технический долг: `TECH_DEBT.md`
- Ядро TFW: `.tfw/` (конвенции, шаблоны, workflow)

## Структура проекта

```
ЕПВО/
├── AGENTS.md           # Правила ИИ-агента
├── AI_ENTRY_POINT.md   # Протокол инициации
├── README.md           # Этот файл
├── TASK.md             # Границы, DoD, риски
├── STEPS.md            # Журнал прогресса
├── TECH_DEBT.md        # Реестр технического долга
├── .tfw/               # Ядро TFW v3 (tool-agnostic)
│   ├── README.md       # Философия TFW
│   ├── conventions.md  # Конвенции
│   ├── glossary.md     # Глоссарий
│   ├── PROJECT_CONFIG.yaml
│   ├── templates/      # HL, TS, RF, ONB, REVIEW шаблоны
│   ├── workflows/      # plan, handoff, resume
│   └── adapters/       # Адаптеры для IDE
├── .agent/             # Antigravity адаптер
│   ├── rules/tfw.md
│   └── workflows/      # tfw-plan, tfw-handoff, tfw-resume
├── tasks/              # Артефакты задач
│   ├── TFW-1__entity_catalog/
│   ├── TFW-2__api_endpoints/
│   ├── TFW-4__gap_decomposition/
│   └── HL__open_questions.md
└── init/               # Исходные файлы методологии TFW
```

## Task Board

| ID | Task | Status | HL | TS | ONB | RF | REV |
|----|------|--------|----|----| --- |----| --- |
| TFW-1 | Entity Catalog (90 entities) | ✅ DONE | ✅ | ✅ | — | ✅ | — |
| TFW-2 | API Endpoint Documentation | ✅ DONE | ✅ | ✅ | ✅ | ✅ | — |
| TFW-4 | Gap Analysis Decomposition & esuvoapi Code Analysis | 🔵 HL | 🔵 | — | — | — | — |

> Statuses: ⬜ TODO → 🔵 HL → 🟡 TS → 🟠 ONB → 🟢 RF → 🔍 REV → ✅ DONE | ❌ BLOCKED

## Безопасность

- Секреты только через переменные окружения
- Логирование всех API-вызовов
- Локальное исполнение по умолчанию

