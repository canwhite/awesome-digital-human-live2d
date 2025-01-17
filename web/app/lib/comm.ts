import * as API from '@/app/lib/api';
/**
 * 这个文件主要包含了一些通用的工具函数和通信类
 * 
 * 主要功能包括：
 * 1. blobToBase64: 将Blob对象转换为Base64字符串
 * 2. base64ToArrayBuffer: 将Base64字符串转换为ArrayBuffer
 * 3. Comm类：实现了一个单例模式的通信类
 * 
 * 这些工具通常用于以下场景：
 * 1. 文件处理：当需要将文件转换为Base64格式进行传输或存储时
 * 2. 数据转换：在需要将二进制数据转换为字符串格式时
 * 3. 网络通信：Comm类可以用于管理应用中的网络请求
 * 4. 音视频处理：在处理音频、视频等二进制数据时
 * 
 * 特别适用于：
 * - 需要在前端处理二进制数据的场景
 * - 需要实现单例模式的网络通信管理
 * - 需要将文件数据转换为可传输格式的场景
 */


function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    // 读取完成后的处理  
    reader.onloadend = function () {
      // 读取成功，result属性中将包含一个data: URL格式的字符串  
      // 通过split(',')来提取Base64编码的字符串  
      const base64data = reader.result as string;
      const base64String = base64data.split(',')[1];
      resolve(base64String);
    };

    // 错误处理  
    reader.onerror = function (error) {
      reject(error);
    };

    // 读取Blob对象，并作为data URL返回  
    reader.readAsDataURL(blob);
  });
}

function base64ToArrayBuffer(base64String: string): ArrayBuffer {
  const binaryString = window.atob(base64String);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

export class Comm {
  // 单例
  public static getInstance(): Comm {
    if (!this._instance) {
      this._instance = new Comm();
    }

    return this._instance;
  }

  // public async getHeartbeat(): Promise<boolean> {
  //   return API.common_heatbeat_api().then(response => {
  //     if (response.data == 1) {
  //       return true;
  //     } else {
  //       return false;
  //     }
  //   }).catch(error => {
  //     console.error(error);
  //     return false;
  //   })
  // }

  public async getAgentsList(): Promise<string[]> {
    return API.agents_list_api().then(response => {
      return response.data;
    }).catch(error => {
      console.error(error);
      return []
    })
  }

  public async getDefaultAgent(): Promise<string> {
    return API.agent_default_api().then(response => {
      return response.data;
    }).catch(error => {
      console.error(error);
      return ""
    })
  }

  public async getAgentSettings(agent: string): Promise<{[key: string]: string}[]> {
    return API.agent_settings_api(agent).then(response => {
      return response.data;
    }).catch(error => {
      console.error(error);
      return {}
    })
  }

  public async getConversionId(
    agent: string = "default",
    settings: { [key: string]: string } = {},
  ): Promise<string> {
    return API.agent_conversationid_api(agent, settings).then(response => {
      return response.data;
    }).catch(error => {
      console.error(error);
      return ""
    })
  }

  public async streamingChat(
    data: string,
    engine: string = "default",
    conversationId: string = "",
    settings: { [key: string]: string } = {},
    callbackProcessing: (index: number, data: string) => void,
    callbackEnd: (index: number) => void
  ): Promise<void> {
    try {
      const reader = await API.agent_infer_streaming_api(data, engine, conversationId, settings);
      const decoder = new TextDecoder("utf-8");
      let index = 0;
      while (true) {
        const { value, done } = await reader.read(); 
        if (done) {
          callbackEnd(index);
          break;
        }
        const chunk = decoder.decode(value, { stream: true });
        callbackProcessing(index, chunk);
        index++;
      }
      reader.releaseLock();
    } catch (error) {
      console.error(error);
    }
  }

  public async asr(
    data: Blob,
    settings: { [key: string]: string } = {},
    engine: string = "default",
    format: string = "wav",
    sampleRate: Number = 16000,
    sampleWidth: Number = 2
  ): Promise<string> {
    return blobToBase64(data).then(base64str => {
      if (base64str == null) {
        return "";
      }
      return API.asr_infer_api(base64str, engine, format, sampleRate, sampleWidth, settings).then(response => {
        return response.data;
      }).catch(error => {
        console.error(error);
        return ""
      })
    }).catch(error => {
      console.error(error);
      return "";
    })
  }

  public async tts(
    data: string,
    settings: { [key: string]: string } = {},
    engine: string = "default"
  ): Promise<ArrayBuffer> {
    // 处理tts输入数据
    const filterData = (data: string): string => {
      // 过滤所有的emoji
      const regex = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2700}-\u{27BF}\u{1F1E0}-\u{1F1FF}]/gu;  
      data = data.replace(regex, '');
      return data
    }
    data = filterData(data);
    if (data.length == 0) {
      return null;
    }
    return API.tts_infer_api(data, engine, settings).then(response => {
      if (response.data == null) {
        return null;
      }
      return base64ToArrayBuffer(response.data);
    }).catch(error => {
      console.error(error)
      return null;
    })
  }

  private static _instance: Comm;
}