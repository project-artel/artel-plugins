---
name: artel-test-cases
description: >-
  Create, revise, or review ARTEL automated QA test cases against a target game build.
  Use when the user asks to create test cases or TCs, including TC 만들어줘,
  테스트 케이스 작성, and TC 검토. For creation requests, author and review the cases,
  then register Authorable cases in ARTEL through MCP or the CLI unless the user
  requests only a draft, review, or local files. Also use for QA feasibility reviews
  and deciding whether existing or small test-only cheats or behaviors can make a
  case runnable. Covers ARTEL QA cases rather than Unity EditMode or PlayMode tests.
---

# ARTEL automated QA test cases

As the coding agent, author cases and review them before saving. The QA agent runs
them in the game build. Base each case on the controls and evidence available to
the QA agent, even when you can see more in the source.

Read [the QA Agent runtime reference](references/qa-agent-runtime.md) before
deciding whether a target build and run can reach, perform, and judge a case.

## Coverage selection

Before generating new cases, use [references/coverage-presets.md](references/coverage-presets.md)
to translate the user's request into a coverage preset for each area. Apply
explicit area instructions first. Default to Core gameplay flows where the user
has left the depth open. Ask one focused question only if two plausible
interpretations would materially change the case list. Honor explicit requests
for particular conditions or variants within the chosen scope.

Report the preset and scope used for each area alongside the cases. For
exhaustive content coverage, report how many identified items have authorable
cases and name items whose cases still need verification or are deferred.

## Candidate selection

1. Identify the project and target build. Review existing cases and state names;
   reuse a matching case instead of duplicating it. Use ARTEL's `authoring_guide`
   for case format and `test_case_guide` when choosing SDK `observe` values.
2. Take the intended result from the user's request or spec. Use code and build
   evidence to establish these three parts:
   - **Reach:** Identify the starting screen and a repeatable way to meet its
     preconditions.
   - **Act:** Name the player input, macro, or behavior the QA agent can actually
     use. For an automatic event with a lasting result, specify when to start
     observing and when to check the result.
   - **Judge:** Name the visible result or readable SDK value, when to read it,
     and what separates pass from fail. Where other actions or targets could
     produce the same evidence, tie it to the intended action and target.
3. Keep the specified expected result when code suggests a defect. Flag the
   discrepancy. Keep any narrower, independently verifiable result in a
   separate case.

## Facts read from game data

Scenes, prefabs, and ScriptableObjects name the assets they use by guid, not by file
name. Resolve those references with
[the reference script](references/unity-refs.py) rather than by matching guids
yourself:
`python3 <this skill>/references/unity-refs.py <project root> <scene, prefab or asset> [--field <name>]`.
It prints each reference beside the asset file it points to, in list order, such as
`LevelLoader / LevelLoader . levels[0] -> Assets/Resources/Levels/level0.txt`.

- Without the script, look up one guid at a time and keep the file name in the
  output: `grep -rl "guid: <guid>" --include=*.meta Assets`. Never pair values from a
  search over several files by the order of its output. In Claude Code's shell,
  `grep` over several files returns them in a different order on each run, and `-h`
  hides the file names that would show the mix-up.
- A scene or prefab saved as binary (the file does not begin with `%YAML`) cannot be
  read this way. Do not guess its contents. Mark the cases that depend on it
  **Confirm by running**.
- When several cases rest on one fact read from data, such as which level comes
  first, a level's layout, or a starting value, record the fact once with its
  evidence (the script's output line or `file:line`). Use the evidence column of the
  game knowledge file (`artel/game-knowledge.md`) when the project keeps one, and
  your notes otherwise. During review, derive each such fact again without reading
  the recorded evidence first, then compare. On a mismatch, fix the record and every
  case that rests on it.

## Momentary events

Exclude short-lived events as standalone automated QA cases when the verdict
depends on catching them in a screenshot or sampled value. Examples include a
projectile crossing the screen, a brief hit effect, and a short animation. A
structured event can support a case if the target run receives it and it is
still readable at verdict time. List cases without that evidence as manual
checks when coverage is needed. A lasting result may be a separate case if the
QA agent can attribute it to the action and target. Report only the outcome that
case checks.

## Before-and-after comparisons

State how the QA agent obtains both the baseline and the comparison. For actual
damage, identify the attack source, the target, and the damage applied by that hit.
Match or account for target defense, critical hits, and buffs. A displayed attack
stat or a combined damage total cannot establish the applied damage of a specific
hit. If the build exposes only the stat, cover it as a separate UI case and defer
the damage case.

## Test support

Reuse existing controls, observations, macros, cheats, and behaviors first.
Add a small, localized cheat or behavior within existing test support if it can
unblock a case without changing core gameplay. Follow the `artel-cheats` or
`artel-behaviors` skill for implementation.

- Use cheats to prepare the starting state. Keep the action under test and its
  outcome on the real gameplay path.
- Use behaviors for timed or repeated inputs. Preserve the actual input path
  when the input binding itself is under test. Judge the game result separately
  from the tool's success response.
- Confirm new test support is registered and works in the target development
  build before relying on it. Use `list_game_functions` when available to check
  registration.

New practice arenas, dedicated targets and reset systems, shared recording or
telemetry infrastructure, new dependencies, and core gameplay changes require
an explicit user request. Defer the affected cases and explain the missing
evidence while that work is outside scope.

## Review before saving

Review the draft separately from authoring. Using only what the QA agent can
access, walk through the starting state, action, and verdict. Check negative
cases for evidence that the game received the attempt; an unchanged state
alone may also mean the agent missed the input.

- **Authorable:** There is evidence for reach, act, and judge in the target build.
- **Confirm by running:** The path is plausible but the action or evidence
  has not been confirmed for that build. Name the check still needed.
- **Deferred:** An action, starting condition, or observation is missing, or
  the case depends on a momentary event. Record why and, where useful, suggest
  manual coverage or the minimum support that would unblock it.

Submit only authorable cases using the ARTEL registration workflow below.
Report the other candidates and reasons separately. Authorability, console
review status, and an actual QA verdict are separate results.

Read [references/few-shot.md](references/few-shot.md) for examples when applying
these rules to timing, blocked actions, mixed damage, or test support decisions.

## ARTEL registration workflow

Treat a request to create ARTEL test cases as a request to author, review, and
register them in ARTEL through MCP or the CLI. If the user asks only for a draft,
review, or local files, follow that scope instead. Local files may support
registration, but creating them alone does not complete a registration request.

1. Before authoring, use the connected ARTEL MCP tools to identify the target
   project and inspect existing cases and folders. Follow the user's requested
   organization and reuse matching cases. Use the ARTEL CLI when MCP is
   unavailable or lacks a required operation, or when the user requests the CLI;
   read [the CLI skill](../artel-cli/SKILL.md) for its workflow.
2. After the review above, register only Authorable cases in the target project
   and requested folders. Report Confirm by running and Deferred candidates
   separately with their missing prerequisites; do not register them as runnable
   cases.
3. Read back each created case through MCP or the CLI and compare its scene,
   precondition, step, expectedValue, and folder assignment with the reviewed
   content. If creation partially fails, inspect the existing results before
   retrying so successful cases are not duplicated.
4. Report the target project, created case IDs, folder assignment, and read-back
   result. Distinguish registration from an actual QA execution result. If no
   cases are Authorable, explain why none were registered. If neither MCP nor the
   CLI can complete registration, report the blocker and any completed work
   instead of treating local files as completion.
