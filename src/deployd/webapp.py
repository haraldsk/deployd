import asyncio
import logging

from quart import Quart, jsonify, Response
from typing import List

from .config import RepoConfig, RepoConfigs
from .deploy import Deployments
from .repository import Repositories

webapp = Quart(__name__)
logger = logging.getLogger(__name__)

# get list of repos from config
rcs: List[RepoConfig] = RepoConfigs().list
# initalise repos
repos: Repositories = Repositories(repoconfigs=rcs)
# initalize deployment
deploys: Deployments = Deployments(repoconfigs=rcs)

async def update(delta=10):
    # deploy all repos
    deploys.apply()

    while True:
        # blocking call - should run in other thread
        repos.update()
        for repo_name in repos.updated:
            logger.info(f"{repo_name} updated")
            [deploy.apply() for deploy in deploys.list if deploy.name == repo_name]
            # deploy repo
            # check status
            # clear update status

        logger.info("entering await")
        await asyncio.sleep(delta)
        logger.info("await returned")

@webapp.before_serving
async def startup():
    loop = asyncio.get_event_loop()
    webapp.update = loop.create_task(update())

@webapp.route("/healthcheck")
async def healthcheck() -> Response:
    return jsonify({"healthy": True})
