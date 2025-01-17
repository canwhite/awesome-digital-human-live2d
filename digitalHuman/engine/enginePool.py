# -*- coding: utf-8 -*-
'''
@File    :   enginePool.py
@Author  :   一力辉 
'''

from threading import RLock
from enum import Enum
from typing import Optional
from collections import defaultdict
from yacs.config import CfgNode as CN
from digitalHuman.utils import logger
from .engineBase import BaseEngine
from .asr import ASRFactory
from .llm import LLMFactory
from .tts import TTSFactory

__all__ = ["EnginePool", "EngineType"]


"""
EnginePool 模块说明

该模块实现了一个引擎池管理类，用于集中管理ASR（语音识别）、TTS（语音合成）和LLM（大语言模型）三种类型的引擎实例。

主要功能：
1. 使用单例模式确保全局只有一个引擎池实例
2. 支持通过配置文件初始化多个同类型引擎
3. 提供统一的引擎获取接口
4. 支持引擎的自动清理

核心类：
- EngineType: 枚举类，定义支持的引擎类型
- EnginePool: 引擎池管理类，负责引擎的创建、存储和获取

实现特点：
1. 线程安全：使用RLock保证单例创建和引擎操作的线程安全
2. 延迟初始化：引擎池在首次使用时才进行初始化
3. 灵活扩展：通过工厂模式创建引擎，易于添加新的引擎实现
4. 日志记录：关键操作都添加了日志记录

使用示例：
    pool = EnginePool()
    pool.setup(config)
    asrEngine = pool.getEngine(EngineType.ASR, "default")
"""


class EngineType(Enum):
    """
    Engine Type
    """
    ASR   = "ENGINE_TYPE_ASR"
    TTS   = "ENGINE_TYPE_TTS"
    LLM   = "ENGINE_TYPE_LLM"

class EnginePool():
    singleLock = RLock()
    _init = False

    def __init__(self):
        if not self._init:
            self._pool = defaultdict(dict)
            self._init = True
    
    # Single Instance
    def __new__(cls, *args, **kwargs):
        with EnginePool.singleLock:
            if not hasattr(cls, '_instance'):
                EnginePool._instance = super().__new__(cls)
        return EnginePool._instance

    def __del__(self):
        self._pool.clear()
        self._init = False
    
    def setup(self, config: CN):
        # asr
        for asrCfg in config.ASR.SUPPORT_LIST:
            self._pool[EngineType.ASR][asrCfg.NAME] = ASRFactory.create(asrCfg)
            logger.info(f"[EnginePool] ASR Engine {asrCfg.NAME} is created.")
        logger.info(f"[EnginePool] ASR Engine default is {config.ASR.DEFAULT}.")
        # llm
        for llmCfg in config.LLM.SUPPORT_LIST:
            self._pool[EngineType.LLM][llmCfg.NAME] = LLMFactory.create(llmCfg)
            logger.info(f"[EnginePool] LLM Engine {llmCfg.NAME} is created.")
        logger.info(f"[EnginePool] LLM Engine default is {config.LLM.DEFAULT}.")
        # tts
        for ttsCfg in config.TTS.SUPPORT_LIST:
            self._pool[EngineType.TTS][ttsCfg.NAME] = TTSFactory.create(ttsCfg)
            logger.info(f"[EnginePool] TTS Engine {ttsCfg.NAME} is created.")
        logger.info(f"[EnginePool] TTS Engine default is {config.TTS.DEFAULT}.")
            
    def getEngine(self, engineType: EngineType, engineName: str) -> Optional[BaseEngine]:
        if engineType not in self._pool:
            logger.error(f"[EnginePool] No such engine type: {engineType}")
            return None
        if engineName not in self._pool[engineType]:
            logger.error(f"[EnginePool] No such engine: {engineName}")
            return None
        return self._pool[engineType][engineName]