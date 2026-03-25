import importlib.util
import unittest
from pathlib import Path


def _load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec for {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class HashcatVersionNormalizationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        system_path = Path(__file__).resolve().parents[1] / "app" / "lib" / "base" / "system.py"
        self.mod = _load_module(system_path, "system_mod")

    def test_normalize_hashcat_version_from_plain_version(self) -> None:
        normalize = self.mod.normalize_hashcat_version
        self.assertEqual(normalize("v7.1.2-382-g2d71af371"), "v7.1.2-382-g2d71af371")

    def test_normalize_hashcat_version_from_parenthesized(self) -> None:
        normalize = self.mod.normalize_hashcat_version
        raw = "hashcat (v7.1.2-382-g2d71af371) starting in help mode"
        self.assertEqual(normalize(raw), "v7.1.2-382-g2d71af371")

    def test_extract_semver(self) -> None:
        extract = self.mod.extract_semver
        self.assertEqual(extract("v7.1.2-382-g2d71af371"), "7.1.2")
        self.assertEqual(extract("hashcat (v6.2.5) starting"), "6.2.5")
        self.assertEqual(extract(""), "")


if __name__ == "__main__":
    unittest.main()

