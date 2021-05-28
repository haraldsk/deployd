import os
import logging
import subprocess
import json

from typing import List, Optional
from .config import RepoConfig, REPOS_ROOT, MANIFESTS_PATH

logger = logging.getLogger(__name__)

class Deployment():
    def __init__(self, name: str, namespace: str,) -> None:
        self._name = name
        self._namespace = namespace
        self._path = os.path.join(REPOS_ROOT, self._name, MANIFESTS_PATH)

    def apply(self) -> bool:
        command: List[str] = f"kubectl apply --namespace {self._namespace} -f {self._path}".split(" ")

        logger.debug(f"running {command}")
        deploy: subprocess.CompletedProcess = subprocess.run(command, stdout=subprocess.PIPE)

        if deploy.returncode == 0:
            return True

        logger.error(deploy.stdout)
        return False

    def get(self) -> Optional[dict]:
        command: List[str] = f"kubectl get --namespace {self._namespace} -f {self._path} -o json".split(" ")

        logger.debug(f"running {command}")
        deploy: subprocess.CompletedProcess = subprocess.run(command, stdout=subprocess.PIPE)

        try:
            json_dict = json.loads(deploy.stdout)
        except json.JSONDecodeError as e:
            logger.error(e.msg)
            return None

        if deploy.returncode == 0:
            return json_dict

        return None

    @property
    def name(self):
        return self._name

class Deployments():
    def __init__(self, repoconfigs: List[RepoConfig],) -> None:
        self._deploys: List[Deployment] = []

        for rc in repoconfigs:
            self._deploys.append(Deployment(name=rc["name"], namespace=rc["namespace"]))

    def apply(self) -> None:
        for deploy in self.list:
            if not deploy.apply():
                logger.error(f"Could not deploy {deploy.name}")

    def get_from_name(self, name: str,) -> Optional[Deployment]:
        deploy = [d for d in self.list if d.name == name]

        if len(deploy):
            return deploy[0]

        return None

    @property
    def list(self) -> List[Deployment]:
        return self._deploys
