# -*- coding: utf-8 -*-
'''
@File    :   asrApi.py
@Author  :   一力辉 
'''

from .reponse import BaseResponse, Response
import base64
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from digitalHuman.utils import config
from digitalHuman.utils import AudioMessage, TextMessage, AudioFormatType
from digitalHuman.engine import EnginePool, EngineType

router = APIRouter()
enginePool = EnginePool()

class InferIn(BaseModel):
    engine: str = "default"
    data: str
    format: str
    sampleRate: int
    sampleWidth: int
    settings: dict = {}

class InferOut(BaseResponse):
    data: Optional[str] = None

"""
ASR API 路由模块

这个模块实现了语音识别(ASR)相关的API接口，主要功能包括：

1. 定义API请求和响应模型：
   - InferIn: 定义语音识别请求的输入参数
   - InferOut: 定义语音识别请求的响应格式

2. 提供语音识别推理接口：
   - /v0/infer: 实现语音识别功能的核心接口
   - 支持多种音频格式和采样参数
   - 可指定不同的ASR引擎进行处理

3. 主要处理流程：
   - 接收Base64编码的音频数据
   - 根据请求参数创建AudioMessage对象
   - 调用指定的ASR引擎进行语音识别
   - 返回识别结果文本

4. 错误处理：
   - 检查音频格式是否支持
   - 捕获引擎运行时的异常
   - 返回统一的错误响应格式

5. 配置管理：
   - 使用全局配置获取默认ASR引擎
   - 支持通过请求参数动态选择引擎

该模块通过FastAPI的APIRouter实现路由注册，与主应用集成。
"""


@router.post("/v0/infer", response_model=InferOut, summary="Automatic Speech Recognition Inference")
async def apiInfer(item: InferIn):
    if item.engine.lower() == "default":
        item.engine = config.SERVER.ENGINES.ASR.DEFAULT
    response = Response()
    try:
        format = AudioFormatType._value2member_map_.get(item.format)
        if format is None:
            raise RuntimeError("Unsupported audio format")
        input = AudioMessage(data=base64.b64decode(item.data), format=format, sampleRate=item.sampleRate, sampleWidth=item.sampleWidth)
        output: Optional[TextMessage] = await enginePool.getEngine(EngineType.ASR, item.engine).run(input, **item.settings)
        if output is None:
            raise RuntimeError("ASR engine run failed")
        response.data = output.data
    except Exception as e:
        response.data = None
        response.error(str(e))
    return JSONResponse(content=response.validate(InferOut), status_code=200)