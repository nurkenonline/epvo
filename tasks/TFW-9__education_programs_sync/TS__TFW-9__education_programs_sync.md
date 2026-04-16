# TS — TFW-9: Инструкция по синхронизации Реестра образовательных программ

> **Дата**: 2026-04-15
> **Автор**: Coordinator (AI)
> **Статус**: ✅ TS — Утверждён
> **Parent HL**: [HL-TFW-9__education_programs_sync](HL-TFW-9__education_programs_sync.md)

---

## 1. Цель

Создать исчерпывающий RF-документ, описывающий бизнес-логику передачи данных Реестра образовательных программ (ОП) в ЕПВО. Документ предназначен для интеграторов **любой** ИС ОВПО и должен быть самодостаточным — содержать полный маппинг полей, sequencing contract, lookup-алгоритмы и gotchas.

## 2. Scope

### In Scope
- Полный маппинг полей для `PROFESSION` (ГОП) — источник: adm_doc.txt Таблица 3 (строки 1797–1886) + OpenAPI (RF_TFW-1.2 §1)
- Полный маппинг полей для `SPECIALIZATIONS` (ОП) — источник: adm_doc.txt Таблица 24 (строки 6095–6501) + OpenAPI (RF_TFW-1.2 §2)
- Маппинг `PROFESSION_CAFEDRA` — OpenAPI (RF_TFW-1.2 §3)
- Маппинг `STUDYFORMS` — adm_doc.txt Таблица 4 (строки 1887–1999)
- Sequencing Contract (порядок UPSERT с учётом FK)
- Lookup-алгоритм для `CenterProfession` через системный справочник (RF_TFW-1.14)
- Правило `classifier` (1 = Специальности, 2 = ГОП) из adm_doc.txt
- Правило `code` vs `professionCode` (два разных поля) из adm_doc.txt
- Правило `specializationCode` для ОП (формат: код + порядковый номер) из adm_doc.txt строки 6224–6247
- Обработка old-style кодов (`5B...`) vs new-style (`6B...`, `7M...`, `8D...`)
- JSON-примеры полных пайлоадов (PROFESSION, SPECIALIZATIONS)
- ≥5 Gotchas с источниками

### Out of Scope
- `PROFESSION_COST`, `TYP_CURRICULUM`, `Q_EXAMINATIONS`, `EDUCATION_PROGRAMS_CODE` — описать только в виде краткой таблицы (поля + composite key) без бизнес-логики
- Код интеграции (Python/Java)
- Специфика конкретного ВУЗа
- Модуль «Подача заявок» (APPLICATIONS)

## 3. Затрагиваемые файлы

| Файл | Действие | Описание |
|------|----------|----------|
| `RF__TFW-9__education_programs_sync.md` | CREATE | Основной RF-документ с маппингом, sequencing, gotchas |

**Бюджет:** 1 новый файл, 0 модификаций. ≤1 файл, ≤1 новый.

## 4. Детальные шаги

### Step 1: Структура RF

RF следует стандартной структуре (аналог RF_TFW-5, RF_TFW-6, RF_TFW-8):

```markdown
§1. PROFESSION (ГОП) — полный маппинг
  §1.1 Composite Key
  §1.2 Матрица полей (adm_doc + OpenAPI)
  §1.3 Бизнес-правила: classifier, code, professionCode
  §1.4 JSON-пример
§2. SPECIALIZATIONS (ОП) — полный маппинг
  §2.1 Composite Key
  §2.2 Матрица полей (adm_doc + OpenAPI)
  §2.3 Бизнес-правила: prof_caf_id, specializationCode, statusep, eduprogtype
  §2.4 Совместные ОП (jointep, doublediploma, universitytype, partneruniverid)
  §2.5 JSON-пример
§3. PROFESSION_CAFEDRA — краткий маппинг
§4. STUDYFORMS — краткий маппинг
§5. Вспомогательные сущности (PROFESSION_COST, TYP_CURRICULUM, Q_EXAMINATIONS, EDUCATION_PROGRAMS_CODE) — табличный обзор
§6. Sequencing Contract
  §6.1 Порядок UPSERT (граф зависимостей)
  §6.2 Правила: что сначала, что потом
§7. Lookup: CenterProfession
  §7.1 Эндпоинт системного справочника
  §7.2 Алгоритм сопоставления по коду
  §7.3 Обработка старых кодов (5B... → 6B...)
§8. Gotchas
§9. Acceptance Criteria
§10. Observations (out-of-scope)
```

### Step 2: Источники данных для Executor

Executor должен свести данные из следующих источников:

