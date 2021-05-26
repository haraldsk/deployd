import os
import logging
import subprocess
import json

from typing import List, Optional
from .config import RepoConfig, REPO_LOCAL_ROOT

logger = logging.getLogger(__name__)

class Deployment():
    def __init__(self, name: str, namespace: str,) -> None:
        self._name = name
        self._namespace = namespace
        self._path = os.path.join(REPO_LOCAL_ROOT, self._name)
        self._last_deploy: Optional[subprocess.CompletedProcess] = None

    def apply(self) -> bool:
        command: List[str] = f"kubectl apply --namespace {self._namespace} -k {self._path}/deploy/manifests".split(" ")
        logging.info(f"running {command}")
        self._last_deploy: subprocess.CompletedProcess = subprocess.run(command, stdout=subprocess.PIPE)

        print(self._last_deploy.stdout)

        if self._last_deploy.returncode == 0:
            return True

        return False

    def status_json(self):
        command: List[str] = f"kubectl get --namespace {self._namespace} -k {self._path}/deploy/manifests -o json".split(" ")

        logging.info(f"running {command}")
        status: subprocess.CompletedProcess = subprocess.run(command, stdout=subprocess.PIPE)
        kcout = json.loads(status.stdout)
        return kcout

    @property
    def name(self):
        return self._name

class Deployments():
    def __init__(self, repoconfigs: List[RepoConfig],) -> None:
        self._deploys: List[Deployment] = []

        for rc in repoconfigs:
            self._deploys.append(Deployment(name=rc["name"], namespace=rc["namespace"]))

    @property
    def list(self) -> List[Deployment]:
        return self._deploys

    def apply(self):
        for deploy in self.list:
            if not deploy.apply():
                logger.info(f"Could not deploy {deploy.name}")

    def get_from_name(self, name: str,) -> Optional[Deployment]:
        deploy = [d for d in self.list if d.name == name]

        if len(deploy):
            return deploy[0]

        return None
