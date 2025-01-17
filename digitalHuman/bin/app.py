# -*- coding: utf-8 -*-
'''
@File    :   app.py
@Author  :   一力辉 
'''

import uvicorn
from digitalHuman.engine import EnginePool
from digitalHuman.agent import AgentPool
from digitalHuman.server import app
from digitalHuman.utils import config
from digitalHuman.utils import logger
from env_key.index import load_and_replace


__all__ = ["runServer"]


def runServer():

    try:
        load_and_replace()
        logger.info("Successfully loaded and replaced API keys")
    except Exception as e:
        logger.error(f"Failed to load and replace API keys: {str(e)}")
    
    #首先是engine
    enginePool = EnginePool()
    #
    enginePool.setup(config.SERVER.ENGINES)

    agentPool = AgentPool()
    #
    agentPool.setup(config.SERVER.AGENTS)
    #启动服务
    uvicorn.run(app, host=config.SERVER.IP, port=config.SERVER.PORT, log_level="info")