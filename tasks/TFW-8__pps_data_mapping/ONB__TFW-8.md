# ONB — TFW-8: Маппинг данных ППС для ЕПВО

> **Дата**: 2026-03-18
> **Исполнитель**: Executor (AI)
> **Статус**: ✅ Онбординг завершён

---

## Questions (blocking — cannot proceed without answers)

| # | Question | Answer |
|---|----------|--------|
| — | Нет блокирующих вопросов | — |

## Recommendations

1. **TS scope расширен**: PDF-инструкция «Адм. отчёты» (011025) содержит значительно больше полей для TUTOR и TUTOR_CAFEDRA, чем OpenAPI spec и TS предполагали. RF будет включать все обнаруженные поля.
2. **Два поля `main_place_of_work`**: В Table 5 (tutors) есть `main_place_of_work` (1/2/3), а в Table 6 (tutor_cafedra) — `primaryEmploymentID` (1/2/3). Оба описывают основное место работы с одинаковыми значениями. Вероятно, разные уровни (преподаватель vs запись по кафедре).

## Risks Found

1. **Поле `ftutor` имеет condition-lock**: PDF указывает `ftutor=true` ТОЛЬКО когда `tutor_cafedra.type=2 AND primaryEmploymentID=1` (не 2!). Это **contradicts** чат (30.04.2025, Айдар: `primaryEmploymentID=2` для зарубежного). Расхождение в версиях инструкций — требует верификации.
2. **Поле `liveRegType`**: Условие в PDF — `tutor_cafedra.type=2` (внешний совместитель). Скорее всего опечатка в PDF, должно быть `type=0` (штатный) с иностранным гражданством.

## Inconsistencies with Code (spec vs reality)

1. RF_TFW-1.5 документирует ~15 полей TUTOR, а PDF instruction содержит ~45 полей.
2. RF_TFW-1.5 документирует ~10 полей TUTOR_CAFEDRA, а PDF содержит ~20 полей.
3. `tutors.deleted` упомянуто в PDF как отдельное поле (`tutors.deleted = 0`), тогда как ранее считалось что это `tutor_cafedra.deleted`.

---

*ONB — TFW-8 | 2026-03-18*
