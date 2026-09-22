# Claude runtime scripts

## pre-bash-guard.sh
Stops known-dangerous shell patterns and nudges Claude toward faster search tooling.

## post-edit-validate.sh
Runs repository-aware validation after edits and writes machine-readable status under `.claude/runtime/`.
Customize this file heavily for your stack.

## stop-gate.sh
Blocks completion when there is no validation evidence or when validation still reports failures.
