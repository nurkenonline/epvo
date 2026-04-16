# Tech Debt Registry

| # | Source | Severity | File | Description | Action |
|---|--------|----------|------|-------------|--------|
| TD-1 | TFW-4/C RF | Low | `RF_TFW-4.C` | SQL View `v_epvo_transcripts` — владелец БД должен написать и оптимизировать запрос до начала интеграции | → backlog (TFW-4) |
| TD-2 | TFW-4/D RF | Med | Бизнес-процесс | Синтетические приказы на стипендию (type=13) — если ВУЗ не издаёт ежемесячный приказ, скрипту придётся генерировать фиктивные | → backlog (TFW-4) |
| TD-3 | TFW-4/E RF | Med | `STUDENT` поле | Семантика `status` vs `isStudent`: одно поле, но значения 1/3 (ОСМС) vs 1-4 (OpenAPI). Нужна унификация маппинга | → backlog (TFW-4) |
| TD-4 | TFW-4/E RF | Med | `GRADUATES`, `STUDENT_DIPLOMA_INFO`, `STUDENT_INFO` | Дублирование дипломных данных в 3 сущностях — single source of truth при реализации | → backlog (TFW-4) |
| TD-5 | TFW-5 RF obs. | Low | `RF_TFW-4.C`, `RF_TFW-1.7` | Naming: `orderType` vs `orderTypeId` в разных RF. Нужна унификация имени JSON-ключа | → backlog (TFW-5) |
| TD-6 | TFW-5 RF obs. | Med | `RF_TFW-1.7` | `SECTION_PERSON` (`sectionpersons`) не задокументирована как отдельная сущность в каталоге, хотя фактически является ей (Таблица 58 adm_doc) | → backlog (TFW-5) |
| TD-7 | TFW-5 RF obs. | Low | `KNOWLEDGE.md` | Дубликация текста в §3 «Решение частых проблем» (строки ~289-295 ≈ ~363-369) | → backlog (TFW-5) |
| TD-8 | TFW-5 RF obs. | Med | `RF_TFW-4.E` §6.1 | `orderType=6` ошибочно указан для выпуска; фактически type=6 = академ.отпуск, для выпуска: type=3 cat=1 (бакалавр.) или type=28 (маг./докт.) | → backlog (TFW-5) |
| TD-9 | TFW-5 RF obs. | Med | Общий | Нет единого справочника OrderType — значения рассредоточены по 5+ документам | → backlog (TFW-5) |
| TD-10 | TFW-6 RF obs. #1 | Med | `RF_TFW-4.E` §6.1 | `orderType=6` не исправлен для выпуска (связано с TD-8). Корректно: type=28 (маг./докт.) / type=3 cat=1 (бак.) | → backlog (TFW-6) |
| TD-11 | TFW-6 RF obs. #2 | Low | `RF_TFW-4.E` §4.1 | `status=4` для выпускников не упомянут, только `isStudent=3` (связано с TD-3) | → backlog (TFW-6) |
| TD-12 | TFW-6 RF obs. #3 | Med | `KNOWLEDGE.md` §2.11 | Sequencing Contract ссылается на ошибочный `orderType=6` — нужно обновить | → backlog (TFW-6) |
| TD-13 | TFW-6 RF obs. #4 | Low | `RF_TFW-5` §3.10 | Семантический конфликт: бакалавриат — `orderType=3 cat=1` (отчисление по выпуску) — нуждается в пояснении | → backlog (TFW-6) |
| TD-14 | TFW-8 ONB Risk #1 | Med | `RF_TFW-8` §1.4 | `ftutor` condition: PDF says `primaryEmploymentID=1`, chat says `=2` для зарубежного — верифицировать через тестовый UPSERT | → backlog (TFW-8) |
| TD-15 | TFW-8 ONB Risk #2 | Low | `RF_TFW-8` §1.5 | `liveRegType` condition в PDF вероятно опечатка (`type=2` вместо `type=0`) — уточнить в чате ЕПВО | → backlog (TFW-8) |
| TD-16 | TFW-8 ONB Inconsist. | Low | `RF_TFW-8` §1, §2 | `tutors.deleted` vs `tutor_cafedra.deleted` — оба поля существуют, разные контексты, документировать в KNOWLEDGE.md | → backlog (TFW-8) |
| TD-17 | TFW-8 RF §6 | Low | `RF_TFW-8` §6 | `TUTOR_PUBLICATION` composite key не подтверждён (`PUB_ID` или `UNIVERSITY_ID`) — верифицировать через API | → backlog (TFW-8) |
| TD-18 | TFW-7 RF obs. #1 | Med | `RF_TFW-5` §3.7 | Pipeline type=13 описан как 4 сущности, практика ИС ОВПО показывает 6+1 (+ ORDER_STUDENT_INFO, ORDERS_ADDITIONAL, TRANSCRIPT) | → backlog (TFW-7) |
| TD-19 | TFW-7 RF obs. #2 | Low | `KNOWLEDGE.md` | Нет раздела §2.9 (стипендии). Ссылка из RF_TFW-5 §3.7 ведёт в пустоту | → backlog (TFW-7) |
| TD-20 | TFW-7 RF obs. #3 | Low | `RF_TFW-2.5` §1.3 | Таблица composite keys не включает `ORDER_ID_COMPOSITE_KEY`, хотя он используется в OpenAPI для `ORDERS/find-by-id` | → backlog (TFW-7) |
| TD-21 | TFW-9 RF obs. #1 | Med | `RF_TFW-1.2` §2 | SPECIALIZATIONS показывает только 10 полей из OpenAPI, тогда как adm_doc (и RF_TFW-9) требует 30+. OpenAPI spec неполный | ✅ Resolved (TFW-10) |
| TD-22 | TFW-9 RF obs. #2 | High | `RF_TFW-1.2` §2 | Ошибочно указана прямая FK `professionId` для ОП (SPECIALIZATIONS), хотя реально привязка идёт через мост `PROFESSION_CAFEDRA` | ✅ Resolved (TFW-10) |
| TD-23 | TFW-9 RF obs. #3 | Low | `RF_TFW-4.B` §3.1 | Семантический конфликт: `duration` описано в месяцах, но `studyPeriod` в PROFESSION — в семестрах | ✅ Resolved (TFW-10) |
| TD-24 | TFW-9 RF obs. #4 | Low | `KNOWLEDGE.md` | Нет раздела §2.x для "Реестра образовательных программ". Нужно добавить сводку правил (classifier, prof_caf_id) | ✅ Resolved (TFW-10) |
| TD-25 | TFW-9 RF obs. #5 | Low | `RF_TFW-4.B` §3 | Сущность названа `EducationProgram`, но её фактический API typeCode = `SPECIALIZATIONS` | ✅ Resolved (TFW-10) |
| TD-26 | TFW-10 RF obs. | Low | OpenAPI spec | Swagger Inconsistency: SPECIALIZATIONS fields and FK keys are wrongly documented in OpenAPI v3 | → backlog (TFW-10) |

> Added by REVIEW files during task lifecycle. See `.tfw/workflows/docs.md`.
