# TS — TFW-7: Процедура удаления приказов из ЕПВО

> **Дата**: 2026-03-18
> **Автор**: Coordinator (AI)
> **Статус**: ✅ TS — Утверждён
> **Parent HL**: [HL-TFW-7__delete_student_orders](HL-TFW-7__delete_student_orders.md)

---

## 1. Цель

Создать RF-документ, описывающий полную процедуру удаления приказов и связанных сущностей из ЕПВО через Delete API. Документ должен быть достаточным, чтобы интегратор любой ИС ОВПО мог безопасно откатить ошибочно отправленные приказы любого типа.

## 2. Scope

### In Scope
- Pipeline удаления (обратный порядок сущностей для каждого типа приказа из RF_TFW-5)
- **Детализированный pipeline для type=13 (стипендии)** — 7 сущностей (SCHOLARSHIP + TRANSCRIPT + 5 базовых)
- Composite key type и поле ID в body для каждой сущности приказа (8+ сущностей)
- Побочные эффекты на `STUDENT` и вспомогательные сущности после удаления
- Матрица: тип приказа → набор сущностей для удаления
- Ограничения API (каскадность, идемпотентность, soft delete)
- Практические наблюдения из проекта AD ЕПВО (пример реализации)
- Рекомендации: в каком порядке удалять, что проверять после удаления

### Out of Scope
- Практическое тестирование Delete API (нет live-запросов)
- Написание кода интеграции
- Удаление сущностей, не связанных с приказами (STUDENT, TUTOR и т.д.)

## 3. Затрагиваемые файлы

| Файл | Действие | Описание |
|------|----------|----------|
| `tasks/TFW-7__delete_student_orders/RF__TFW-7__delete_student_orders.md` | CREATE | RF — процедура удаления приказов |

**Бюджет:** 1 новый файл, 0 модификаций. ✅

## 4. Детальные шаги

### Step 1: Delete API — механика вызова

Описать механику `POST /org-data/{typeCode}/delete` на основе RF_TFW-2.5:
- URL, метод, headers
- Формат body: `{ "type": "...", "id/orderId/sectionId/...": <value> }`
- Ответ сервера (200, 400)
- Ограничение: 1 запись за вызов (нет batch delete)

### Step 2: Composite key map для сущностей приказов

Составить таблицу composite key → body-поле для каждой сущности, участвующей в pipeline приказов:

| Сущность | typeCode | Composite Key Type | Поле ID в body |
|----------|----------|--------------------|----------------|
| `ORDERS` | `ORDERS` | ? | `orderId` или `id` |
| `ORDER_SECTIONS` | `ORDER_SECTIONS` | ? | `sectionId` или `id` |
| `SECTION_PERSON` | `SECTION_PERSON` | ? | `id` |
| `ORDER_STUDENT_INFO` | `ORDER_STUDENT_INFO` | ? | `orderStudentInfoId` или `id` |
| `ORDERS_ADDITIONAL` | `ORDERS_ADDITIONAL` | ? | `id` |
| `SCHOLARSHIP` | `SCHOLARSHIP` | `UNIVERSITY_ID_COMPOSITE_KEY` | `id` ❓ |
| `TRANSCRIPT` | `TRANSCRIPT` | ? | `id` ❓ |
| `RETIRES` | `RETIRES` | `UNIVERSITY_ID_COMPOSITE_KEY` | `id` ✅ |

> `RETIRES` подтверждён из KNOWLEDGE.md §2.8. `SCHOLARSHIP` и `TRANSCRIPT` — гипотезы. Остальные — гипотезы на основе RF_TFW-2.5.

**Источники:** RF_TFW-2.5 §1.3, KNOWLEDGE.md §2.8, RF_TFW-1.7 (OpenAPI поля).

### Step 3: Pipeline удаления по типам приказов

Инвертировать pipeline создания из RF_TFW-5 §3. Для каждого контингентного orderType указать:
1. Какие сущности удалять и в каком порядке (дочерние → родительские)
2. Какие побочные эффекты откатить (например, `STUDENT.status` обратно)

Группировать типы по общему шаблону удаления:

| Шаблон | Типы приказов | Сущности для удаления (в порядке) |
|--------|---------------|-----------------------------------|
| Базовый (5 сущностей) | 2, 3, 7, 8, 9, 11, 48, 49 | ORDERS_ADDITIONAL → ORDER_STUDENT_INFO → SECTION_PERSON → ORDER_SECTIONS → ORDERS |
| + RETIRES | 6, 14 | RETIRES → (базовый) |
| **+ SCHOLARSHIP + TRANSCRIPT** | **13, 27** | **TRANSCRIPT → SCHOLARSHIP → (базовый)** |
| + GRADUATES/DIPLOMA | 28 | GRADUATES → STUDENT_DIPLOMA_INFO → (базовый) |
| + ACADEMIC_MOBILITY | 30, 31, 32, 33 | ORDERS_ACADEMIC_MOBILITY → (базовый) |
| + COURSE_TRANSFER | 34 | COURSE_TRANSFER_ORDER → (базовый) |
| + INTERNSHIP | 39 | ORDER_INTERNSHIP_STUDENTS → (базовый) |

