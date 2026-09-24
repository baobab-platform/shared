# Foundation 4 branch protection

Every Baobab-Platform repository must protect its default `main` branch with a GitHub
ruleset. Repository administrators apply the setting because branch protection
is not source-controlled.

The minimum ruleset must:

- require a pull request before merging;
- require at least one approval and a CODEOWNER review;
- dismiss stale approvals when new commits are pushed;
- require conversation resolution;
- require the `foundation` status check and the repository's application CI;
- require branches to be up to date before merging;
- block force pushes and branch deletion; and
- apply to administrators unless an emergency bypass is explicitly audited.

The ruleset becomes enforceable after the repository's Foundation 4 pull
request has merged and the `foundation` check has completed successfully at
least once on `main`.

Enable GitHub's dependency graph before setting
`dependency_review_enabled: true` in the repository caller workflow. Trivy
dependency scanning remains mandatory regardless of that repository setting.
