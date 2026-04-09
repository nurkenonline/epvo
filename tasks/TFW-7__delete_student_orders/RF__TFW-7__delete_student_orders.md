# RF — TFW-7: Процедура удаления приказов из ЕПВО

> **Дата**: 2026-03-18
> **Автор**: Executor (AI)
> **Статус**: 🟢 RF — Выполнено
> **Parent HL**: [HL-TFW-7__delete_student_orders](HL-TFW-7__delete_student_orders.md)
> **TS**: [TS__TFW-7__delete_student_orders](TS__TFW-7__delete_student_orders.md)

---

## 1. Delete API — механика вызова

### 1.1 Эндпоинт

```
POST /org-data/{typeCode}/delete
```

**Метод:** `POST` (не `DELETE`). Источник: [RF_TFW-2.5](../TFW-2__api_endpoints/RF_TFW-2.5__orgdata_delete_api.md) §1.1.

**Headers:**
```
Authorization: Basic <base64(username:password)>
Content-Type: application/json
```

**Request Body:**
```json
{
  "type": "<COMPOSITE_KEY_TYPE>",
  "<idField>": <value>
}
```

**Response:**
- `200 OK` — запись удалена (предположительно soft delete)
- `400 Bad Request` — запись не найдена или неверный ключ

**Ограничения:**
- Одна запись за вызов (нет batch delete)
- Soft delete (записи помечаются как неактивные, не удаляются физически) ⚠️

---

## 2. Composite Key Map для сущностей приказов

| Сущность | typeCode | Composite Key Type | Поле ID в body | Источник |
|----------|----------|--------------------|:--------------:|----------|
| ORDERS | `ORDERS` | `ORDER_ID_COMPOSITE_KEY` ⚠️ | `orderId` | По аналогии с `find-by-id` |
| ORDER_SECTIONS | `ORDER_SECTIONS` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` (= sectionId) | Гипотеза |
| SECTION_PERSON | `SECTION_PERSON` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` | Гипотеза |
| ORDER_STUDENT_INFO | `ORDER_STUDENT_INFO` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` (= orderStudentInfoId) | Гипотеза |
| ORDERS_ADDITIONAL | `ORDERS_ADDITIONAL` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` | Гипотеза |
| SCHOLARSHIP | `SCHOLARSHIP` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` | Гипотеза |
| TRANSCRIPT | `TRANSCRIPT` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` | Гипотеза |
| RETIRES | `RETIRES` | `UNIVERSITY_ID_COMPOSITE_KEY` | `id` | ✅ KNOWLEDGE.md §2.8 |
| GRADUATES | `GRADUATES` | `STUDENT_ID_COMPOSITE_KEY` ⚠️ | `studentId` | Гипотеза |
| STUDENT_DIPLOMA_INFO | `STUDENT_DIPLOMA_INFO` | `STUDENT_ID_COMPOSITE_KEY` ⚠️ | `studentId` | Гипотеза |
| ORDERS_ACADEMIC_MOBILITY | `ORDERS_ACADEMIC_MOBILITY` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` | Гипотеза |
| COURSE_TRANSFER_ORDER | `COURSE_TRANSFER_ORDER` | `UNIVERSITY_ID_COMPOSITE_KEY` ⚠️ | `id` | Гипотеза |

> ⚠️ **Только RETIRES подтверждён практически.** Все остальные типы — гипотезы на основе паттерна из [RF_TFW-2.5](../TFW-2__api_endpoints/RF_TFW-2.5__orgdata_delete_api.md) §1.3 и OpenAPI spec (`find-by-id`). При ошибке `400` — попробовать альтернативный composite key type.

> ⚠️ **Для ORDERS:** В OpenAPI `find-by-id` используется `ORDER_ID_COMPOSITE_KEY` с полем `orderId`. Для delete предположительно тот же тип. Если `400` — попробовать `UNIVERSITY_ID_COMPOSITE_KEY` с полем `id`.

### 2.1 Пример запроса на удаление ORDERS

```bash
curl --location 'https://epvo.kz/isvuz/api/org-data/ORDERS/delete' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Basic <credentials>' \
  --data '{
    "type": "ORDER_ID_COMPOSITE_KEY",
    "orderId": 28037482
  }'
