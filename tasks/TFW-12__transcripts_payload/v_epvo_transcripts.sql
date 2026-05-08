-- Шаблон SQL View: v_epvo_transcripts
--
-- ПРИНЦИП: Vendor-Agnostic Structure
-- Данный шаблон оперирует абстрактными понятиями ("таблица студентов", "таблица оценок")
-- Местный DBA ОВПО должен заменить абстрактные таблицы и поля (обозначены префиксом 'db_') на реальные.

CREATE OR REPLACE VIEW v_epvo_transcripts AS
SELECT
    -- Базовые идентификаторы
    123 AS universityId, -- ЗАМЕНИТЬ на константу ID вашего ВУЗа
    db_marks.id AS id, -- Уникальный ID оценки/строки журнала
    db_students.id AS studentId, -- Ссылка на студента
    db_subjects.id AS subjectId, -- Ссылка на справочник дисциплин

-- Коды и названия дисциплины
COALESCE(db_subjects.code_kz, '-') AS subjectCode,
COALESCE(db_subjects.code_ru, '-') AS codeRu,
COALESCE(db_subjects.code_en, '-') AS codeEn,
COALESCE(db_subjects.name_ru, '-') AS subjectNameRu,
COALESCE(db_subjects.name_kz, '-') AS subjectNameKz,
COALESCE(db_subjects.name_en, '-') AS subjectNameEn,

-- Академические показатели
CAST(
    db_marks.credits AS DECIMAL(5, 2)
) AS credits,
CAST(
    db_marks.ects AS DECIMAL(5, 2)
) AS ects, -- Включено как базовое поле
db_marks.course_number AS courseNumber,
db_marks.term_number AS term,

-- Тип дисциплины (0-учебная, 1-практика, 2-госэкзамен, 5-зачет, 6-НИР...)
COALESCE(db_marks.type_id, 0) AS type,

-- Оценки
db_marks.alpha_mark AS alphaMark,
CAST(
    db_marks.numeral_mark AS DECIMAL(3, 2)
) AS numeralMark,
CAST(
    db_marks.total_mark AS DECIMAL(5, 2)
) AS totalMark,

-- Флаги
-- В JSON payload они должны быть приведены к boolean скриптом интеграции (кроме accepted)
CASE
    WHEN db_marks.total_mark >= 50 THEN 1
    ELSE 0
END AS accepted,
CASE
    WHEN db_marks.total_mark >= 50 THEN TRUE
    ELSE FALSE
END AS isPassed,
COALESCE(db_marks.is_retake, FALSE) AS wasretaken,
COALESCE(db_marks.is_deleted, FALSE) AS deleted,
COALESCE(
    db_marks.not_for_scholarship,
    FALSE
) AS notIncludedScholarship,

-- Специфичные флаги
CASE
    WHEN db_marks.type_id = 2 THEN TRUE
    ELSE FALSE
END AS isGeneralExam,
COALESCE(db_marks.is_additional, FALSE) AS isAdditionalSubject,
COALESCE(db_marks.is_coursework, FALSE) AS isCoursework,
COALESCE(
    db_marks.has_additional_type,
    FALSE
) AS isSubjectWithAdditionalType

-- Опциональное служебное поле (для Python скрипта)
-- is_ready_for_epvo = TRUE означает, что обязательные текстовые поля не пусты
-- , CASE WHEN db_subjects.name_ru IS NOT NULL THEN TRUE ELSE FALSE END AS is_ready_for_epvo

FROM
    abstract_table_marks AS db_marks
    INNER JOIN abstract_table_students AS db_students ON db_marks.student_id = db_students.id
    INNER JOIN abstract_table_subjects AS db_subjects ON db_marks.subject_id = db_subjects.id
WHERE
    db_marks.is_final = TRUE;
-- В транскрипт идут только итоговые оценки за семестр