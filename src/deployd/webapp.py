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
    # blocking call - should run in other thread
    deploys.apply()

    while True:
        # blocking call - should run in other thread
        repos.update()

        for repo in repos.updated:
            logger.info(f"{repo.name} updated")
            if not deploys.get_from_name(repo.name).apply():
                logger.error(f"deployment of {repo.name} failed")

            # assuming deployment cannot fail - do not deploy again before new code is pushed
            repo.clear_updated()

        logger.debug("entering await")
        await asyncio.sleep(delta)
        logger.debug("await returned")

@webapp.before_serving
async def startup():
    loop = asyncio.get_event_loop()
    webapp.update = loop.create_task(update())

@webapp.route("/deployment/<path:name>")
async def deployment(name) -> Response:
    logger.info(f"fetching status from {name}")

    deploy = deploys.get_from_name(name)

    if deploy is None:
        return jsonify({"deployment": "Unavailable"}), 404

    return jsonify(deploy.status_json())

@webapp.route("/healthcheck")
async def healthcheck() -> Response:
    return jsonify({"healthy": True})
