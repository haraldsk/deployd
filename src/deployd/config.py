from typing import List, TypedDict


REPO_LOCAL_ROOT = "/tmp"


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
            )
        ]

    @property
    def list(self) -> List[RepoConfig]:
        return self._repoconfigs
