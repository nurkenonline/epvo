# ONB — TFW-7: Процедура удаления приказов из ЕПВО

> **Дата**: 2026-03-18
> **Автор**: Executor (AI)
> **Статус**: 🟠 ONB — Ожидает ответов
> **Parent HL**: [HL-TFW-7__delete_student_orders](HL-TFW-7__delete_student_orders.md)
> **TS**: [TS__TFW-7__delete_student_orders](TS__TFW-7__delete_student_orders.md)

---

## 1. Understanding (как понял задачу)

Создать RF-документ, описывающий обратную процедуру (удаление) для приказов ЕПВО. Для каждого типа приказа — какие сущности удалять, в каком порядке, с каким composite key, и какие побочные эффекты откатить. Отдельный детализированный pipeline для type=13 (стипендии) на основе практической реализации AD ЕПВО. Документация нейтральная, для любой ИС ОВПО.

## 2. Entry Points (откуда начинать)

| Источник | Что даёт |
|----------|---------|
| [RF_TFW-2.5](../TFW-2__api_endpoints/RF_TFW-2.5__orgdata_delete_api.md) | Механика Delete API: URL, body, composite keys, ограничения |
| [RF_TFW-5 §3](RF__TFW-5__student_orders.md) | Pipeline **создания** для 18 типов (инвертировать) |
| AD ЕПВО: `scholarship_csv.py` | Практический pipeline стипендии (6 сущностей + month_offset) |
| AD ЕПВО: `orders_importer.py` | Pipeline type=13 с TRANSCRIPT |
| KNOWLEDGE.md §2.8 | Подтверждённый DELETE для RETIRES |

## 3. Questions (blocking — cannot proceed without answers)

| # | Question | Answer |
|---|----------|--------|
| — | Нет блокирующих вопросов | — |

## 4. Recommendations (suggestions, not blocking)

1. **Composite key для ORDER_STUDENT_INFO**: в OpenAPI спецификации (`find-by-id`) используется `ORDER_STUDENT_INFO_COMPOSITE_KEY` с полем `orderStudentInfoId`. Для delete предположу аналогичный тип, но помечу как ⚠️.
2. **Composite key для ORDERS**: `ORDER_ID_COMPOSITE_KEY` с полем `orderId` (по аналогии с `find-by-id`). Помечу как ⚠️.

## 5. Risks Found (edge cases, potential issues not in TS)

1. **Зависимость от порядка при soft delete**: если удаление — soft delete, то даже при «неправильном» порядке записи не будут физически утеряны. Но FK-проверки на стороне ЕПВО могут заблокировать удаление родителя при наличии активных дочерних. Рекомендация: всегда удалять в обратном порядке.
2. **TRANSCRIPT при type=13**: RF_TFW-5 §3.7 не включает TRANSCRIPT в pipeline стипендии, но `orders_importer.py` создаёт его с `not_included_scholarship=True`. Если TRANSCRIPT был создан — его тоже нужно удалить. Но если pipeline не создавал TRANSCRIPT (как в `scholarship_csv.py`), то удалять нечего.
3. **Повторное создание после soft delete**: если ID использовать повторно после удаления, неясно — UPSERT перезапишет soft-deleted запись или создаст дубликат.

## 6. Inconsistencies with Code (spec vs reality)

1. **RF_TFW-5 §3.7 vs AD ЕПВО `scholarship_csv.py`**: RF_TFW-5 описывает pipeline стипендии как 4 сущности (ORDERS → ORDER_SECTIONS → SECTION_PERSON → SCHOLARSHIP), но `scholarship_csv.py` использует 6: добавляются `ORDER_STUDENT_INFO` и `ORDERS_ADDITIONAL`. В RF задокументирую полный pipeline из 6 сущностей (+ опционально TRANSCRIPT).

---

*ONB — TFW-7: Процедура удаления приказов из ЕПВО | 2026-03-18*
