# README Health Mini Checklist

A quick, practical check for whether a repository is easy to understand, run, test, and hand off.

## What This Is

This is a free 10-minute README review for solo builders, maintainers, and small teams. It helps spot the first bits of friction that make a repo harder to use or maintain.

It is intentionally small. Use it to find the obvious gaps before doing a deeper repo-health pass.

## Who It Is For

- Solo builders preparing a repo for users, contributors, or clients.
- Maintainers who keep answering the same setup questions.
- Small teams handing a repo to another developer.
- Developers trying to make a project easier to run, test, or review.

## 10-Minute README Health Check

Open the README and answer each question with `yes`, `partial`, or `no`.

- Can a new reader tell what the project does in the first 30 seconds?
- Is there a clear install or setup path?
- Is there a clear command to run the project locally?
- Is there a clear command to run tests?
- Is CI status or validation explained?
- Are required tools, runtimes, or environment variables listed?
- Are common setup failures or troubleshooting notes included?
- Is contribution or issue-reporting guidance easy to find?
- Can someone hand this repo to another developer without a private explanation?
- Are unsafe details like secrets, tokens, or private infrastructure absent from examples?

## Setup Clarity

Look for:

- Required runtime versions.
- Package manager choice.
- Install command.
- Local run command.
- Environment variable names without real values.

Good sign: a new developer can install and run the project without asking which command to use.

## Test Clarity

Look for:

- Test command.
- Expected test duration or scope.
- Notes for skipped, flaky, or optional tests.
- How to run the smallest useful validation.

Good sign: a maintainer can quickly tell whether a change broke the repo.

## CI Clarity

Look for:

- CI badge or a short note about automated checks.
- Which checks run on pull requests.
- What to do when CI fails.
- Any required local command that mirrors CI.

Good sign: contributors know what "green" means before opening a PR.

## Dependency Clarity

Look for:

- Runtime and package manager versions.
- Native/system dependencies.
- Lockfile expectations.
- Upgrade or dependency-refresh notes.

Good sign: setup failure is not caused by hidden dependency assumptions.

## Contribution Clarity

Look for:

- Where to open issues.
- What information to include in bug reports.
- Branch or PR expectations.
- Code style or formatting command.

Good sign: a helpful contributor can make a focused change without guessing the process.

## Handoff Clarity

Look for:

- Project purpose.
- Current status.
- Known limitations.
- Deployment or release notes, if relevant.
- Owner or maintainer expectations.

Good sign: another developer can pick up the repo and name the next practical action.

## Scoring Guide

Score each category from 0 to 2:

- `0`: missing or unclear.
- `1`: partially present, but a new developer may still need help.
- `2`: clear enough for a new developer to act.

Categories:

- Setup clarity.
- Test clarity.
- CI clarity.
- Dependency clarity.
- Contribution clarity.
- Handoff clarity.

Total:

- `0-4`: README needs a basic recovery pass.
- `5-8`: README is usable, but handoff friction remains.
- `9-12`: README is in good shape for a lightweight repo-health pass.

## Next Action Examples

If setup clarity is weak:

- Add the install command.
- Add the local run command.
- List required runtime versions.

If test clarity is weak:

- Add the main test command.
- Add the fastest validation command.
- Explain known skipped or flaky tests.

If CI clarity is weak:

- Link or name the CI workflow.
- Explain what checks must pass.
- Add a local command that mirrors CI when possible.

If handoff clarity is weak:

- Add the project status.
- Add known limitations.
- Add the next recommended maintenance task.

## Full Kit

For deeper worksheets, intake questions, CI/test triage, dependency/docs hygiene, and a report template, use the full Repo Health Snapshot Kit:

https://designsy1.gumroad.com/l/toksiz

The full kit is self-serve. It does not include custom repository review.

## Done-For-You Intake

For a scoped done-for-you repo health request, open an intake issue:

https://github.com/xcapselx/repo-health-checks/issues

Do not post secrets, API keys, recovery codes, customer data, private infrastructure details, production credentials, payment details, tax information, or private keys in issues.
