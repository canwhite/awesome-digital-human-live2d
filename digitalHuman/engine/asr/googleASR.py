# -*- coding: utf-8 -*-
'''
@File    :   googleASR.py
@Author  :   一力辉 
'''

from ..builder import ASREngines
from ..engineBase import BaseEngine
from typing import List, Optional
import speech_recognition as sr
from speech_recognition import AudioData
from digitalHuman.utils import AudioMessage, TextMessage
from digitalHuman.utils import logger

"""
GoogleAPI 是一个基于Google语音识别API的ASR（自动语音识别）引擎实现类。

主要功能包括：
1. 继承自BaseEngine基类，实现ASR引擎的基本功能
2. 使用speech_recognition库与Google语音识别API进行交互
3. 支持通过配置文件设置API KEY和识别语言
4. 将音频数据转换为文本信息

类方法说明：
- checkKeys(): 返回必须的配置项列表，包括API KEY和语言设置
- setup(): 初始化语音识别器实例
- run(): 执行语音识别任务，将音频消息转换为文本消息

使用示例：
    config = load_config()  # 加载包含Google API配置的yaml文件
    asr_engine = GoogleAPI(config)  # 创建实例
    asr_engine.setup()  # 初始化
    text = asr_engine.run(audio_message)  # 执行语音识别
"""


__all__ = ["GoogleAPI"]

#ASR实际上就是识别音频信息转化为文本，作为输入存在
@ASREngines.register("GoogleAPI")
class GoogleAPI(BaseEngine): 
    def checkKeys(self) -> List[str]:
        return ["KEY", "LANGUAGE"]
    
    def setup(self):
        self.rec = sr.Recognizer()
    
    async def run(self, input: AudioMessage, **kwargs) -> Optional[AudioMessage]:
        try: 
            key = self.cfg.KEY if self.cfg.KEY else None
            audio = AudioData(
                input.data,
                input.sampleRate,
                input.sampleWidth
            )

            result = str(self.rec.recognize_google(audio, key=key, language=self.cfg.LANGUAGE))
            message = TextMessage(data=result)
            return message
        except Exception as e:
            logger.error(f"[ASR] Engine run failed: {e}")
            return None