```

### 2.2 Пример запроса на удаление SCHOLARSHIP

```bash
curl --location 'https://epvo.kz/isvuz/api/org-data/SCHOLARSHIP/delete' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Basic <credentials>' \
  --data '{
    "type": "UNIVERSITY_ID_COMPOSITE_KEY",
    "id": 86037482
  }'
```

---

## 3. Pipeline удаления по типам приказов

### 3.1 Принцип: обратный порядок

Pipeline удаления = зеркальное отражение pipeline создания (из [RF_TFW-5](../TFW-5__student_orders/RF__TFW-5__student_orders.md) §3). Дочерние сущности удаляются **перед** родительскими, чтобы не нарушать FK-ограничения.

### 3.2 Шаблоны удаления

| Шаблон | orderType | Сущности для удаления (в порядке) | Кол-во вызовов |
|--------|:---------:|-----------------------------------|:--------------:|
| **Базовый** | 2, 3, 4, 7, 8, 9, 10, 11, 48, 49 | ORDERS_ADDITIONAL → ORDER_STUDENT_INFO → SECTION_PERSON → ORDER_SECTIONS → ORDERS | 5 |
| **+ RETIRES** | 6, 14 | RETIRES → (базовый) | 6 |
| **+ SCHOLARSHIP + TRANSCRIPT** | **13**, 27 | TRANSCRIPT ❓ → SCHOLARSHIP → (базовый) | 6–7 |
| **+ GRADUATES** | 28, 3 (cat=1) | GRADUATES → STUDENT_DIPLOMA_INFO → (базовый) | 7 |
| **+ ACADEMIC_MOBILITY** | 30, 31, 32, 33 | ORDERS_ACADEMIC_MOBILITY → (базовый) | 6 |
| **+ COURSE_TRANSFER** | 34 | COURSE_TRANSFER_ORDER → (базовый) | 6 |
| **+ INTERNSHIP** | 39 | ORDER_INTERNSHIP_STUDENTS → (базовый) | 6 |

> ❓ TRANSCRIPT при type=13: зависит от реализации ИС ОВПО. Некоторые реализации создают TRANSCRIPT с `not_included_scholarship=True`, другие — нет. Удалять только если TRANSCRIPT был создан.

### 3.3 Базовый pipeline удаления (5 сущностей)

Применяется к: type=2, 3, 4, 7, 8, 9, 10, 11, 48, 49.

```
Шаг 1: DELETE /org-data/ORDERS_ADDITIONAL/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <additional_id> }

Шаг 2: DELETE /org-data/ORDER_STUDENT_INFO/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <osi_id> }

Шаг 3: DELETE /org-data/SECTION_PERSON/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <person_id> }

Шаг 4: DELETE /org-data/ORDER_SECTIONS/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <section_id> }

Шаг 5: DELETE /org-data/ORDERS/delete
         → { "type": "ORDER_ID_COMPOSITE_KEY", "orderId": <order_id> } ⚠️
```

> ⚠️ Шаг 5: если `ORDER_ID_COMPOSITE_KEY` вернёт `400`, попробовать `UNIVERSITY_ID_COMPOSITE_KEY` с `"id": <order_id>`.

### 3.4 Pipeline удаления type=6/14 (академический отпуск)

```
Шаг 0: DELETE /org-data/RETIRES/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <retires_id> }  ✅ подтверждён