### Step 3b: Детальный pipeline удаления для type=13 (стипендии)

На основе практической реализации AD ЕПВО (два источника: `scholarship_csv.py` и `orders_importer.py`) описать:

**Pipeline создания (7 сущностей, подтверждённый практикой):**
```
ORDERS (orderType=13) → ORDER_SECTIONS → SECTION_PERSON (movementDate, overall_performance)
→ ORDER_STUDENT_INFO → ORDERS_ADDITIONAL → SCHOLARSHIP → TRANSCRIPT
```

**Pipeline удаления (обратный порядок, 7 сущностей):**
```
TRANSCRIPT → SCHOLARSHIP → ORDERS_ADDITIONAL → ORDER_STUDENT_INFO
→ SECTION_PERSON → ORDER_SECTIONS → ORDERS
```

Ключевые особенности для документирования:
- **TRANSCRIPT:** создаётся с `not_included_scholarship=True` (исключение из стипендиальных отчётов)
- **SCHOLARSHIP:** обязательные поля `scholarshipMoney`, `sectionId`, `scholarshipTypeId`, `overallPerformance`
- **ID-формула с month_offset:** в AD ЕПВО используется формула `base + studentId + (month-1)*1M` для уникальности ID при множественных месяцах
- **Побочные эффекты:** удаление приказа о стипендии **не меняет** `STUDENT.status`, но может повлиять на карточку финансирования (кэш ~1-2 часа)

### Step 4: Побочные эффекты (откат STUDENT)

Описать, какие поля STUDENT нужно вернуть в предыдущее состояние после удаления приказа:

| orderType | Что откатить в STUDENT |
|-----------|------------------------|
| 2 (зачисление) | `status` → предыдущий (или удалить запись?) |
| 3 (отчисление) | `status → 1`, `studyStatusId` обратно |
| 6 (академ.отпуск) | `isinretire → 0` |
| 28 (выпуск) | `status → 1`, `courseNumber` обратно |
| ... | ... |

> ⚠️ Откат STUDENT — это **UPSERT**, не delete. Нужно знать предыдущее состояние.

### Step 5: Ограничения и рекомендации

Собрать открытые вопросы из HL §2.2 и зафиксировать:
- **Каскадность:** гипотеза (нет каскадного удаления, т.к. UPSERT тоже не каскадный)
- **Soft delete:** гипотеза (на основе RF_TFW-2.5 §1.5.3)
- **Идемпотентность:** гипотеза + рекомендация (400 при повторном удалении)
- **Рекомендация:** всегда удалять все сущности явно, в обратном порядке

### Step 6: Observations

Обязательная секция RF — структурированная таблица:
- Несоответствия, обнаруженные при анализе
- Гипотезы, требующие верификации
- Тип: `gap / hypothesis / improvement`

## 5. Acceptance Criteria

- [ ] RF содержит механику Delete API с примером запроса
- [ ] Таблица composite key → body-поле для 8+ сущностей приказов (включая SCHOLARSHIP и TRANSCRIPT)
- [ ] Pipeline удаления описан для всех основных типов (сгруппированных по шаблонам)
- [ ] **Детальный pipeline для type=13** (стипендии) с 7 сущностями и особенностями (month_offset, TRANSCRIPT.not_included_scholarship)
- [ ] Побочные эффекты на STUDENT задокументированы для каждого типа
- [ ] Ограничения API (каскадность, soft delete, идемпотентность) зафиксированы
- [ ] Открытые вопросы из HL §2.2 разрешены или помечены ⚠️/❓
- [ ] Секция Observations заполнена
- [ ] Документ нейтрален (для любой ИС ОВПО)

## 6. Риски фазы

| Риск | Mitigation |
|------|------------|
| Composite key types для `ORDERS`, `ORDER_SECTIONS` не подтверждены практикой | Указать наиболее вероятный тип + альтернативу как ⚠️ |
| В chat_epvo.json нет упоминаний удаления приказов | Работать с RF_TFW-2.5 и логическими выводами, пометить как неверифицированные |
| Откат STUDENT требует знания предыдущего состояния | Описать как рекомендацию: сделать `find-by-id` перед удалением |

---

*TS — TFW-7: Процедура удаления приказов из ЕПВО | 2026-03-17*
