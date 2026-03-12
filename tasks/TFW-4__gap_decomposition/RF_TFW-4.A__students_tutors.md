# RF_TFW-4.A — Базовый контингент (Обучающиеся и ППС)

> **Дата**: 2026-03-07
> **Связанная задача**: TFW-4 Phase A
> **Статус**: 🟢 RF — Ожидает ревью координатора

## 1. Сводка
Этот документ описывает строгие бизнес-правила (Business Logic Specification) для подготовки DTO-моделей сущностей `STUDENT`, `STUDENT_INFO` и `TUTOR` к отправке в ЕПВО. Артефакт должен использоваться агентами-исполнителями при написании mapper-классов (или ETL-скриптов).

## 2. Сущность: STUDENT (Обучающийся)
- **Endpoint**: `/org-data/list/save`
- **Composite Key**: `studentId`
- **Зависимости**: `CenterCountry`, `studyStatusId`

### 2.1. Матрица Маппинга
| EPVO Field | Type | Required | AD Source / Logic |
|------------|------|----------|-------------------|
| `studentId` | Int | ✅ | Уникальный ID студента из локальной БД |
| `firstName` | Str | ✅ | Имя по паспорту |
| `lastName` | Str | ✅ | Фамилия по паспорту |
| `iinPlt` | Str | ⚠️ | ИИН студента (12 цифр). Если не резидент, ИИН может быть пуст. |
| `sitizenshipId` | Int | ✅ | Гражданство (ID справочника `CenterCountry`). См. Пр. 1. |
| `incorrectiin` | Bool | ⚠️ | Флаг некорректного ИИН (см. Пр. 2). По умолчанию `false`. |
| `isStudent` | Int | ✅ | Флаг активности для ОСМС. `1` - активный, `3` - отчислен (см. Пр. 3). |

### 2.2. Бизнес-правила (Critical Business Logic)

**Правило 1 (Гражданство - Strict Drop):**
```text
IF local.citizenship IS NULL:
    LOG_ERROR("Гражданство не указано, запись пропущена")
    DROP_RECORD() // Не отправляем в ЕПВО
ELSE:
    EPVO.sitizenshipId = MATCH_COUNTRY_CODE(local.citizenship)
```
*Обоснование: Отправка Null или ложного гражданства (например 113 для всех) ломает отчеты ЕПВО и приводит к 500 ошибке API.*

**Правило 2 (ИИН и 7-й разряд):**
ЕПВО жестко проверяет 7-й разряд ИИН (пол).
```text
IF EPVO.sitizenshipId != 113:
    // Для иностранцев проверка 7-й цифры отключена на стороне ЕПВО
    EPVO.incorrectiin = false
ELSE:
    IF IIN_IS_WRONG_GENDER(local.iinPlt, local.sexId):
        // Если гос. орган выдал ИИН с ошибкой для гражданина РК
        EPVO.incorrectiin = true
    ELSE:
        EPVO.incorrectiin = false
```

**Правило 3 (ОСМС - isStudent):**
Логика статуса обучающегося:
```text
IF local.studyStatus == "Отчислен":
    EPVO.isStudent = 3
ELSE IF local.studyStatus == "Обучающийся":
    EPVO.isStudent = 1
ELSE:
    // В академическом отпуске и т.д.
    EPVO.isStudent = 0 // Либо согласно локальному маппингу
```

## 3. Сущность: STUDENT_INFO (Расширенные данные)
- **Endpoint**: `/org-data/list/save`
- **Composite Key**: `studentId`

### 3.1. Матрица Маппинга
| EPVO Field | Type | Required | AD Source / Logic |
|------------|------|----------|-------------------|
| `studentId` | Int | ✅ | Привязка к профилю `STUDENT` |

## 4. Сущность: TUTOR (ППС)
Аналогично студентам, для сотрудников (ППС) действует **Правило 1** по обязательному гражданству, иначе будет возвращена ошибка `400 Bad Request` или `500`.

## 5. Observations (out-of-scope, not modified)
No observations.
