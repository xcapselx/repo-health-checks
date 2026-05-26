# Sample Repo Health Scorecard

This scorecard is a synthetic example that pairs with the [Sample Repo Health Snapshot](SAMPLE_REPO_HEALTH_SNAPSHOT.md).

## Snapshot

Sample repo: `demo-task-board`

Overall score: `68 / 100`

Risk rating: `Medium`

Recommended next move: tighten README setup/test guidance before handing the repo to another developer.

## Scorecard

| Area | Weight | Sample Score | Status |
|---|---:|---:|---|
| Setup clarity | 25 | 14 | Needs cleanup |
| Test clarity | 15 | 10 | Partial |
| CI clarity | 10 | 7 | Partial |
| README clarity | 20 | 14 | Usable with gaps |
| Dependency hygiene | 10 | 8 | Mostly healthy |
| Contribution clarity | 10 | 6 | Missing basics |
| Handoff clarity | 10 | 9 | Stronger than average |

Adjusted score: `68 / 100`

## Fast Interpretation

- `85-100`: easy to hand off.
- `70-84`: usable, with small cleanup needed.
- `50-69`: works for the maintainer, but likely slows new contributors.
- `<50`: setup, test, or docs friction is likely blocking outside help.

## Top Three Fixes

1. Add exact install, run, and test commands to the README.
2. Explain environment variables without exposing real values.
3. Add a short CI and handoff note so helpers know what "ready" means.

## Links

- Free mini checklist: [README Health Mini Checklist](README_HEALTH_MINI_CHECKLIST.md)
- Full self-serve kit: https://designsy1.gumroad.com/l/toksiz
- Done-for-you intake: https://github.com/xcapselx/repo-health-checks/issues
