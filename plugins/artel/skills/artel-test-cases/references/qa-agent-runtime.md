# QA Agent runtime and TC evidence

The coding agent reads the game source to write the case. The QA Agent reads the
case snapshot supplied to its run, selects inputs from its available tools,
observes the game, and reports a verdict. Put the starting condition, the target
of the input, and the meaning of any game-specific value in the case when they
are needed to execute or judge it. Use `authoring_guide` for the case format.

## Actions and observations

| Channel | What it gives the QA Agent | What to confirm before writing the case |
| --- | --- | --- |
| Player input | Tools such as `click`, `click_button`, and `press_key` send input to the build. | Name a target the agent can find in the current scene. Verify that the input is supported and the game reacts to it. |
| Macro, cheat, behavior | A macro repeats a sequence. A cheat can prepare a starting state. A behavior can carry out timed or repeated input. | Confirm the function is registered for the target build and enabled for the run. Keep the action under test on the gameplay path. |
| Scene and objects | `observe_scene` and `inspect_object` expose observations supplied by the SDK. `observe` names request specific game values. | Use `test_case_guide` to pick the value the game logic actually uses. Check that the run receives a readable value from the intended object. |
| Images | Vision-enabled runs can use `capture_screen`. Automatic capture depends on the run configuration and deployed version. | If the verdict depends on what the screen looks like, confirm the run can obtain an image at the required point. Each image represents one frame. |

A successful input response shows that the tool ran. Use a separate game
observation to check whether the expected result happened. For a negative case,
also identify evidence that the game received the attempt.

## Pulse values, events, and disappearing objects

- Pulse carries observations from the SDK. It samples watched state and sends
  changes. A value that changes and returns between samples can be missed. The
  SDK can also send specific events through a separate event record. Confirm
  event coverage and availability in the target run before relying on it.
- A value omitted from a delta carries no update for that value. The agent can
  still have the last value it received. Treat an explicit `gone` report, an
  inactive object, and an object missing from an incomplete or replacement
  snapshot as different observations. A case about destruction needs evidence
  of destruction, such as an explicit removal report with the right meaning
  for that case or a readable game state that confirms it.
- Past Pulse blocks in tool results can be shortened as the context grows.
  Runs with recent value history may show a sequence such as `100 → 90 → 80`.
  Confirm that the target run exposes that history if an intermediate value is
  required. The sequence shows the order in which values were observed. Use a
  target-specific event or controlled setup when the verdict depends on which
  actor or effect caused a change.

## Example: Turn count advances once

On the battle screen, confirm it is the player's turn and read the current turn
count `N`. Click the visible **End Turn** button. Wait for the build's observable
turn-transition condition, then read the same battle's turn count. The expected
value is `N + 1`. A game-specific member such as `TurnBattleSystem::TurnCount`
can supply the evidence if the target run can read it. If the source contains
that member but the build has yet to return it, classify the case as **Needs
build verification** and name the missing check. At execution time, a missing
comparison value and an observed value different from `N + 1` are distinct
results.
