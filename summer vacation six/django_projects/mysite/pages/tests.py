from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase, override_settings

from .views import _find_reference_file, _parent_level_for_topic


class ReferenceFileLookupTests(SimpleTestCase):
    def test_parent_level_for_topic_supports_old_submission_names(self):
        self.assertEqual(
            _parent_level_for_topic("chapter-1-level-1-1"),
            "chapter-1-level-1",
        )

    def test_find_reference_file_resolves_matching_parent_level_file(self):
        with TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            references_dir = base_dir / "references"
            references_dir.mkdir()
            ref_file = references_dir / "chapter-1-level-1.pkl"
            ref_file.write_bytes(b"reference")

            with override_settings(BASE_DIR=base_dir):
                found_path, found_level = _find_reference_file("chapter-1-level-1")

        self.assertEqual(found_path, ref_file)
        self.assertEqual(found_level, "chapter-1-level-1")

    def test_find_reference_file_resolves_old_topic_level_to_parent_file(self):
        with TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            references_dir = base_dir / "references"
            references_dir.mkdir()
            ref_file = references_dir / "chapter-1-level-1.pkl"
            ref_file.write_bytes(b"reference")

            with override_settings(BASE_DIR=base_dir):
                found_path, found_level = _find_reference_file("chapter-1-level-1-1")

        self.assertEqual(found_path, ref_file)
        self.assertEqual(found_level, "chapter-1-level-1")

    def test_find_reference_file_keeps_old_fallback_for_non_level_one_names(self):
        with TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            references_dir = base_dir / "references"
            references_dir.mkdir()
            ref_file = references_dir / "chapter-1-level-2-1.pkl"
            ref_file.write_bytes(b"reference")

            with override_settings(BASE_DIR=base_dir):
                found_path, found_level = _find_reference_file("chapter-1-level-2")

        self.assertEqual(found_path, ref_file)
        self.assertEqual(found_level, "chapter-1-level-2-1")
