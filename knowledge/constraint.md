# Knowledge: Constraint

> Topic file for `constraint` facts. Updated by `/tfw-knowledge`.
> See KNOWLEDGE.md §4 for the index.

> **Source format**: Use reference patterns (e.g., `RF TFW-18 §6`, `REVIEW TFW-22`).
> Build-time resolver converts these to hyperlinks. See compilable_contract.md §2.

| # | Fact | Verified | Source(s) | Added |
|---|------|----------|-----------|-------|
| 1 | API ЕПВО использует механизм Full Replace (UPSERT): при обновлении записи необходимо передавать все поля, иначе непереданные значения сбросятся в `null`. | 🟢 | KNOWLEDGE.md §1.1 | 2026-04-17 |
| 2 | Поле `scholarshipMoney` (сумма стипендии) технически обязательно; его отсутствие вызывает 500 ошибку сервера, хотя оно не возвращается при чтении (Write-only context). | 🟢 | KNOWLEDGE.md §2.9 | 2026-04-17 |
