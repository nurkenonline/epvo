# REVIEW — TFW-8: Маппинг данных ППС для ЕПВО

> **Дата**: 2026-03-18
> **Автор**: Reviewer (AI)
> **Verdict**: ✅ APPROVE
> **RF**: [RF_TFW-8__pps_data_mapping](RF_TFW-8__pps_data_mapping.md)
> **TS**: [TS__TFW-8__pps_data_mapping](TS__TFW-8__pps_data_mapping.md)

---

## 1. Review Checklist

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | DoD met? (all TS acceptance criteria) | ✅ | Все 7 критериев выполнены, детали ниже |
| 2 | Code quality (conventions, naming) | ✅ | Документ. задача — формат RF соответствует проекту (аналог RF_TFW-1.5/1.7) |
| 3 | Test coverage | N/A | Документационная задача, тестов нет |
| 4 | Philosophy aligned (matches HL) | ✅ | HL указывал «Полнота > детализация», RF следует этому принципу |
| 5 | Tech debt (shortcuts documented?) | ✅ | 2 элемента (см. § 3) |
| 6 | Security | N/A | Нет кода, нет секретов |
| 7 | Breaking changes | N/A | Нет кода |
| 8 | Style & standards | ✅ | Markdown-таблицы, JSON-примеры, mermaid-графы |
| 9 | Observations collected | ✅ | ONB содержит 2 risks, 3 inconsistencies |

### DoD — детальная верификация

| TS Criterion | Status | Evidence |
|-------------|--------|----------|
| RF содержит маппинг для 9 сущностей (OpenAPI + скрытые) | ✅ | §1–9: TUTOR (45+ полей), TUTOR_CAFEDRA (20+ полей), 7 дочерних |
| Бизнес-логика СУР (4 OR-блока) | ✅ | §11.2: BLOCK 1–4 с SQL-like псевдокодом |
| Значения `type`, `primaryEmploymentID` с источниками | ✅ | §2.1: type 0/1/2; §2.2: primaryEmploymentID 1/2/3 + чат+PDF |
| Sequencing Contract | ✅ | §10: 7 шагов + mermaid-граф + таблица зависимостей |
| JSON-примеры TUTOR и TUTOR_CAFEDRA | ✅ | §1.9 и §2.5 с реальными данными из чата |
| Gotchas (≥5) с источниками | ✅ | §12: 8 gotchas со ссылками на чат (даты, авторы) |
| Данные из PDF-инструкций | ✅ | §11.3–11.5: ВП-4, ВП-34, ВП-35; §7: Table 7 (tutorqual) из PDF |

### Сверхплановые элементы (executor discovery)

RF значительно превышает scope TS:
- 30+ полей из PDF Адм. отчётов, не упомянутых в TS (registration, Scopus/WoS, CATO кОды, f-блок)
- 3 дополнительных бизнес-правила из PDF (ВП-4, ВП-34, ВП-35)
- `TUTOR_QUALIFICATION` дополнена полной схемой из PDF Table 7 (18 полей vs ~5 в OpenAPI)

## 2. Verdict

**✅ APPROVE**

RF является исчерпывающей спецификацией данных ППС для ЕПВО. Все критерии TS выполнены, документ структурирован по разделам, содержит JSON-примеры, mermaid-графы, и 8 задокументированных gotchas. Особенно ценен §11 (бизнес-логика фильтрации) — ранее нигде не документировалось.

## 3. Tech Debt Collected

| # | Source | Severity | Description | Action |
|---|--------|----------|-------------|--------|
| 1 | ONB Risk #1 | Medium | `ftutor` condition: PDF says `primaryEmploymentID=1`, chat says `=2` для зарубежного. RF пометил ⚠️ «требует верификации» | → Верифицировать через тестовый UPSERT |
| 2 | ONB Risk #2 | Low | `liveRegType` condition в PDF вероятно опечатка (`type=2` вместо `type=0`) | → Уточнить в чате ЕПВО |
| 3 | ONB Inconsistency | Low | `tutors.deleted` vs `tutor_cafedra.deleted` — оба поля существуют, но разные контексты | → Документировать в KNOWLEDGE.md |
| 4 | RF §6 | Low | `TUTOR_PUBLICATION` composite key не подтверждён (`PUB_ID` или `UNIVERSITY_ID`) | → Верифицировать через API |

## 4. Traces Updated

- [x] README Task Board — status → ✅ DONE
- [x] HL status — обновлён
- [ ] TECH_DEBT.md — добавить 4 элемента (ниже)
- [ ] KNOWLEDGE.md — добавить секцию TUTOR (→ /tfw-docs)

---

*REVIEW — TFW-8: Маппинг данных ППС для ЕПВО | 2026-03-18*