Шаги 1–5: (базовый pipeline)
```

> ⚠️ При type=14 (продление): `RETIRES` — **одна запись на студента**. Удаление RETIRES при продлении может потребовать восстановления предыдущих значений (termscount, finishDate). Источник: KNOWLEDGE.md §2.8.

### 3.5 Pipeline удаления type=13 (стипендии) — детализированный

**Источники:**
- [RF_TFW-5](../TFW-5__student_orders/RF__TFW-5__student_orders.md) §3.7 — базовый pipeline (4 сущности)
- Практическая реализация ИС ОВПО — расширенный pipeline (6 сущностей)
- Практическая реализация ИС ОВПО — pipeline с TRANSCRIPT (7 сущностей)

#### 3.5.1 Pipeline создания (из практической реализации)

```
ORDERS (orderType=13, categoryId=1)
  → ORDER_SECTIONS (orderId, universityId)
    → SECTION_PERSON (sectionId, personId=studentId, movementDate, overallPerformance)
      → ORDER_STUDENT_INFO (orderId, studentId, course)
        → ORDERS_ADDITIONAL (orderId, studentId, course)
          → SCHOLARSHIP (studentId, sectionId, scholarshipYear/Month, scholarshipMoney,
                          scholarshipTypeId, overallPerformance, terminationDate, operation=1)
            → TRANSCRIPT (опционально, not_included_scholarship=True)
```

> **Расхождение с RF_TFW-5 §3.7:** RF_TFW-5 описывает 4 сущности (ORDERS → ORDER_SECTIONS → SECTION_PERSON → SCHOLARSHIP), но практическая реализация ИС ОВПО добавляет ORDER_STUDENT_INFO и ORDERS_ADDITIONAL. Полный pipeline = 6 обязательных + 1 опциональный (TRANSCRIPT).

#### 3.5.2 Pipeline удаления (обратный порядок)

```
Шаг 0 (если создан): DELETE /org-data/TRANSCRIPT/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <transcript_id> }

Шаг 1: DELETE /org-data/SCHOLARSHIP/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <scholarship_id> }

Шаг 2: DELETE /org-data/ORDERS_ADDITIONAL/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <additional_id> }

Шаг 3: DELETE /org-data/ORDER_STUDENT_INFO/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <osi_id> }

Шаг 4: DELETE /org-data/SECTION_PERSON/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <person_id> }

Шаг 5: DELETE /org-data/ORDER_SECTIONS/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <section_id> }

Шаг 6: DELETE /org-data/ORDERS/delete
         → { "type": "ORDER_ID_COMPOSITE_KEY", "orderId": <order_id> } ⚠️
```

#### 3.5.3 Особенности стипендийных приказов

| Аспект | Описание |
|--------|----------|
| **Связь SCHOLARSHIP ↔ ORDER** | Через поле `sectionId` (= `orderId` по конвенции) |
| **Множественные месяцы** | Один студент может иметь стипендии за несколько месяцев. Каждый месяц — отдельный pipeline с отдельными ID. Формула ID с `month_offset`: `base + studentId + (month-1) × 1 000 000` |
| **Удаление за конкретный месяц** | Удалять нужно конкретный набор сущностей для конкретного месяца. ID вычисляется по формуле с month_offset |
| **TRANSCRIPT** | Опционально создаётся с `not_included_scholarship=True`. Удалять **только если был создан** |
| **Побочные эффекты** | Удаление приказа о стипендии **не меняет** `STUDENT.status` и `isStudent`. Может повлиять на модуль финансирования ЕПВО (кэш обновляется ~1-2 часа) |
| **type=27 (прекращение стипендии)** | Устанавливает `terminationDate`, `scholarshipMoney=0`. Удаление type=27 → отмена прекращения. Может потребовать UPSERT SCHOLARSHIP с восстановлением суммы |

### 3.6 Pipeline удаления type=28 (завершение обучения)

```
Шаг 0: DELETE /org-data/GRADUATES/delete
         → { "type": "STUDENT_ID_COMPOSITE_KEY", "studentId": <student_id> } ⚠️

Шаг 1: DELETE /org-data/STUDENT_DIPLOMA_INFO/delete
         → { "type": "STUDENT_ID_COMPOSITE_KEY", "studentId": <student_id> } ⚠️