| Источник | Что извлечь | Строки |
|----------|-------------|--------|
| `adm_doc.txt` Таблица 3 | Поля `professions`: `professionid`, `classifier`, `professioncode`, `code`, `deleted` | 1797–1886 |
| `adm_doc.txt` Таблица 4 | Поля `studyforms`: `degreeId`, `courseCount`, `creditsCount`, `termsCount`, `departmentId` | 1887–1999 |
| `adm_doc.txt` Таблица 24 | Поля `specializations`: ~30 полей включая `prof_caf_id`, `specializationcode`, `statusep`, `eduprogtype`, `is_interdisciplinary`, `doublediploma`, `jointep` и др. | 6095–6501 |
| RF_TFW-1.2 | OpenAPI-схема: `PROFESSION` (15 полей), `SPECIALIZATIONS` (10 полей), `PROFESSION_CAFEDRA`, `PROFESSION_COST`, `TYP_CURRICULUM`, `Q_EXAMINATIONS`, `EDUCATION_PROGRAMS_CODE` | Весь файл |
| RF_TFW-1.14 | Системный справочник `CenterProfession` — структура, endpoint | Строка 44 |
| RF_TFW-4.B | Существующие 2 бизнес-правила (duration, professionCode) + risk со старыми кодами | Весь файл |
| RF_TFW-6 §4.3 | Правило `ГОП vs CenterProfessionCode` (professionId ↔ centerProfessionCode) | Строки 250–260 |
| KNOWLEDGE.md §1.1 | Механизм UPSERT (Full Replace) | Строки 7–12 |
| KNOWLEDGE.md §1.2 | Composite Keys: `professionId` для PROFESSION | Строка 21 |
| KNOWLEDGE.md §1.6 | Naming Traps | Строки 54–62 |
| **Чат ЕПВО (Telegram)** | Инсайты по ОП/ГОП из обсуждений с Бахтияром/Айдаром (2023–2026) | См. Step 3.5 ниже |

### Step 3.5: Инсайты из чата ЕПВО (для Executor)

Executor должен включить в RF следующие подтверждённые факты из чата техподдержки:

**Факт 1 (Связь SPECIALIZATIONS → PROFESSION):**
Бахтияр (2025-09-19) подтвердил JOIN-путь:
```sql
specializations.prof_caf_id → profession_cafedra.id → professions.professionid
```
ОП привязывается к ГОП **через промежуточную таблицу** `profession_cafedra`, а НЕ напрямую.

**Факт 2 (professionId в SPECIALIZATIONS ≠ CENTER_PROFESSION):**
Dinara (2023-10-30): передача `professionId=1993` (ID из CENTER_PROFESSION) → 500 ошибка.
→ `professionId` в SPECIALIZATIONS ссылается на **локальную** таблицу `professions`, не на центральный справочник.

**Факт 3 (centerProfChecked/centerProfessionCode → миграция на professionId):**
Dark Moon (2025-09-12): «с таблицы graduates убрали centerProfChecked и centerProfessionCode?»
Бахтияр (2025-08-29): «если centerProfChecked=true стоит, centerProfessionCode обязателен»
→ ЕПВО мигрирует с `centerProfessionCode` на `professionId`. В GRADUATES теперь используется `professionId`.

**Факт 4 (ignore_rms для СУР):**
Айдар (2025-10-09): «specializations таблица, поле ignore_rms» — исключает ОП из расчёта показателей СУР.

**Факт 5 (description длина):**
Бахтияр (2023-11-17): поля `descriptionRu/Kz/En` в specializations → `varchar(4096)`.

**Факт 6 (forOop, trainingForOop):**
Бахтияр (2026-03-04): поля `forOop`, `trainingForOop` — не новые, существуют давно.

**Факт 7 (edu_prog_type — нет справочника):**
Каиржан (2025-09-16) спрашивал «на какой справочник ссылается edu_prog_type?» — ответа не последовало. Значения из adm_doc: 1=Действующая, 2=Новая, 3=Инновационная.

**Факт 8 (Реестр ОП — НЦРВО):**
Бахтияр (2025-05-12): «Реестр ОП — запросить у НЦРВО Включение и Обновление заявки». Включение ОП в Реестр ≠ отправка через API. Нужна заявка через https://enic-kazakhstan.edu.kz/ru/reestr-op/ovpo-1

**Факт 9 (Подготовительное отделение — не заполнять professionId):**
Account (2023-10-17): «Не заполнять professionId, specializationID в таблице student [для подготовительного отделения]»

### Step 3: Ключевые бизнес-правила (для Executor)

Executor должен формализовать минимум следующие правила:

**Правило 1: classifier (тип записи PROFESSION)**
```
adm_doc.txt строки 1825–1834:
  classifier = 1  → Запись описывает Специальность (старый формат)
  classifier = 2  → Запись описывает ГОП (новый формат, основной)
```

**Правило 2: code vs professionCode (два разных поля!)**
```
adm_doc.txt строки 1860–1884:
  professionCode  → Внутренний код ВУЗа для специальности/ГОП
  code            → Код из центрального справочника center_profession
                     ⚠️ Это два РАЗНЫХ поля! code — обязателен для сопоставления
```

