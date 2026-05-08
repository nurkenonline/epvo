# ONB — TFW-12: Transcripts Payload Design

> **Date**: 2026-05-07
> **Author**: Antigravity (Executor)
> **Status**: 🟠 ONB — Onboarding complete, ready for execution

---

## 1. Questions (blocking — cannot proceed without answers)

| # | Question | Answer |
|---|----------|--------|
| 1 | В `sur_doc.txt` упоминается таблица `deletedtranscript` для выпускников и отчисленных. Должны ли мы в этой задаче описать JSON Payload и для `deletedtranscript`, или ограничиваемся только базовым `TRANSCRIPT`? | ограничеваемся базовым `TRANSCRIPT` |
| 2 | В таблице 19 поле `ects` указано как обязательное только для ГОП. Стоит ли нам заложить логику расчета (или вывода) `ects` в `v_epvo_transcripts` как базовую колонку для всех? | да|

## 2. Recommendations (suggestions, not blocking)
1. **Служебное поле валидации:** Предлагаю добавить в контракт SQL View `v_epvo_transcripts` дополнительную колонку `is_ready_for_epvo` (логическое выражение), которая на уровне БД будет проверять, не равны ли NULL обязательные текстовые поля (`subjectName*`, `subjectCode`). Это позволит Python-скрипту легко фильтровать "битые" оценки до отправки.

## 3. Risks Found (edge cases, potential issues not in TS)
1. **Формат булевых полей:** API ЕПВО иногда принимает `1/0`, а иногда `true/false`. Для транскриптов флаги `isPassed`, `deleted`, `notIncludedScholarship` и др. в OpenAPI обычно описаны как `boolean`. В спецификации мы строго зафиксируем тип `boolean`, но в SQL это часто `tinyint(1)`. DBA должен будет учесть приведение типов.

## 4. Inconsistencies with Code (spec vs reality)
1. Несоответствий нет, так как мы разрабатываем контракт с нуля (vendor-agnostic).

## 7. Knowledge Citations Review

| # | Source | Item | Confirmation |
|---|--------|------|--------------|
| 1 | `TECH_DEBT.md` | TD-1 | Ознакомлен. Создание View разрешает этот долг до написания кода. |
| 2 | `RF_TFW-4.C` | §3.1 | Ознакомлен. Структура View будет базироваться на этом документе. |
| 3 | `sur_doc.txt` | Таблица 19 | Ознакомлен. Будет использовано как эталон для JSON спецификации. |

---

*ONB — TFW-12: Transcripts Payload Design | 2026-05-07*
