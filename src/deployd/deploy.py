import os
import logging
import subprocess

from typing import List
from .config import RepoConfig, REPO_LOCAL_ROOT

logger = logging.getLogger(__name__)

class Deployment():
    def __init__(self, name, namespace,) -> None:
        self._name = name
        self._namespace = namespace
        self._path = os.path.join(REPO_LOCAL_ROOT, self._name)

    def apply(self):
        command: List[str] = f"kubectl apply -k {self._path}/deploy/manifests".split(" ")
        logging.info(f"running {command}")
        proc: subprocess.CompletedProcess = subprocess.run(command)
        print(proc.stdout)

    def status(self):
        pass

    @property
    def name(self):
        return self._name

class Deployments():
    def __init__(self, repoconfigs: List[RepoConfig]) -> None:
        self._deploys: List[Deployment] = []

        for rc in repoconfigs:
            self._deploys.append(Deployment(name=rc["name"], namespace=rc["namespace"]))

    @property
    def list(self) -> List[Deployment]:
        return self._deploys

    def apply(self):
        for deploy in self.list:
            # check if deployed before
            # apply
            deploy.apply()
            # set status