Шаги 2–6: (базовый pipeline)
```

> ⚠️ Для GRADUATES и STUDENT_DIPLOMA_INFO composite key предположительно `STUDENT_ID_COMPOSITE_KEY`, т.к. записи привязаны к `studentId`, а не к `orderId`.

### 3.7 Pipeline удаления type=30/32 (мобильность)

```
Шаг 0: DELETE /org-data/ORDERS_ACADEMIC_MOBILITY/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <mobility_id> }

Шаги 1–5: (базовый pipeline)
```

### 3.8 Pipeline удаления type=34 (перевод с курса)

```
Шаг 0: DELETE /org-data/COURSE_TRANSFER_ORDER/delete
         → { "type": "UNIVERSITY_ID_COMPOSITE_KEY", "id": <transfer_id> }

Шаги 1–5: (базовый pipeline)
```

---

## 4. Побочные эффекты на STUDENT после удаления

Удаление приказа отменяет его последствия на профиль студента. Для полного отката необходимо **вручную обновить** `STUDENT` через UPSERT.

| orderType | Какие поля STUDENT откатить | Как |
|:---------:|----------------------------|-----|
| 2 (зачисление) | `status`, `enrollOrderDate` | UPSERT STUDENT: восстановить предыдущий status (или удалить студента, если он был создан этим приказом) |
| 3 (отчисление) | `status → 1`, `studyStatusId` | UPSERT STUDENT: вернуть `status=1` (обучающийся) |
| 4 (перевод) | `professionId`, `studyFormId`, `courseNumber`, `studyLanguageId` | UPSERT STUDENT: восстановить старые значения (сохранить old* из ORDER_STUDENT_INFO **до** удаления) |
| 6 (академ.отпуск) | `isinretire → 0` | UPSERT STUDENT: `isinretire=0` |
| 10 (смена оплаты) | `paymentFormId` | UPSERT STUDENT: восстановить старую форму оплаты |
| **13 (стипендия)** | **—** | **Не требуется откат STUDENT** |
| 14 (продление академ.) | `isinretire` | Зависит от контекста: если это единственный приказ — `isinretire=0` |
| **27 (прекращение стипендии)** | **—** | **Не требуется откат STUDENT.** Может потребовать UPSERT SCHOLARSHIP (восстановить сумму) |
| 28 (выпуск) | `status → 1`, `courseNumber` | UPSERT STUDENT: вернуть `status=1`, восстановить `courseNumber` |
| 30/32 (мобильность) | `academicMobility` | UPSERT STUDENT: восстановить предыдущее значение |
| 31/33 (возвращение) | `academicMobility` | UPSERT STUDENT: восстановить флаг мобильности |

> ⚠️ **Рекомендация:** Перед удалением приказа — вызвать `GET /org-data/STUDENT/find-by-id` для сохранения текущего состояния студента. Это позволит восстановить значения при ошибке.

> ⚠️ **UPSERT = Full Replace** (KNOWLEDGE.md §1.1): при обновлении STUDENT необходимо отправлять **все** поля, не только изменённые.

---

## 5. Ограничения и рекомендации

### 5.1 Каскадное удаление

**Гипотеза: каскадного удаления нет.** UPSERT в ЕПВО не каскадный (KNOWLEDGE.md §1.1). По аналогии, delete тоже не каскадный. Удаление ORDERS **не удаляет** автоматически ORDER_SECTIONS, SECTION_PERSON и т.д.

**Рекомендация:** Всегда удалять **все** сущности pipeline явно, в обратном порядке.

### 5.2 Идемпотентность

**Гипотеза:** Повторное удаление уже удалённой записи вернёт `400 Bad Request` (запись не найдена). Источник: RF_TFW-2.5 §1.4 (формат ошибки).

**Рекомендация:** При получении `400` — считать удаление успешным (запись уже не существует) и продолжать pipeline.

### 5.3 Soft Delete

**Гипотеза: записи не удаляются физически.** Из RF_TFW-2.5 §1.5.3: «записи, вероятно, не удаляются физически из БД ЕПВО, а помечаются как неактивные».

**Последствия:**
- Повторное создание с тем же ID после soft delete → поведение неизвестно. Возможен конфликт или перезапись.
- **Рекомендация:** При повторном создании использовать **новые ID** во избежание конфликтов.

### 5.4 Порядок удаления

```
Дочерние → Родительские

