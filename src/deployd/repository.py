import git
import logging
import os

from typing import List
from .config import RepoConfig, REPOS_ROOT

logger = logging.getLogger(__name__)

class Repository():
    def __init__(self,
                 name: str,
                 remote: str,) -> None:
        self._name = name
        self._remote = remote

        self._path = os.path.join(REPOS_ROOT, self._name)
        try:
            self._repo = git.Repo.clone_from(self._remote, self._path)
        except git.GitCommandError:
            logger.error(f"Could not clone {self._remote} into {self._path}")
        self._head = self._repo.head.commit.tree
        self._updated = False

    def update(self) -> bool:
        logger.info(f"calling update on {self._name}")
        try:
            self._repo.remotes.origin.pull()
        except git.GitCommandError:
            logger.error(f"Could not update git repo in {self._path}")
            return False
        # updated
        if self._head != self._repo.head.commit.tree:
            self._updated = True
            self._head = self._repo.head.commit.tree

        return self._updated

    @property
    def name(self) -> str:
        return self._name

    @property
    def updated(self) -> bool:
        return self._updated

    def clear_updated(self) -> None:
        self._updated = False


class Repositories():

    def __init__(self, repoconfigs: List[RepoConfig]) -> None:
        self._repos: List[Repository] = []

        for rc in repoconfigs:
            self._repos.append(Repository(name=rc["name"], remote=rc["location"],))

    @property
    def list(self) -> List[Repository]:
        return self._repos

    def update(self) -> None:
        logger.debug(f"calling update on {self._repos}")

        for r in self._repos:
            r.update()

    @property
    def updated(self) -> List[Repository]:
        return [repo for repo in self._repos if repo.updated]

    def get_from_name(self, name: str,) -> Repository:
        return [repo for repo in self.list if repo.name == name][0]
