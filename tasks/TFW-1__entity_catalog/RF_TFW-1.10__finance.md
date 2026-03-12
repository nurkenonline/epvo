# RF_TFW-1.10 — Финансы

> **Группа:** Контракты, финансирование, стоимость, рейтинг, доходы
> **Сущностей:** 6 | **Composite Key:** `CONTRACT_ID_COMPOSITE_KEY`, `PROFIT_ID_COMPOSITE_KEY`, `URATING_ID_COMPOSITE_KEY`, `UNIVERSITY_ID_COMPOSITE_KEY`

---

## 1. U_CONTRACT — Договоры на обучение

**typeCode:** `U_CONTRACT`
**Composite Key:** `CONTRACT_ID_COMPOSITE_KEY` → `{ type, contractId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"U_CONTRACT"` |
| universityId | int32 | ✅ | ID вуза |
| contractId | int32 | ✅ | Уникальный ID договора |
| studentId | int32 | | ID обучающегося (→ Student) |
| contractNumber | string | | Номер договора |
| contractDate | date | | Дата договора |
| amount | double | | Сумма договора |
| year | int32 | | Учебный год |

**FK-зависимости:** `Student`

---

## 2. U_FINANCING — Финансирование

**typeCode:** `U_FINANCING`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"U_FINANCING"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| year | int32 | | Учебный год |
| sourceType | int32 | | Тип источника |
| amount | double | | Сумма финансирования |
| description | string | | Описание |

---

## 3. UNIVERSITY_FINANCING — Финансирование вуза

**typeCode:** `UNIVERSITY_FINANCING`
**Composite Key:** `UNIVERSITY_ID_COMPOSITE_KEY` → `{ type, id }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"UNIVERSITY_FINANCING"` |
| universityId | int32 | ✅ | ID вуза |
| id | int32 | ✅ | Уникальный ID |
| year | int32 | | Учебный год |
| budgetAmount | double | | Бюджетное финансирование |
| extraBudgetAmount | double | | Внебюджетное финансирование |

---

## 4. U_PROFIT — Доходы

**typeCode:** `U_PROFIT`
**Composite Key:** `PROFIT_ID_COMPOSITE_KEY` → `{ type, profitId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"U_PROFIT"` |
| universityId | int32 | ✅ | ID вуза |
| profitId | int32 | ✅ | Уникальный ID |
| year | int32 | | Учебный год |
| profitType | int32 | | Тип дохода |
| amount | double | | Сумма |

---

## 5. U_RATING — Рейтинги вуза

**typeCode:** `U_RATING`
**Composite Key:** `URATING_ID_COMPOSITE_KEY` → `{ type, uratingId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"U_RATING"` |
| universityId | int32 | ✅ | ID вуза |
| uratingId | int32 | ✅ | Уникальный ID рейтинга |
| ratingName | string | | Название рейтинга |
| year | int32 | | Год |
| position | int32 | | Позиция |
| score | double | | Балл |

---

## 6. PRACTICE_CONTRACT — Договоры на практику

**typeCode:** `PRACTICE_CONTRACT`
**Composite Key:** `PRACTICE_CONTRACT_ID_COMPOSITE_KEY` → `{ type, practiceContractId }`

| Поле | Тип | Обязательное | Описание |
|------|-----|:---:|----------|
| typeCode | string | ✅ | `"PRACTICE_CONTRACT"` |
| universityId | int32 | ✅ | ID вуза |
| practiceContractId | int32 | ✅ | Уникальный ID договора |
| organizationName | string | | Название организации |
| contractNumber | string | | Номер договора |
| contractDate | date | | Дата договора |
| startDate | date | | Дата начала |
| endDate | date | | Дата окончания |

---

## ❓ Поля с неясным описанием

В данной группе **нет** полей с пустым описанием.

---

*Создано: 2026-02-19 | Источник: OpenAPI spec v0 (epvo.kz)*
