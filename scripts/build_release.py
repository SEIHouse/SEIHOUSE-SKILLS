"""Build or check the current deterministic, dated plugin download."""

from datetime import date
from io import BytesIO
from pathlib import Path
import argparse
import json
import posixpath
import re
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = (
    '.gitattributes', '.gitignore', 'README.md', 'CHANGELOG.md', 'MIGRATION.md',
    'plugin.json', 'requirements-dev.txt',
)
SOURCE_DIRS = ('.codex-plugin', 'skills', 'scripts', 'tests', '.github')


def release_info():
    manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    version = manifest['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Expected a stable semantic version in plugin.json')
    entry = re.search(r'^## \[([^\]]+)\] - (\d{4}-\d{2}-\d{2})$',
                      (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8'), re.MULTILINE)
    if not entry or entry[1] != version:
        raise ValueError('Latest changelog entry must match the manifest version')
    return version, date.fromisoformat(entry[2])


def source_files():
    paths = [ROOT / name for name in ROOT_FILES]
    for folder in SOURCE_DIRS:
        paths.extend(path for path in (ROOT / folder).rglob('*')
                     if path.is_file() and '__pycache__' not in path.parts
                     and path.suffix not in ('.pyc', '.pyo'))
    for path in paths:
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            raise ValueError(f'Missing or unsafe source: {path}')
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def source_bytes(path):
    # All current package source is UTF-8 text; normalize checkout line endings so
    # Windows and Linux produce the same bundle. ZIP archives are excluded above.
    return path.read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8')


def bundle_path():
    version, released = release_info()
    return ROOT / 'zip' / f'seihouse-skills-v{version}-{released.isoformat()}.zip'


def bundle_bytes():
    _, released = release_info()
    result = BytesIO()
    with zipfile.ZipFile(result, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in source_files():
            entry = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(),
                                    (released.year, released.month, released.day, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, source_bytes(path), compresslevel=9)
    return result.getvalue()


def check_bundle():
    # Compare payload and deterministic metadata, allowing Python/zlib versions
    # to produce different compressed byte streams for the same source.
    destination = bundle_path()
    _, released = release_info()
    expected = {path.relative_to(ROOT).as_posix(): source_bytes(path) for path in source_files()}
    for name, payload in expected.items():
        if not name.endswith('.md'):
            continue
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', payload.decode('utf-8')):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith('#'):
                continue
            linked = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(parsed.path)))
            if linked not in expected:
                raise ValueError(f'Broken bundled reference in {name}: {target}')
    with zipfile.ZipFile(destination) as archive:
        entries = archive.infolist()
        if [entry.filename for entry in entries] != list(expected):
            raise ValueError('Download file list/order differs from current source')
        for entry in entries:
            if archive.read(entry) != expected[entry.filename]:
                raise ValueError(f'Stale bundled file: {entry.filename}')
            if entry.date_time != (released.year, released.month, released.day, 0, 0, 0):
                raise ValueError(f'Incorrect release timestamp: {entry.filename}')
            if entry.create_system != 3 or entry.external_attr != 0o100644 << 16:
                raise ValueError(f'Incorrect release permissions: {entry.filename}')
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare the current ZIP with source without writing')
    args = parser.parse_args()
    if args.check:
        count = check_bundle()
        print(f'PASS dated bundle matches {count} source files: {bundle_path().name}')
    else:
        destination = bundle_path()
        destination.parent.mkdir(exist_ok=True)
        destination.write_bytes(bundle_bytes())
        print(f'Built {destination.name} ({check_bundle()} files)')


if __name__ == '__main__':
    main()
