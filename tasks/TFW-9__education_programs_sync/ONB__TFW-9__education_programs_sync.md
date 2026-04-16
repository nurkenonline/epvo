# ONB — TFW-9: Инструкция по синхронизации Реестра образовательных программ

> **Дата**: 2026-04-15
> **Автор**: Executor (AI)
> **Статус**: ✅ ONB — Без блокирующих вопросов

---

## Questions (blocking — cannot proceed without answers)

| # | Question | Answer |
|---|----------|--------|
| — | Нет блокирующих вопросов | — |

## Recommendations (suggestions, not blocking)

1. В RF_TFW-1.2 SPECIALIZATIONS содержит только 10 полей из OpenAPI. adm_doc.txt Таблица 24 содержит 30+ полей. В RF буду использовать adm_doc как авторитетный источник, дополняя OpenAPI-схемой.
2. Обратить внимание на расхождение `professionId` в SPECIALIZATIONS OpenAPI-каталоге (RF_TFW-1.2 показывает прямую FK → Profession) vs adm_doc + чат (через `prof_caf_id → profession_cafedra`). Опишу оба варианта.

## Risks Found

1. `edu_prog_type` / `eduprogtype` — значения 1/2/3 не подтверждены системным справочником (Факт 7 из чата). Пометку ⚠️.
2. Поля `centerProfChecked` / `centerProfessionCode` могут быть deprecated (Факт 3). Отмечу как миграционный риск.

## Inconsistencies with Code (spec vs reality)

1. RF_TFW-1.2 §2 (SPECIALIZATIONS): показывает `professionId` как прямую FK. Но adm_doc Таблица 24 (строка 6117) и чат Бахтияра (2025-09-19) однозначно показывают `prof_caf_id → profession_cafedra.id` как мостовую таблицу. Оба пути будут описаны.

---

*ONB — TFW-9 | 2026-04-15*
