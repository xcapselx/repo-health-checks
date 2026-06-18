# Repo Health Checks

Focused GitHub repository health checks, CI/test triage, and small automation fixes for builders who need to turn a messy, fast-built, or AI-built repo into a handoff-ready next-action list.

## GitHub Action

Use this repo as a GitHub Action in your CI to automatically check your repo health on every push and PR:

```yaml
- uses: xcapselx/repo-health-checks@v2
  with:
    path: '.'
    fail-on-low-score: 'false'
    output-format: 'markdown'
```

The action runs a non-invasive scan (no network calls, no data uploads) and produces a handoff-readiness scorecard with 9 checks covering README, LICENSE, SECURITY.md, dependency lockfiles, file tree hygiene, CI workflows, test structure, .gitignore, and community files. See the [example workflow](.github/workflows/repo-health-check.yml).

## Start Here

Cloned this repo? In the first 30 seconds, open the free [README Health Mini Checklist](README_HEALTH_MINI_CHECKLIST.md), pick one repo, and score whether it is handoff-ready: easy to understand, run, test, and turn into a next-action list.

After you finish, you can optionally share a [checklist result issue](https://github.com/xcapselx/repo-health-checks/issues/new?template=checklist-result.yml). Do not include secrets, credentials, private repo URLs, production access details, customer/user data, tokens/API keys, or private logs.

For the full path, use [START_HERE.md](START_HERE.md).

Shortest path:

1. Use the free [README Health Mini Checklist](README_HEALTH_MINI_CHECKLIST.md).
2. Compare your result with the [Sample Repo Health Snapshot](SAMPLE_REPO_HEALTH_SNAPSHOT.md) and [Sample Scorecard](SAMPLE_REPO_HEALTH_SCORECARD.md).
3. If you want the fuller self-serve workflow for turning scores into a repo-health report and prioritized next-action list, use the [Repo Health Snapshot Kit - $29](https://designsy1.gumroad.com/l/toksiz).
4. If you want scoped help on a specific repo, open a [done-for-you intake issue](https://github.com/xcapselx/repo-health-checks/issues/new?template=repo-health-check.yml).

The free checklist and samples are enough for a quick self-review. The $29 kit is self-serve and does not include a custom repo review.

## First 3 Kit Buyer Mini-Readouts

Launch bonus for the first 3 $29 kit buyers: request one public-repo mini-readout after purchase.

You get a 10-minute public-repo pass, one short note, and the top 3 next actions for handoff readiness.

Scope: public repos only. No secrets, private access, PR creation, security audit, production incident response, large refactor plan, ongoing consulting, or promised fixes.

Use the Gumroad purchase/support contact path with a public GitHub repo URL only.

## Free Mini Checklist

Not ready for a paid kit or review yet? Start with the free [README Health Mini Checklist](README_HEALTH_MINI_CHECKLIST.md) to check setup, tests, CI, dependencies, contribution notes, and handoff clarity in about 10 minutes.

## Sample Snapshot

Want to see the shape of the outcome first? Read the synthetic [Sample Repo Health Snapshot](SAMPLE_REPO_HEALTH_SNAPSHOT.md) and compact [Sample Scorecard](SAMPLE_REPO_HEALTH_SCORECARD.md).

## Self-Serve Kit

Want to turn checklist scores into a fuller self-serve report and next-action list without hiring someone yet?

[Buy the Repo Health Snapshot Kit - $29](https://designsy1.gumroad.com/l/toksiz)

It is a downloadable workflow for setup friction, test/CI triage, dependency and docs hygiene, safe intake, and a handoff-ready repo-health report.

## Services

### Repo Handoff Readiness Snapshot - $79

A focused repo review that turns setup, test, CI, docs, and handoff friction into a short scorecard and prioritized next-action list.

**[Buy now on Gumroad ->](https://designsy1.gumroad.com/l/ftgbj)**

What is included:
- Review one public-safe repository or sanitized repo context.
- Check README clarity, setup path, test command, CI signal, package scripts, dependency hygiene, contribution notes, and handoff friction.
- Deliver one Markdown snapshot with a handoff-readiness score, top friction points, prioritized next-action list, scope notes, and public-safety reminders.
- Target delivery: 24 hours after payment and usable public-safe context.

Timeline: 24 hours after payment and usable public-safe context.

### CI/Test Fix Sprint - $149

- Everything in Repo Health Snapshot.
- Prepare one focused patch or PR for a small reproducible issue.
- Include commands run and verification notes.

Timeline: 48 hours after reproduction access.

### Workflow Automation Upgrade - $299

- Improve one CI, test, lint, release, or repo automation workflow.
- Add concise documentation for how to run or maintain it.
- Deliver a focused branch or patch and verification notes.

Timeline: 72 hours after requirements are confirmed.

## Best Fit

- Solo builders with a repo that stopped passing tests.
- Small teams with fragile CI or unclear package scripts.
- Maintainers who need a short technical report before investing in a larger fix.
- Founders who want a focused cleanup without a long consulting engagement.

## Request A Review

Open a new issue with the repo link, failing command or workflow, expected result, preferred branch, and any constraints around sensitive services.

[Buy the self-serve kit](https://designsy1.gumroad.com/l/toksiz) or [request a done-for-you review](https://github.com/xcapselx/repo-health-checks/issues/new?template=repo-health-check.yml).

Opening an issue is an intake request, not a purchase. Work starts only after scope, timing, and payment terms are confirmed.

## Optional Checklist Feedback

If you used the free checklist and want to share what helped or what was unclear, open a short [checklist result issue](https://github.com/xcapselx/repo-health-checks/issues/new?template=checklist-result.yml).

This is optional feedback, not a support request and not a purchase path.

## Scope Guard

This service is for focused repo cleanup and small automation fixes. Large refactors, production incident response, private data handling, and broad security audits need a separate scope.

Do not post sensitive values, recovery codes, customer data, private service details, or production access details in issues.
