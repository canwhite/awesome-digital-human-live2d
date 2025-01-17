# -*- coding: utf-8 -*-
'''
@File    :   api.py
@Author  :   一力辉 
'''

from .commonApi import router as commonRouter
from .asrApi import router as asrRouter
from .agentApi import router as agentRouter
from .llmApi import router as llmRouter
from .ttsApi import router as ttsRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

__all__ = ["app"]

"""
这个文件是数字人项目的API主入口文件，主要功能如下：

1. 导入各个模块的路由器：
   - commonRouter: 通用API路由
   - asrRouter: 语音识别(ASR)API路由
   - agentRouter: 智能体(Agent)API路由
   - llmRouter: 大语言模型(LLM)API路由
   - ttsRouter: 语音合成(TTS)API路由

2. 创建FastAPI应用实例：
   - 设置应用标题、描述和版本号
   - 添加CORS中间件，允许跨域请求

3. 注册各个路由：
   - 每个路由都有统一的前缀/adh
   - 按功能模块划分路由组，方便管理和文档展示
   - 每个路由组都有对应的tags，用于API文档分类

整个API服务采用模块化设计，将不同功能的路由分开管理，通过统一的入口文件进行整合。
这种设计使得代码结构清晰，易于维护和扩展。
"""

app = FastAPI(
    title="Awesome Digital Human", 
    description="This is a cool set of apis for Awesome Digital Human",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(commonRouter, prefix="/adh/common", tags=["COMMON"])
app.include_router(asrRouter, prefix="/adh/asr", tags=["ASR"])
app.include_router(llmRouter, prefix="/adh/llm", tags=["LLM"])
app.include_router(ttsRouter, prefix="/adh/tts", tags=["TTS"])
app.include_router(agentRouter, prefix="/adh/agent", tags=["AGENT"])