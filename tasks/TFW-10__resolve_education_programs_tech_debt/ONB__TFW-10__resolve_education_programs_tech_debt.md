# ONB — TFW-10 / Phase 1: Разрешение технического долга по Реестру ОП

> **Дата**: 2026-04-15
> **Автор**: Coordinator (AI) / Executor (AI)
> **Статус**: ✅ ONB — Исполнение начато
> **Parent HL**: [HL-TFW-10](HL-TFW-10__resolve_education_programs_tech_debt.md)
> **TS**: [TS-TFW-10](TS__TFW-10__resolve_education_programs_tech_debt.md)

---

## 1. Understanding (как понял задачу)
Задача заключается в устранении пяти пунктов технического долга (TD-21 — TD-25), накопленных в ходе TFW-9. Требуется внести исправления в каталог сущностей (`RF_TFW-1.2`), анализ гэпов (`RF_TFW-4.B`), базу знаний (`KNOWLEDGE.md`) и реестр техдолга (`TECH_DEBT.md`). Работа носит исключительно документарный характер (без изменения кода).

## 2. Entry Points (откуда начинать)
- `tasks/TFW-1__entity_catalog/RF_TFW-1.2__education_programs.md` — исправление структуры ОП.
- `tasks/TFW-4__gap_decomposition/RF_TFW-4.B__admissions_registries.md` — уточнение бизнес-правил и имен.
- `KNOWLEDGE.md` — добавление архитектурной секции.
- `TECH_DEBT.md` — закрытие тикетов.

## 3. Questions (blocking — cannot proceed without answers)

| # | Question | Answer |
|---|----------|--------|
| 1 | Подтверждаем ли мы использование секции 2.21 в KNOWLEDGE.md? | Да, так как 2.1-2.20 уже заняты. |

## 4. Recommendations (suggestions, not blocking)
1. Включить в RF подтверждение того, что Mermaid-граф успешно рендерится после добавления новых связей.

## 5. Risks Found (edge cases, potential issues not in TS)
1. **Divergence**: OpenAPI спецификация ЕПВО (Swagger) всё еще дезинформирует разработчиков про `professionId`. Риск того, что внешние разработчики проигнорируют нашу базу знаний и будут следовать Swagger.

## 6. Inconsistencies with Code (spec vs reality)
1. TS указывает на `prof_caf_id` как на единственный рабочий путь, в то время как YAML/OpenAPI spec от Platonus продолжает утверждать обратное.

---

*ONB — TFW-10 / Phase 1: Разрешение технического долга по Реестру ОП | 2026-04-15*
