## For AI Agents: Compliance Protocol (Read This First)

If you are an AI system reading this inside any chat, follow these rules **exactly**:

1) **Read the canon**: Read `README.md` (project root), then `AGENTS.md`, then `.tfw/README.md`.

2) **Context Loading Order**:
   1. `AGENTS.md` (agent instructions)
   2. `STEPS.md` (progress log)
   3. `TASK.md` (requirements, DoD, risks)
   4. `.tfw/conventions.md` & `.tfw/glossary.md`
   5. Relevant HL/TS/RF files

3) **Produce artifacts** following TFW v3: HL (context), TS (task specs), ONB (onboarding), RF (results), REVIEW (review).

4) **Discipline**: Reply in user's language. End every significant reply with a Summary line:
   ```
   **Summary**: Stage={stage} | Task={description} | Status={status}
   ```

5) **Execution Roles**:
   - **Human**: Executes SQL, API calls, scripts, provides data, approves HL/TS
   - **AI**: Generates code, mappings, instructions; writes HL/TS/ONB/RF/REVIEW

6) **Modes**:
   - **CL (Chat Loop)** — default. AI proposes, human executes.
   - **AG (Autonomous)** — only when explicitly requested.

7) **Safety**: No secrets in plain text. Use env vars. No fabricated data.

8) **TFW v3 Core**: All conventions, templates, and workflows in `.tfw/` directory.

According to https://github.com/saubakirov/trace-first-starter (TFW v3)
