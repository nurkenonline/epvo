# RF — TFW-12: Transcripts Payload Design

> **Date**: 2026-05-07
> **Author**: Antigravity (Executor)
> **Status**: 🟢 RF — Implementation complete, ready for review

---

## 1. What Was Done
1. `tasks/TFW-12__transcripts_payload/payload_spec.md` — Создан эталонный JSON Payload с описанием типов и обязательности полей для сущности `TRANSCRIPT`.
2. `tasks/TFW-12__transcripts_payload/v_epvo_transcripts.sql` — Написан Vendor-Agnostic шаблон SQL View для инкапсуляции бизнес-логики выгрузки оценок.
3. `TECH_DEBT.md` — Добавлена запись `TD-27` для неучтенной сущности `deletedtranscript` (по требованию координатора/пользователя).

## 2. Key Decisions
- **`ects` как базовое поле:** Согласно указанию пользователя (ответ на вопрос в онбординге), поле `ects` заложено в SQL-шаблон и JSON как базовая колонка для всех записей (не только для ГОП) в целях упрощения пайплайна и унификации контракта.
- **Vendor-Agnostic подход:** SQL-скрипт написан с использованием абстрактных названий таблиц (`abstract_table_marks`, `abstract_table_students`) без привязки к конкретным коммерческим системам (Univer, Platonus и др.). Это гарантирует соблюдение принципов HL.

## 3. Acceptance Criteria
- [x] Файл `payload_spec.md` создан и содержит готовый JSON объект.
- [x] Файл `v_epvo_transcripts.sql` создан и содержит драфт валидного DDL запроса.
- [x] Все обязательные поля из `sur_doc.txt` (Таблица 19) учтены в обоих артефактах.

## 4. Verification
- SQL синтаксис проверен визуально: скрипт содержит валидный DDL `CREATE OR REPLACE VIEW`, который может быть выполнен в любой ANSI SQL СУБД после замены абстрактных таблиц местным DBA.
- JSON-структура полностью сопоставлена с Таблицей 19 из `sur_doc.txt` (проверены типы `integer`, `double`, `boolean`, `string`).

## 5. Observations
No observations.

## 6. Fact Candidates
- **deletedtranscript:** В ЕПВО существует отдельная таблица `deletedtranscript` для транскриптов выпускников и отчисленных студентов, требующая отдельной интеграции (добавлено в техдолг как TD-27).
- **Vendor-Agnostic constraint:** Пользователь строго запретил описывать и ссылаться на структуру реальных коммерческих систем в артефактах. Все шаблоны должны быть универсальными.

## 7. Strategic Insights
- Внедрение абстрактных SQL-интерфейсов (Vendor-Agnostic Views) позволяет разрабатывать единый Python-коннектор к ЕПВО, делегируя маппинг сложной бизнес-логики (например, расчет итоговой оценки и ECTS) владельцам локальных баз данных ВУЗов.

## 8. Diagrams
No diagrams.

---
*RF — TFW-12: Transcripts Payload Design | 2026-05-07*
