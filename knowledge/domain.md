# Knowledge: Domain

> Topic file for `domain` facts. Updated by `/tfw-knowledge`.
> See KNOWLEDGE.md §4 for the index.

> **Source format**: Use reference patterns (e.g., `RF TFW-18 §6`, `REVIEW TFW-22`).
> Build-time resolver converts these to hyperlinks. See compilable_contract.md §2.

| # | Fact | Verified | Source(s) | Added |
|---|------|----------|-----------|-------|
| 1 | Студент исчезает из модуля генерации дипломов сразу после смены статуса на "Выпускник" (`status=4`). Рекомендуется генерировать номер диплома до смены статуса (при `status=1`). | 🟢 | KNOWLEDGE.md §2.16 | 2026-04-17 |
| 2 | Для докторантов PhD обязательны поля `doctorDefended` и `dateDissertationDefense` в профиле `STUDENT` для успешной генерации номера диплома в ЕПВО. | 🟢 | KNOWLEDGE.md §2.5 | 2026-04-17 |
| 3 | Внутренняя академическая мобильность мапится на `categoryId` 301 (выезд) и 101 (приезд), внешняя мобильность — на 302 (выезд) и 102 (приезд). | 🟢 | KNOWLEDGE.md §1.7 | 2026-04-17 |
