import os
import getpass
import datetime
import re
from packaging import version


_SEMVER_RE = re.compile(r'(\d+\.\d+\.\d+)')
_PAREN_V_RE = re.compile(r'\(v([^)]+)\)')


def normalize_hashcat_version(raw: str) -> str:
    raw = (raw or '').strip()
    if not raw:
        return ''

    # Prefer a short semantic version in the UI (e.g. 7.1.2).
    semver = extract_semver(raw)
    if semver:
        return semver

    # Fallback to parenthesized and first-line formats when no semver is found.
    m = _PAREN_V_RE.search(raw)
    if m:
        return m.group(1).strip()

    first_line = raw.splitlines()[0].strip()
    return first_line


def extract_semver(raw: str) -> str:
    raw = (raw or '').strip()
    m = _SEMVER_RE.search(raw)
    return m.group(1) if m else ''


class SystemManager:
    def __init__(self, shell, settings):
        self.shell = shell
        self.settings = settings

    def run_updates(self):
        self.update_hashcat_version()
        self.update_git_hash_version()
        self.update_autoid()

    def update_autoid(self):
        current_version_raw = self.settings.get('hashcat_version', '').strip()
        current_semver = extract_semver(current_version_raw)
        has_autoid = False
        if current_semver:
            minimum_version = '6.2.3'
            try:
                if version.parse(current_semver) >= version.parse(minimum_version):
                    has_autoid = True
            except version.InvalidVersion:
                has_autoid = False

        self.settings.save('hashcat_autoid', 1 if has_autoid else 0)
        return True

    def update_hashcat_version(self):
        hashcat_binary = self.settings.get('hashcat_binary', '')
        if len(hashcat_binary) == 0:
            return False
        elif not os.path.isfile(hashcat_binary):
            return False
        elif not os.access(hashcat_binary, os.X_OK):
            return False

        raw = self.shell.execute([hashcat_binary, '--version'], user_id=0)
        normalized = normalize_hashcat_version(raw)
        if raw:
            self.settings.save('hashcat_version_raw', raw)
        if normalized:
            self.settings.save('hashcat_version', normalized)
        return True

    def update_git_hash_version(self):
        git_binary = self.shell.execute(['which', 'git'], user_id=0)
        if len(git_binary) == 0:
            return False

        # Save latest commit short hash.
        version = self.shell.execute(['git', 'rev-parse', '--short', 'HEAD'], user_id=0)
        self.settings.save('git_hash_version', version)

        # Save commit count on the master branch (like a version tracker).
        try:
            count = int(self.shell.execute(['git', 'rev-list', '--count', 'master'], user_id=0))
        except ValueError:
            count = 0
        self.settings.save('git_commit_count', count)

        # Save last commit date.
        try:
            last_commit_timestamp = int(self.shell.execute(['git', 'log', '-1', '--format=%at'], user_id=0))
        except ValueError:
            last_commit_timestamp = 0

        last_commit_date = ''
        if last_commit_timestamp > 0:
            last_commit_date = datetime.datetime.fromtimestamp(last_commit_timestamp).strftime('%Y-%m-%d %H:%M')
        self.settings.save('last_commit_date', last_commit_date)

        return True

    def get_system_user(self):
        return getpass.getuser()

    def get_system_user_home_directory(self, user=""):
        if len(user) == 0:
            user = self.get_system_user()

        return self.shell.execute(['/bin/bash', '-c', 'eval echo ~' + user], user_id=0)
