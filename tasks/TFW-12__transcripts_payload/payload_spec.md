# Спецификация JSON Payload: TRANSCRIPT

Основано на документе `sur_doc.txt` (Таблица 19. transcript).
Данная спецификация описывает контракт данных для передачи транскриптов (оценок) в API ЕПВО (`POST /org-data/list/save`).
Вся бизнес-логика извлечения данных должна быть скрыта в абстрактном SQL View `v_epvo_transcripts`.

## Пример JSON-объекта (Payload)

```json
[
  {
    "typeCode": "TRANSCRIPT",
    "universityId": 123,
    "id": 9876543,
    "studentId": 102030,
    "subjectId": 456,
    "subjectCode": "MATH101",
    "codeRu": "МАТ101",
    "codeEn": "MATH101",
    "subjectNameRu": "Высшая математика",
    "subjectNameKz": "Жоғары математика",
    "subjectNameEn": "Higher Mathematics",
    "credits": 5.0,
    "ects": 5.0,
    "courseNumber": 1,
    "term": 1,
    "type": 0,
    "alphaMark": "A",
    "numeralMark": 4.0,
    "totalMark": 95.5,
    "accepted": 1,
    "isPassed": true,
    "wasretaken": false,
    "deleted": false,
    "notIncludedScholarship": false,
    "isGeneralExam": false,
    "isAdditionalSubject": false,
    "isCoursework": false,
    "isSubjectWithAdditionalType": false
  }
]
```

## Описание полей (Контракт данных)

| Поле JSON | Тип | Обязательность | Описание |
|-----------|-----|----------------|----------|
| `typeCode` | string | **Да** | Всегда равно `"TRANSCRIPT"` |
| `universityId` | int | **Да** | Уникальный идентификатор ОВПО в системе ЕПВО |
| `id` | int | **Да** | Уникальный ID записи транскрипта |
| `studentId` | int | **Да** | ID студента (FK на абстрактную таблицу студентов) |
| `subjectId` | int | **Да** | ID дисциплины из справочника дисциплин |
| `subjectCode` | string | **Да** | Код дисциплины на казахском языке |
| `codeRu` | string | **Да** | Код дисциплины на русском языке |
| `codeEn` | string | **Да** | Код дисциплины на английском языке |
| `subjectNameRu` | string | **Да** | Название дисциплины на русском языке |
| `subjectNameKz` | string | **Да** | Название дисциплины на казахском языке |
| `subjectNameEn` | string | **Да** | Название дисциплины на английском языке |
| `credits` | float | **Да** | Количество кредитов |
| `ects` | float | **Да** | Коэффициент ECTS кредитов (включено как базовое поле) |
| `courseNumber` | int | **Да** | Номер курса (1, 2, 3...) |
| `term` | int | **Да** | Академический период (семестр: 1, 2, 3...) |
| `type` | int | **Да** | 0-учебная, 1-практика, 2-госэкзамен, 5-зачет, 6-НИР, 7-акад. разница, 32-без контроля |
| `alphaMark` | string | **Да** | Буквенная оценка (A, A-, B+, B...) |
| `numeralMark` | float | **Да** | Цифровой эквивалент (4.0, 3.67...) |
| `totalMark` | float | **Да** | Итоговая оценка в баллах/процентах (0 - 100) |
| `accepted` | int | **Да** | Признак "Дисциплина пройдена успешно" (обычно 0/1) |
| `isPassed` | boolean| Нет | Флаг успешного прохождения |
| `wasretaken` | boolean| **Да** | Признак повторного прохождения (Retake) |
| `deleted` | boolean| **Да** | Признак удаления записи |
| `notIncludedScholarship`| boolean| **Да** | Не учитывать при назначении стипендии |
| `isGeneralExam` | boolean| **Да** | По дисциплине предусмотрен госэкзамен (обязательно при `type=2`) |
| `isAdditionalSubject` | boolean| **Да** | Дополнительно пройденная дисциплина |
| `isCoursework` | boolean| **Да** | Является курсовой работой |
| `isSubjectWithAdditionalType`| boolean| **Да** | Дисциплина с доп. видом обучения |
| `hash` | string | Нет | Заполняется только если `type=2` (госэкзамен) |
| `markId` | int | Нет | Уникальный номер оценки |
| `grouptypeid` | int | Нет | Обязательно только если `type=1` (практика) |
