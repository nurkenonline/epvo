# Tech Debt Registry

| # | Source | Severity | File(s) | Description | Status |
|---|--------|----------|---------|-------------|--------|
| TD-1 | TFW-4/C RF | Low | `RF_TFW-4.C` | SQL View `v_epvo_transcripts` — владелец БД должен написать и оптимизировать запрос до начала интеграции | ⬜ Backlog |
| TD-2 | TFW-4/D RF | Med | Бизнес-процесс | Синтетические приказы на стипендию (type=13) — если ВУЗ не издаёт ежемесячный приказ, скрипту придётся генерировать фиктивные | ⬜ Backlog |
| TD-3 | TFW-4/E RF | Med | `STUDENT` поле | Семантика `status` vs `isStudent`: одно поле, но значения 1/3 (ОСМС) vs 1-4 (OpenAPI). Нужна унификация маппинга | ⬜ Backlog |
| TD-4 | TFW-4/E RF | Med | `GRADUATES`, `STUDENT_DIPLOMA_INFO`, `STUDENT_INFO` | Дублирование дипломных данных в 3 сущностях — single source of truth при реализации | ⬜ Backlog |
| TD-5 | TFW-5 RF obs. | Low | `RF_TFW-4.C`, `RF_TFW-1.7` | Naming: `orderType` vs `orderTypeId` в разных RF. Нужна унификация имени JSON-ключа | ⬜ Backlog |
| TD-6 | TFW-5 RF obs. | Med | `RF_TFW-1.7` | `SECTION_PERSON` (`sectionpersons`) не задокументирована как отдельная сущность в каталоге, хотя фактически является ей (Таблица 58 adm_doc) | ⬜ Backlog |
| TD-7 | TFW-5 RF obs. | Low | `KNOWLEDGE.md` | Дубликация текста в §3 «Решение частых проблем» (строки ~289-295 ≈ ~363-369) | ⬜ Backlog |
| TD-8 | TFW-5 RF obs. | Med | `RF_TFW-4.E` §6.1 | `orderType=6` ошибочно указан для выпуска; фактически type=6 = академ.отпуск, для выпуска: type=3 cat=1 (бакалавр.) или type=28 (маг./докт.) | ⬜ Backlog |
| TD-9 | TFW-5 RF obs. | Med | Общий | Нет единого справочника OrderType — значения рассредоточены по 5+ документам | ⬜ Backlog |
| TD-10 | TFW-6 RF obs. #1 | Med | `RF_TFW-4.E` §6.1 | `orderType=6` не исправлен для выпуска (связано с TD-8). Корректно: type=28 (маг./докт.) / type=3 cat=1 (бак.) | ⬜ Backlog |
| TD-11 | TFW-6 RF obs. #2 | Low | `RF_TFW-4.E` §4.1 | `status=4` для выпускников не упомянут, только `isStudent=3` (связано с TD-3) | ⬜ Backlog |
| TD-12 | TFW-6 RF obs. #3 | Med | `KNOWLEDGE.md` §2.11 | Sequencing Contract ссылается на ошибочный `orderType=6` — нужно обновить | ⬜ Backlog |
| TD-13 | TFW-6 RF obs. #4 | Low | `RF_TFW-5` §3.10 | Семантический конфликт: бакалавриат — `orderType=3 cat=1` (отчисление по выпуску) — нуждается в пояснении | ⬜ Backlog |
| TD-14 | TFW-8 ONB Risk #1 | Med | `RF_TFW-8` §1.4 | `ftutor` condition: PDF says `primaryEmploymentID=1`, chat says `=2` для зарубежного — верифицировать через тестовый UPSERT | ⬜ Backlog |
| TD-15 | TFW-8 ONB Risk #2 | Low | `RF_TFW-8` §1.5 | `liveRegType` condition в PDF вероятно опечатка (`type=2` вместо `type=0`) — уточнить в чате ЕПВО | ⬜ Backlog |
| TD-16 | TFW-8 ONB Inconsist. | Low | `RF_TFW-8` §1, §2 | `tutors.deleted` vs `tutor_cafedra.deleted` — оба поля существуют, разные контексты, документировать в KNOWLEDGE.md | ⬜ Backlog |
| TD-17 | TFW-8 RF §6 | Low | `RF_TFW-8` §6 | `TUTOR_PUBLICATION` composite key не подтверждён (`PUB_ID` или `UNIVERSITY_ID`) — верифицировать через API | ⬜ Backlog |

> Added by REVIEW files during task lifecycle. See `.tfw/workflows/docs.md`.
