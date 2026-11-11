#!/usr/bin/env python3
"""Print the asset paths that serialized fields in a Unity scene, prefab or asset point to.

A field in a .unity, .prefab or .asset file names its target by guid, for example
`levels: - {fileID: 4900000, guid: dc5d..., type: 3}`. The guid belongs to the target's
.meta file. This script resolves every guid by reading each .meta file itself and prints
each reference beside the file it points to, in the order the field lists them.

Why a script: matching guids by hand is error-prone. In Claude Code's shell, `grep`
over several files returns matches in a different order on every run, and
`grep -h` drops the file name that would reveal the mix-up.

Usage:
  python3 unity-refs.py <project root> <scene, prefab or asset path>
  python3 unity-refs.py <project root> <path> --field levels
  python3 unity-refs.py <project root> <path> --component LevelLoader

Output, one line per reference:
  <GameObject> / <component script> . <field>[<index>] -> <asset path>

Standard library only. Reads files; changes nothing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DOCUMENT = re.compile(r"^--- !u!(\d+) &(-?\d+)", re.M)
REFERENCE = re.compile(r"\{fileID: (-?\d+), guid: ([0-9a-f]{32}), type: \d+\}")
KEY = re.compile(r"^(\s*)(?:- )?([A-Za-z_][\w]*):")
GUID_LINE = re.compile(r"^guid: ([0-9a-f]{32})", re.M)
NAME = re.compile(r"^\s+m_Name: (.*)$", re.M)
OWNER = re.compile(r"^\s+m_GameObject: \{fileID: (-?\d+)\}", re.M)
SCRIPT = re.compile(r"^\s+m_Script: \{fileID: -?\d+, guid: ([0-9a-f]{32})", re.M)
MONO_BEHAVIOUR = "114"
GAME_OBJECT = "1"
# Guids of Unity's built-in resources (default material, default skybox). They have no .meta file.
BUILT_IN = {"0000000000000000e000000000000000", "0000000000000000f000000000000000"}
# Class ids of common built-in components. Others are printed by number.
CLASS_NAMES = {
    "4": "Transform", "20": "Camera", "23": "MeshRenderer", "82": "AudioSource", "95": "Animator",
    "104": "RenderSettings", "108": "Light", "212": "SpriteRenderer", "222": "CanvasRenderer",
    "223": "Canvas", "224": "RectTransform", "1001": "PrefabInstance",
}


def guid_paths(root: Path) -> dict[str, str]:
    """guid -> asset path (without `.meta`), read from each .meta file under Assets and Packages."""
    paths: dict[str, str] = {}
    # Library/PackageCache holds the scripts of installed packages (TextMeshPro and others); skipped when absent.
    for folder in ("Assets", "Packages", "Library/PackageCache"):
        base = root / folder
        if not base.is_dir():
            continue
        for meta in sorted(base.rglob("*.meta")):
            found = GUID_LINE.search(meta.read_text(encoding="utf-8", errors="ignore"))
            if found:
                paths[found.group(1)] = str(meta.relative_to(root))[: -len(".meta")]
    return paths


def documents(text: str) -> list[tuple[str, str, str]]:
    """(class id, file id, body) for each YAML document, in file order."""
    marks = list(DOCUMENT.finditer(text))
    out = []
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        out.append((mark.group(1), mark.group(2), text[mark.end() : end]))
    return out


def references(body: str) -> list[tuple[str, int, str]]:
    """(field path, list index or -1, guid) for each guid reference in one document body."""
    out = []
    stack: list[tuple[int, str]] = []
    counters: dict[str, int] = {}
    for line in body.splitlines():
        key = KEY.match(line)
        if key:
            indent = len(key.group(1))
            while stack and stack[-1][0] >= indent:
                stack.pop()
            stack.append((indent, key.group(2)))
        refs = REFERENCE.findall(line)
        if not refs:
            continue
        # The top key names the document type (`MonoBehaviour:`, `PrefabInstance:`), so it is left out of the path.
        path = ".".join(name for depth, name in stack if depth > 0) or "?"
        listed = line.lstrip().startswith("- ") and not key
        for _, guid in refs:
            if listed:
                index = counters.get(path, 0)
                counters[path] = index + 1
            else:
                index = -1
            out.append((path, index, guid))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("root", help="Unity project root (the folder that holds Assets/)")
    parser.add_argument("path", help="scene, prefab or asset file, relative to the root or absolute")
    parser.add_argument("--field", help="only fields whose path contains this name")
    parser.add_argument("--component", help="only components whose script file name contains this")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    target = Path(args.path)
    if not target.is_absolute():
        target = root / target if (root / target).is_file() else target.resolve()
    if not target.is_file():
        print(f"not a file: {target}", file=sys.stderr)
        return 2

    if not target.read_bytes()[:5] == b"%YAML":
        # A project whose Asset Serialization is not Force Text saves scenes and prefabs as binary. Reading one as text
        # finds nothing, and taking that as "no references" would be wrong.
        print(
            f"{target} is binary-serialized, not text YAML: its references cannot be read from the file. "
            "Do not guess them; mark facts that depend on this file 'Confirm by running'.",
            file=sys.stderr,
        )
        return 3

    paths = guid_paths(root)
    docs = documents(target.read_text(encoding="utf-8", errors="ignore"))
    names = {}
    for class_id, file_id, body in docs:
        if class_id == GAME_OBJECT:
            found = NAME.search(body)
            names[file_id] = found.group(1).strip() if found else "?"

    printed = 0
    for class_id, _, body in docs:
        owner = OWNER.search(body)
        owner_name = names.get(owner.group(1), "?") if owner else "?"
        script = SCRIPT.search(body) if class_id == MONO_BEHAVIOUR else None
        if script:
            script_name = Path(paths.get(script.group(1), "?")).stem
        else:
            script_name = CLASS_NAMES.get(class_id, f"class {class_id}")
        if args.component and args.component not in script_name:
            continue
        for field, index, guid in references(body):
            if field.endswith("m_Script") or field.endswith("m_CorrespondingSourceObject"):
                continue
            if args.field and args.field not in field:
                continue
            slot = f"[{index}]" if index >= 0 else ""
            if guid in BUILT_IN:
                where = "(Unity built-in resource)"
            else:
                where = paths.get(guid, f"guid {guid} (no .meta found)")
            print(f"{owner_name} / {script_name} . {field}{slot} -> {where}")
            printed += 1
    if not printed:
        print("no matching references", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
