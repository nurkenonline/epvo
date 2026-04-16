# RF — TFW-10 / Phase 1: Разрешение технического долга по Реестру ОП

> **Дата**: 2026-04-15
> **Автор**: Executor (AI)
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-10](HL-TFW-10__resolve_education_programs_tech_debt.md)
> **TS**: [TS-TFW-10](TS__TFW-10__resolve_education_programs_tech_debt.md)

---

## 1. Что сделано

### Новые файлы
| Файл | Описание |
|------|----------|
| `tasks/TFW-10.../RF__TFW-10...md` | Данный отчет о результатах выполнения задачи. |
| `tasks/TFW-10.../ONB__TFW-10...md` | Документ онбординга исполнителя (Trace-First). |

### Изменённые файлы
| Файл | Изменения |
|------|----------|
| `tasks/TFW-1/RF_TFW-1.2__education_programs.md` | Матрица `SPECIALIZATIONS` расширена (30+ полей), исправлено `professionId` -> `prof_caf_id`, обновлен Mermaid-граф. |
| `tasks/TFW-4/RF_TFW-4.B__admissions_registries.md` | Добавлены `[!WARNING]` о семантике `duration`, уточнен `typeCode = SPECIALIZATIONS`. |
| `KNOWLEDGE.md` | Добавлен раздел §2.21 (Архитектура ОП, JOIN-путь, Full Replace, НЦРВО). |
| `TECH_DEBT.md` | Пункты TD-21 — TD-25 переведены в статус `✅ Resolved (TFW-10)`. |
| `README.md` | Обновлен статус TFW-10 до 🟢 RF. |

## 2. Ключевые решения

1. **Мостовая связь**: Решено вынести описание JOIN-пути (`SPECIALIZATIONS -> PROFESSION_CAFEDRA -> PROFESSION`) в базу знаний как критически важный архитектурный инсайт для избежания 500 ошибок (TD-22).
2. **Семантическая инспекция**: Добавлено предупреждение о различии шкал времени (семестры vs месяцы) в разных эндпоинтах, так как это скрытый источник багов при автоматизации (TD-23).
3. **Full Replace Rule**: Включено напоминание о специфике `/save`, так как для справочников ОП это особенно критично из-за большого количества необязательных полей.

## 3. Acceptance Criteria (DoD)

- [x] В `RF_TFW-1.2` секция `SPECIALIZATIONS` имеет 30+ полей, а граф учитывает `PROFESSION_CAFEDRA`. (TD-21, TD-22)
- [x] В `RF_TFW-4.B` присутствуют предупреждения о единицах измерения и typeCode `SPECIALIZATIONS`. (TD-23, TD-25)
- [x] В `KNOWLEDGE.md` появился новый подпункт §2.21, описывающий логику ОП. (TD-24)
- [x] Статусы 5 пунктов долга в `TECH_DEBT.md` изменены на `✅ Resolved (TFW-10)`.
- [x] Написан `RF__TFW-10__resolve_education_programs_tech_debt.md` по шаблону TFW v3.

## 4. Верификация

- Lint: N/A (Documentation only)
- Tests: N/A
- Verify: Визуальная проверка Mermaid-графа и разметки таблиц — ОК. Все ссылки в `KNOWLEDGE.md` верифицированы по чатам техподдержки.

## 5. Observations (out-of-scope, not modified)

| # | File | Line(s) | Type | Description |
|---|------|---------|------|-------------|
| 1 | `RF_TFW-1.2` | 286 | todo | Раздел "Поля с неясным описанием" пуст, но фактически OpenAPI v3 всё еще "неясна" в части ОП. |
| 2 | `TECH_DEBT.md` | 1-24 | naming | Остальные пункты техдолга (TD-1 - TD-20) используют старый формат `→ backlog` вместо `→ backlog (TFW-x)`. |

---

*RF — TFW-10 / Phase 1: Разрешение технического долга по Реестру ОП | 2026-04-15*
