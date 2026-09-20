# Foundation CI support policy

## Supported consumers

Foundation CI is distributed from the private `baobab-platform/shared` repository. GitHub permits this reuse only where the caller can access private organization workflows. The supported production estate is therefore:

- private Baobab repositories;
- internal repositories where the organization plan and policy permit access; and
- exact immutable commit-SHA references.

Public repositories are not supported callers while `shared` remains private. A public repository must be made private before its Foundation caller is enabled. The rollout inventory must treat a workflow that never starts as an access/configuration failure, not as a successful or not-applicable gate.

## Promotion requirements

A Foundation revision is promotable only after all of the following are green:

1. workflow and contract static validation in `shared`;
2. the `shared` self-consumer run;
3. one representative private consumer for every activated runtime or artifact class;
4. verification of the exact emitted result check name; and
5. consumer references pinned to the promoted commit SHA.

The stable reusable entry point remains `.github/workflows/foundation-repository-gates.yml`. Consumers must not reference its internal component workflows directly.

## Required check

The consumer's caller job id becomes part of GitHub's displayed check context. Use a consistent caller job id of `foundation`. Rulesets must be configured from the check emitted by a successful pilot run, rather than from a guessed display name.

## Failure ownership

A run that does not create jobs is a Foundation distribution or GitHub configuration defect. A started gate reporting `misconfigured` is a repository contract defect. A started applicable gate reporting `failed` is a policy or repository defect. Only an explicit classifier decision may make a control not applicable.
