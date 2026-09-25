# Critical prohibitions

These rules are always active.

- Never run `/init` in an existing project because it can overwrite project guidance.
- Never modify any `CLAUDE.md` file unless explicitly instructed.
- Never create a new `CLAUDE.md` when one already exists.
- Never implement multiple independent features in one unit of work.
- Never continue after a failing test suite without first addressing the failure or explicitly scoping around it.
- Never retry paid API calls automatically after an error without explicit approval.
- Never leave `pass`, `...`, `TODO`, placeholder returns, or scaffold-only code in production paths.
- Never commit `.env`, `.env.*`, secrets, or private keys.
- Never write implementation code before a test and validation plan exists.
- Never say “it works” without proof output.
- Never claim a test result without showing actual command output.
- Never move to the next task without a project status update.
- Never patch symptoms without identifying the root cause.
- Never introduce unpinned dependencies (`^`, `~`, floating tags, latest tags) in production-critical dependencies.
- Never use agent teams for sequential tasks where a single session or targeted subagents are cheaper and clearer.
