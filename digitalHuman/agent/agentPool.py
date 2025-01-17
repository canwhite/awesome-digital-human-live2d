# -*- coding: utf-8 -*-
'''
@File    :   AgentPool.py
@Author  :   一力辉 
'''

from threading import RLock
from typing import Optional, List
from yacs.config import CfgNode as CN
from digitalHuman.utils import logger
from .agentBase import BaseAgent
from .core import AgentFactory

__all__ = ["AgentPool"]

"""
AgentPool 是一个单例模式的代理池管理类，用于管理和维护不同类型的Agent实例。

主要功能包括：
1. 单例模式：通过__new__方法实现单例，确保全局只有一个AgentPool实例
2. 初始化管理：通过_init标志位控制初始化状态
3. 代理池管理：使用字典_pool存储所有Agent实例
4. 配置加载：通过setup方法根据配置文件初始化所有支持的Agent
5. 实例获取：通过get方法按名称获取指定Agent实例
6. 列表查询：通过list方法获取所有已加载的Agent名称列表

使用示例：
    config = load_config()  # 加载配置文件
    agent_pool = AgentPool()  # 获取单例实例
    agent_pool.setup(config)  # 初始化代理池
    agent = agent_pool.get("OpenaiAgent")  # 获取指定Agent
"""

class AgentPool():
    singleLock = RLock()
    _init = False

    def __init__(self):
        if not self._init:
            self._pool = dict()
            self._init = True
    
    # Single Instance
    def __new__(cls, *args, **kwargs):
        with AgentPool.singleLock:
            if not hasattr(cls, '_instance'):
                AgentPool._instance = super().__new__(cls)
        return AgentPool._instance

    def __del__(self):
        self._pool.clear()
        self._init = False
    
    def setup(self, config: CN):
        for cfg in config.SUPPORT_LIST:
            self._pool[cfg.NAME] = AgentFactory.create(cfg)
            logger.info(f"[AgentPool] AGENT Engine {cfg.NAME} is created.")
        logger.info(f"[AgentPool] AGENT Engine default is {config.DEFAULT}.")
            
    def get(self, name: str) -> Optional[BaseAgent]:
        if name not in self._pool:
            logger.error(f"[AgentPool] No such agent: {name}")
            return None
        return self._pool[name]

    def list(self) -> List[str]:
        return list(self._pool.keys())