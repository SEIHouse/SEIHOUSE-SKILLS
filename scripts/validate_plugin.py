"""Validate discovery, shared manifests, skill metadata, dates, and local links."""

from datetime import date
from pathlib import Path
import json
import re
from urllib.parse import unquote, urlsplit

import yaml

from build_release import IGNORED_DIRS, ROOT, release_info

EXPECTED_SKILLS = {
    'browser-synth-builder', 'creative-ui-translator', 'seihouse-planning',
    'seihouse-codebase-conventions', 'seihouse-components-performance',
    'seihouse-layout-optimization', 'seihouse-pr', 'seihouse-verification',
    'sensei-skill', 'workshop-replica',
}
SHARED_FIELDS = ('name', 'version', 'description', 'author', 'homepage',
                 'repository', 'license', 'keywords')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    generic = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    codex = json.loads((ROOT / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    version, released = release_info()
    require(generic['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
            'Unexpected general plugin schema')
    require(all(generic[key] == codex[key] for key in SHARED_FIELDS), 'Plugin manifest metadata differs')
    require(generic['repository'] == generic['homepage'] == 'https://github.com/SEIHouse/SEIHOUSE-SKILLS',
            'Repository URLs must be canonical')
    require((ROOT / codex['skills']).resolve() == ROOT / 'skills', 'Incorrect skill discovery path')
    actual = {path.name for path in (ROOT / 'skills').iterdir()
              if path.is_dir() and path.name not in IGNORED_DIRS}
    require(actual == EXPECTED_SKILLS, f'Unexpected skill discovery: {actual ^ EXPECTED_SKILLS}')
    for name in sorted(actual):
        path = ROOT / 'skills' / name / 'SKILL.md'
        text = path.read_text(encoding='utf-8')
        match = re.match(r'^---\n(.*?)\n---(?:\n|$)', text, re.DOTALL)
        require(match is not None, f'Missing YAML frontmatter: {name}')
        front = yaml.safe_load(match[1])
        require(isinstance(front, dict) and front.get('name') == name, f'Name mismatch: {name}')
        require(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)) and len(name) <= 64,
                f'Invalid skill name: {name}')
        description = front.get('description')
        require(isinstance(description, str) and 0 < len(description.strip()) <= 1024
                and '<' not in description and '>' not in description, f'Invalid description: {name}')
        metadata = front.get('metadata', {})
        require(metadata.get('version') == version, f'Incorrect skill version: {name}')
        updated = metadata.get('last_updated')
        require(isinstance(updated, str), f'Expected ISO date string: {name}')
        require(date.fromisoformat(updated) <= released, f'Skill date exceeds release date: {name}')
        print(f'PASS skill: {name} ({metadata["version"]}, {updated})')

    links = 0
    for path in ROOT.rglob('*.md'):
        if IGNORED_DIRS.intersection(path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding='utf-8')
        require('\ufffd' not in text, f'Invalid UTF-8 replacement character: {path}')
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith('#'):
                continue
            linked = (path.parent / unquote(parsed.path)).resolve()
            require(linked.is_relative_to(ROOT) and linked.is_file(), f'Broken or external local link: {path}: {target}')
            links += 1
        fence = None
        for number, line in enumerate(text.splitlines(), 1):
            require(line.rstrip(' \t') == line, f'Trailing whitespace: {path}:{number}')
            match = re.match(r'^(`{3,}|~{3,})(.*)$', line)
            if match:
                marker, suffix = match.groups()
                if fence is None:
                    fence = marker
                elif marker[0] == fence[0] and len(marker) >= len(fence) and not suffix.strip():
                    fence = None
        require(fence is None, f'Unclosed fenced code block: {path}')
        if path.name != 'MIGRATION.md':
            require(not any(name in text for name in ('plan-mode-gate', 'seihouse-gemini-verification-loop',
                                                      'seihouse-pr-review')), f'Retired invocation: {path}')
    print(f'PASS shared manifests, discovery, release {version} ({released}), and {links} local links')


if __name__ == '__main__':
    main()
