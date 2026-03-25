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


class HashcatHelpParsingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        manager_path = Path(__file__).resolve().parents[1] / "app" / "lib" / "hashcat" / "manager.py"
        self.mod = _load_module(manager_path, "hashcat_manager_mod")

    def test_parse_hash_modes_header_is_case_insensitive(self) -> None:
        HashcatManager = self.mod.HashcatManager

        class _Shell:
            def __init__(self, out: str):
                self._out = out

            def execute(self, cmd, user_id=0, log_to_db=False):
                return self._out

        fake = """
hashcat (v7.1.2) starting in help mode

- [ Hash Modes ] -

      # | Name                                                       | Category
  ======+============================================================+======================================
    900 | MD4                                                        | Raw Hash
      0 | MD5                                                        | Raw Hash

- [ Brain Client Features ] -
"""
        m = HashcatManager(shell=_Shell(fake), hashcat_binary="hashcat", hashid=None)
        parsed = m.get_supported_hashes()
        self.assertEqual(parsed.get("Raw Hash", {}).get("900"), "MD4")
        self.assertEqual(parsed.get("Raw Hash", {}).get("0"), "MD5")

    def test_parse_stops_on_next_section_header(self) -> None:
        HashcatManager = self.mod.HashcatManager

        class _Shell:
            def __init__(self, out: str):
                self._out = out

            def execute(self, cmd, user_id=0, log_to_db=False):
                return self._out

        fake = """
- [ Hash Modes ] -

      # | Name | Category
  ======+======+=========
      0 | MD5  | Raw Hash
- [ Options ] -
 Options Short / Long | Type | Description
"""
        m = HashcatManager(shell=_Shell(fake), hashcat_binary="hashcat", hashid=None)
        parsed = m.get_supported_hashes()
        self.assertEqual(parsed.get("Raw Hash", {}).get("0"), "MD5")


if __name__ == "__main__":
    unittest.main()

