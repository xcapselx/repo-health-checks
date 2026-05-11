# Service Details

## How I Work

1. Reproduce the issue or inspect the target workflow.
2. Keep the scope tight and avoid unrelated refactors.
3. Document commands, assumptions, and verification results.
4. Flag anything I cannot verify.
5. Deliver either a concise report or a focused branch/patch, depending on the package.

## Intake Questions

- What repository should I inspect?
- Is the repository public, or will access be granted separately?
- Which command, workflow, or test is failing?
- What result do you expect instead?
- Which branch should I target?
- Are there any private services, secrets, production data, or paid APIs that I must avoid?
- Do you want a report only, or a focused patch/PR if the issue is small?
- What deadline matters for this fix?

## Boundaries

- No secrets in GitHub issues.
- No broad refactors without a new scope.
- No production incident response.
- No private infrastructure access unless explicitly scoped through an approved channel.
- No off-scope security testing.

## Deliverable Format

Each delivery includes:

- Summary of the problem.
- Commands run.
- Files or workflows inspected.
- Findings and likely cause.
- Patch or PR link when applicable.
- Verification notes.
- Remaining risks or follow-up recommendations.
