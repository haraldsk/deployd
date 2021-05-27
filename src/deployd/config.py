from typing import List, TypedDict


REPOS_ROOT = "/tmp"
MANIFESTS_PATH = "deploy/manifests"


class RepoConfig(TypedDict):
    name: str
    namespace: str
    location: str

class RepoConfigs():
    def __init__(self) -> None:
        self._repoconfigs: List[RepoConfig] = [
            RepoConfig(
                name="haraldsk/an-application",
                namespace="haraldsk",
                location="https://github.com/haraldsk/an-application",
            ),
            RepoConfig(
                name="haraldsk/an-other-application",
                namespace="haraldsk",
                location="https://github.com/haraldsk/an-other-application",
            ),
        ]

    @property
    def list(self) -> List[RepoConfig]:
        return self._repoconfigs
