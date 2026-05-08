# TS — TFW-12: Transcripts Payload Design

> **Date**: 2026-05-07
> **Author**: Antigravity (Coordinator)
> **Status**: 🟡 TS_DRAFT — Awaiting approval
> **Parent HL**: [HL-TFW-12](HL__TFW-12__transcripts_payload.md)

---

## 1. Objective
Спроектировать спецификацию JSON Payload для отправки транскриптов в ЕПВО и написать базовый шаблон SQL View `v_epvo_transcripts`, который инкапсулирует логику подготовки данных на стороне БД ИС ОВПО.

## 2. Scope

### In Scope
- Создание эталонного JSON объекта для сущности `TRANSCRIPT` с описанием типов и обязательности полей.
- Написание DDL-скрипта (SQL) для создания представления `v_epvo_transcripts`.

### Out of Scope
- Написание Python-кода (интегратора/синхронизатора).
- Развертывание SQL View в реальной базе данных ВУЗа.
- Упоминание, анализ или описание реальных структур БД коммерческих систем. Вся документация должна быть vendor-agnostic.

## 3. Affected Files

| File | Action | Description |
|------|--------|------------|
| `tasks/TFW-12__transcripts_payload/payload_spec.md` | CREATE | Спецификация JSON Payload для `TRANSCRIPT` |
| `tasks/TFW-12__transcripts_payload/v_epvo_transcripts.sql` | CREATE | Шаблон DDL для SQL View |

**Budget:** 2 new files, 0 modifications.

## 4. Detailed Steps

### Step 1: Создание спецификации Payload
- Создать файл `tasks/TFW-12__transcripts_payload/payload_spec.md`.
- На основе `sur_doc.txt` (Таблица 19 `transcript`) описать JSON структуру.
- Указать обязательные поля: `universityId`, `id`, `studentId`, `subjectCode`, `credits`, `alphaMark`, `numeralMark`, `totalMark`, `subjectNameRu/Kz/En`, `accepted`, `courseNumber`, `term`, `type`, `codeEn/Ru`, `deleted`, `subjectId`, `isGeneralExam`, `isAdditionalSubject`, `isCoursework`, `isSubjectWithAdditionalType`, `notIncludedScholarship`, `wasretaken`.

### Step 2: Создание шаблона SQL View
- Создать файл `tasks/TFW-12__transcripts_payload/v_epvo_transcripts.sql`.
- Написать `CREATE OR REPLACE VIEW v_epvo_transcripts AS SELECT ...`
- В SELECT перечислить все поля, требуемые для Payload.
- Добавить абстрактные SQL-комментарии для местного DBA ВУЗа, поясняющие логику объединения данных, строго без привязки к конкретным системам (использовать общие термины: "таблица студентов", "таблица оценок", "справочник дисциплин").

## 5. Acceptance Criteria

- [ ] Файл `payload_spec.md` создан и содержит готовый JSON объект.
- [ ] Файл `v_epvo_transcripts.sql` создан и содержит драфт валидного DDL запроса.
- [ ] Все обязательные поля из `sur_doc.txt` (Таблица 19) учтены в обоих артефактах.

## 6. Phase Risks

| Risk | Mitigation |
|------|------------|
| Несоответствие типов данных (например, int vs boolean) | Строго следовать форматам из `sur_doc.txt` (Таблица 19). |

---

*TS — TFW-12: Transcripts Payload Design | 2026-05-07*
