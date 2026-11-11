# TC coverage presets

Use the preset to decide which candidates deserve separate test cases. Apply
the same reach, act, and judge checks from [the skill](../SKILL.md) to every
candidate. Give each case one primary outcome to judge. The examples below
illustrate scope. Confirm the actual paths and observations on the target build.

## Build smoke

Use for requests such as "Check that this build starts and I can get into a
game." Cover the shortest supported path through startup to playable state.
Choose independently observable checkpoints where a failure blocks entry, such
as the main menu appearing and the first playable scene becoming ready. Stop
once the player can begin playing. Record any part of startup the QA agent
cannot reach or judge, such as process launch when the session attaches after
launch.

## Core gameplay flows

Use for requests such as "Check that players can finish the main things they
do in this game." Select one representative path per key player goal from the
game requirements and scope, such as completing the tutorial, winning the
first match, or claiming its reward. Write a separate case for each major
checkpoint where a failure would block progress, and for the goal's observable
outcome. If the selected path starts a new game, include separate cases for
the title screen appearing, the new-game action starting a new session, and
entry into the first playable encounter or equivalent. Keep these as explicit
verdicts when they also serve as preconditions for later cases.

Include alternate routes or conditions when the user requests them or they
define a distinct in-scope goal.

## Screen-by-screen checks

Use for requests such as "Open each settings screen and check that its main
control works." Enumerate the player-facing screens or panels in scope. For
each, check entry and the observable result of a representative interaction
where one exists. Separate those checks when each has an independent verdict.
For example, confirm that the spell selection panel opens, then confirm that
selecting a spell marks it as selected. Expand to additional controls or
screen states when requested.

## Exhaustive content coverage

Use for requests such as "Check that every spell works." Enumerate the items
in the requested scope from the target build and game requirements or data.
For each item, choose a representative use and verify the observable outcome
that establishes that item's expected behavior. For example, check that a
healing spell restores health and that a shielding spell grants a shield.
Keep items whose use or outcome cannot be verified visible in the coverage
report. If the item list is incomplete, state which part was identified and
where the inventory is incomplete. Include additional conditions and item
combinations only when requested or necessary to establish the item's expected
behavior.

## Area-specific requests

"Check the main gameplay, open every settings screen, and test every spell"
uses Core gameplay flows for the game overall, Screen-by-screen checks for
settings, and Exhaustive content coverage for spells. Keep the shared steps
needed to complete a core flow. Reuse a case where it establishes the same
primary outcome under the same conditions.