Удаление в обратном порядке:
  Вспомогательные (SCHOLARSHIP, RETIRES, GRADUATES, TRANSCRIPT, ...)
    → ORDERS_ADDITIONAL
      → ORDER_STUDENT_INFO
        → SECTION_PERSON
          → ORDER_SECTIONS
            → ORDERS
```

**Если удаление сущности вернуло ошибку:**
- Залогировать ошибку
- **Продолжать** к следующей сущности (fail-forward)
- По завершении — вывести полный отчёт с ошибками

### 5.5 Определение ID для удаления

Для удаления необходимо знать ID каждой сущности. Два подхода:

1. **Детерминистический** — если ID вычислялись по формуле при создании (например, в ИС ОВПО: `order_id = base + studentId + month_offset`)
2. **Через запрос** — вызвать `find-all-pageable` или `find-by-id` для каждой сущности, чтобы получить ID

**Рекомендация:** Хранить ID созданных сущностей в локальном кэше при создании. При удалении — читать из кэша.

---

## 6. Ключевые решения

1. **`UNIVERSITY_ID_COMPOSITE_KEY` как fallback.** Для сущностей без собственного composite key type используется `UNIVERSITY_ID_COMPOSITE_KEY` с полем `id`. Подтверждён для `RETIRES` (KNOWLEDGE.md §2.8).

2. **`ORDER_ID_COMPOSITE_KEY` для ORDERS.** По аналогии с `find-by-id` (`epvo_client.get_order_details`), где используется `ORDER_ID_COMPOSITE_KEY` с полем `orderId`.

3. **6+1 сущностей для type=13.** RF_TFW-5 §3.7 описывает 4 сущности, но практическая реализация ИС ОВПО использует 6 (+ опционально TRANSCRIPT). В RF задокументирован полный pipeline из 6+1 сущностей.

4. **Побочные эффекты — ответственность интегратора.** Delete API не откатывает изменения в STUDENT автоматически. После удаления приказа интегратор должен самостоятельно обновить STUDENT через UPSERT.

## 7. Acceptance Criteria

- [x] RF содержит механику Delete API с примером запроса (§1, §2.1, §2.2)
- [x] Таблица composite key → body-поле для 12 сущностей приказов (§2)
- [x] Pipeline удаления описан для всех основных типов, сгруппированных по 7 шаблонам (§3.2)
- [x] Детальный pipeline для type=13 (стипендии) с 6+1 сущностями (§3.5)
- [x] Особенности стипендий: month_offset, TRANSCRIPT.not_included_scholarship, type=27 (§3.5.3)
- [x] Побочные эффекты на STUDENT задокументированы для 11 типов (§4)
- [x] Ограничения API: каскадность, soft delete, идемпотентность (§5.1-5.3)
- [x] Открытые вопросы из HL §2.2 разрешены или помечены ⚠️ (§2, §5)
- [x] Документ нейтрален (для любой ИС ОВПО)

## 8. Observations (out-of-scope, not modified)

| # | Файл | Строки | Тип | Описание |
|---|------|--------|-----|----------|
| 1 | RF_TFW-5 §3.7 | 170-181 | gap | Pipeline type=13 описан как 4 сущности, но практика ИС ОВПО показывает 6+1. RF_TFW-5 требует обновления |
| 2 | KNOWLEDGE.md | — | gap | Нет раздела §2.9 (стипендии). Ссылка в RF_TFW-5 §3.7 ведёт в пустоту. Документация стипендий не формализована |
| 3 | RF_TFW-2.5 §1.3 | 69-86 | gap | Таблица composite keys не включает `ORDER_ID_COMPOSITE_KEY`, хотя он используется в OpenAPI для `ORDERS/find-by-id` |

---

*RF — TFW-7: Процедура удаления приказов из ЕПВО | 2026-03-18*
