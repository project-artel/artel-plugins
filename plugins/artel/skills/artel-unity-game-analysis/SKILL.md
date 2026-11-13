---
name: artel-unity-game-analysis
description: >-
  Analyze Unity game data in a project checkout. Use when a game behavior,
  asset relationship, level order, or starting value needs evidence from a
  Unity scene, prefab, ScriptableObject, or serialized asset.
---

# Unity game data analysis

## Resolve serialized asset references

Scenes, prefabs, and ScriptableObjects refer to external assets by GUID. Use
[`scripts/unity-refs.py`](scripts/unity-refs.py) to resolve those GUIDs through
`.meta` files and preserve the order of references in serialized lists.

```sh
python3 <this skill>/scripts/unity-refs.py <project root> <scene, prefab or asset> [--field <name>] [--component <script name>]
```

The output maps `<GameObject> / <component script> . <field>[<index>]` to the
asset path. For fields that reference other assets, inspect the resolved assets
to establish the requested fact.

- If the script is unavailable, search for one GUID at a time in `.meta` files
  and keep the matching file paths in the output. Preserve the order from the
  serialized field. Search result order can vary between runs.
- When a file does not begin with `%YAML`, this script cannot inspect its
  references. State what could not be verified and identify what to check in
  the Unity Editor or target build. Treat a GUID without a matching `.meta`
  file as unresolved.

## Record evidence for shared facts

When several ARTEL test cases depend on the same game data fact, record it once
in the game repository's `artel/game-knowledge.md`. Create the file if needed.
Include the matching script output line or `file:line` in the evidence column.
