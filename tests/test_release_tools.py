"""Exercise local-cache exclusion without excluding real package documentation."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_release
import validate_plugin


class LocalFilesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'plugin'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(*build_release.IGNORED_DIRS))
        for module in (build_release, validate_plugin):
            current = patch.object(module, 'ROOT', self.root)
            current.start()
            self.addCleanup(current.stop)

    def validate(self):
        with redirect_stdout(StringIO()):
            validate_plugin.main()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def test_local_caches_do_not_change_bundle_or_validation(self):
        expected = build_release.bundle_bytes()
        for name in ('.cache/report.md', '.venv/report.md', 'node_modules/report.md',
                     'scripts/.cache/run.log', 'scripts/__pycache__/module.pyc',
                     'skills/.cache/report.md', 'tests/.venv/report.md'):
            self.write(name, '[broken](missing-file.md)  \n')
        self.validate()
        self.assertEqual(build_release.bundle_bytes(), expected)
        build_release.check_bundle()

    def test_package_docs_are_still_checked_by_component(self):
        for name in ('zip/report.md', 'skills/sensei-skill/references/report.md',
                     'skills/sensei-skill/references/.cache-not-a-directory-name/report.md'):
            with self.subTest(path=name):
                path = self.write(name, '[broken](missing-file.md)\n')
                try:
                    with self.assertRaisesRegex(ValueError, 'Broken or external local link'):
                        self.validate()
                finally:
                    path.unlink()


if __name__ == '__main__':
    unittest.main()
