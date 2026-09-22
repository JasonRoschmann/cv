# Work protocol

## Phase 1 — before implementation

- Read current project status.
- Break work into the smallest complete unit: one endpoint, one component, one migration, one worker behavior, one infrastructure change.
- Identify affected files and dependencies.
- Choose orchestration strategy: single session, subagent, or agent team.
- Produce a test and validation plan before writing code.
- If the requirement is unclear, ask or investigate before implementing.

## Phase 2 — implementation

- One complete unit at a time.
- Prefer test-first when practical.
- Then implement.
- Check work against applicable rules.
- No stubs, TODOs, `pass`, placeholder exceptions, or fake success paths.
- Re-check definition of done after each significant file change.

## Phase 3 — proof protocol

Proof is mandatory before claiming completion.

- Run the most relevant test command and show actual output.
- Run lint/typecheck/build where applicable and show actual output.
- If containers are involved, show actual runtime status.
- If logs are relevant, inspect recent logs and explain warnings/errors.
- Show a concrete proof action such as curl output, screenshot, or integration test result.
- Update project status before moving on.
- Wait for confirmation before starting the next independent task when the workflow requires staged progress.

## Phase 4 — debugging protocol

- Read the full stack trace, not just the final line.
- Identify file and line number.
- Find root cause rather than symptom.
- Implement fix.
- Add a reproduction or regression test that fails before the fix and passes after.
- Re-run the relevant validation suite.
- If paid APIs are involved, ask before retrying.
- Check adjacent code for similar defects.
