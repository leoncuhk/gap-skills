#!/usr/bin/env python3
"""Validate terra skill files: frontmatter, naming, cross-references, template JSON."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
errors = []

skill_names = set(os.listdir(SKILLS))
total_lines = 0

for name in sorted(skill_names):
    path = os.path.join(SKILLS, name, "SKILL.md")
    if not os.path.isfile(path):
        errors.append(f"skills/{name}: missing SKILL.md")
        continue
    text = open(path).read()
    total_lines += text.count("\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        errors.append(f"{path}: missing frontmatter block")
        continue
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    if fm.get("name") != name:
        errors.append(f"{path}: frontmatter name '{fm.get('name')}' != directory '{name}'")
    if len(fm.get("description", "")) < 20:
        errors.append(f"{path}: description too short")
    body = m.group(2)
    # every referenced terra-* skill must exist
    for ref in set(re.findall(r"`(terra[a-z-]*)`", body)):
        if ref not in skill_names:
            errors.append(f"{path}: references unknown skill '{ref}'")

# core spec must define every tag the other skills use
core = open(os.path.join(SKILLS, "terra", "SKILL.md")).read()
for tag in ["KU", "UK", "UU?", "[H]", "[A]"]:
    if tag not in core:
        errors.append(f"terra/SKILL.md: tag {tag} not defined in core spec")

# templates must be valid
json.load(open(os.path.join(ROOT, "templates", "settings-template.json")))

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK — {len(skill_names)} skills valid, {total_lines} combined lines")