**Правило 3: specializationCode (формат кода ОП)**
```
adm_doc.txt строки 6224–6247:
  IF specializations.is_interdisciplinary = true:
      specializationCode = код_области_образования (4 цифры) + "088" + порядковый_номер (2 цифры)
  ELSE:
      specializationCode = код_направления_подготовки (5 цифр) + порядковый_номер (2 цифры)
  
  Условие: обязателен, если center_profession.classifier=2 (т.е. ГОП)
```

**Правило 4: statusep (статус ОП в Реестре)**
```
adm_doc.txt строки 6273–6282:
  statusep = 0  → Не включена в Реестр ОП
  statusep = 1  → Включена в Реестр ОП
  statusep = 2  → Исключена из Реестра ОП
```

**Правило 5: prof_caf_id (привязка ОП к кафедре)**
```
adm_doc.txt строки 6117–6129:
  specializations.prof_caf_id → ID из таблицы profession_cafedra
  ⚠️ Это НЕ professionId и НЕ cafedraId, а ID связующей записи PROFESSION_CAFEDRA
```

### Step 4: Sequencing Contract

Executor должен описать следующий порядок UPSERT:

```
Шаг 1: PROFESSION (ГОП — корневая сущность)
  ↓ professionId
Шаг 2: STUDYFORMS (формы обучения — справочник ВУЗа)
  ↓ [нет прямой FK, но нужен для TYP_CURRICULUM и PROFESSION_COST]
Шаг 3: PROFESSION_CAFEDRA (связка ГОП ↔ Кафедра)
  ↓ id (= prof_caf_id для SPECIALIZATIONS)
Шаг 4: SPECIALIZATIONS (ОП — зависит от PROFESSION_CAFEDRA через prof_caf_id)
  ↓ [конец основного pipeline]
Шаг 5 (опц.): PROFESSION_COST, TYP_CURRICULUM, EDUCATION_PROGRAMS_CODE, Q_EXAMINATIONS
```

### Step 5: Lookup CenterProfession

Executor должен описать алгоритм:

```
1. GET /api/v1/system-dictionary/CenterProfession
   → Массив: [{ id, code, nameRu, nameKz, nameEn, parentId?, levelId?, ... }]

2. Сопоставление по коду:
   local.professionCode → найти в массиве запись где center.code == local.professionCode
   → PROFESSION.centerProfId = center.id

3. Если не найден:
   → Проверить, является ли код старым форматом (5B..., 5M...)
   → Попытаться маппинг через таблицу соответствий (5B → 6B)
   → Если маппинг невозможен → пометить ⚠️, не отправлять centerProfId
```

### Step 6: Gotchas

Executor должен задокументировать минимум:

1. **code ≠ professionCode** — два разных поля, оба обязательны
2. **classifier=1 vs classifier=2** — разные типы записей в одной таблице
3. **prof_caf_id ≠ professionId** — ОП привязывается к PROFESSION_CAFEDRA, не напрямую к PROFESSION
4. **specializationCode — формат зависит от is_interdisciplinary**
5. **Full Replace** — при UPSERT PROFESSION все поля должны быть отправлены повторно, иначе будут сброшены в null

## 5. Acceptance Criteria

- [ ] RF содержит маппинг ≥8 полей PROFESSION с бизнес-правилами (classifier, code, professionCode, deleted, etc.)
- [ ] RF содержит маппинг ≥15 полей SPECIALIZATIONS с бизнес-правилами (prof_caf_id, specializationCode, statusep, eduprogtype, is_interdisciplinary, совместные ОП fields, etc.)
- [ ] Sequencing Contract описан: 4+ шага с обоснованием FK-зависимостей
- [ ] Lookup CenterProfession: описан endpoint, алгоритм сопоставления по коду, fallback для старых кодов
- [ ] ≥5 Gotchas с указанием источника (adm_doc.txt строки, RF, чат)
- [ ] JSON-примеры для PROFESSION и SPECIALIZATIONS — полные пайлоады, готовые к отправке через `/org-data/list/save`
- [ ] Вспомогательные сущности (PROFESSION_CAFEDRA, STUDYFORMS, PROFESSION_COST, TYP_CURRICULUM) — табличный обзор (поля + composite key)
- [ ] Документ нейтрален к конкретной ИС ОВПО
- [ ] Observations (out-of-scope) вынесены в отдельную секцию

## 6. Риски фазы

| Риск | Mitigation |
|------|------------|
| Расхождение adm_doc.txt и OpenAPI по именам полей | Формализовать расхождения в секции Gotchas. Указать оба варианта (`adm_doc → API actual`). Ссылаться на KNOWLEDGE.md §1.6 (Naming Traps) |
| Структура `CenterProfession` справочника не полностью описана | Описать гипотезу на основе `{ id, code, nameRu, ... }`. Пометить ⚠️ все предполагаемые поля |
| Сложность specializations (30+ полей, половина — совместные ОП) | Разделить маппинг на обязательные поля и блок «Совместные ОП» (отдельная подсекция) |

---

*TS — TFW-9: Инструкция по синхронизации Реестра образовательных программ | 2026-04-15*
