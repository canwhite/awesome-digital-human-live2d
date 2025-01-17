import "whatwg-fetch";


/**
 * 这个文件主要包含与后端API交互的相关函数
 * 
 * 主要功能包括：
 * 1. 获取服务器URL：通过环境变量或当前主机名构建服务器地址
 * 2. WebSocket心跳检测：建立与服务器的WebSocket连接用于心跳检测
 * 3. ASR语音识别接口：提供语音识别服务
 * 
 * 环境变量配置：
 * - NEXT_PUBLIC_ADH_SERVER_PROTOCOL: 服务器协议 (http/https)
 * - NEXT_PUBLIC_ADH_SERVER_PORT: 服务器端口
 * - NEXT_PUBLIC_ADH_SERVER_VERSION: API版本
 * - NEXT_PUBLIC_ADH_SERVER_IP: 服务器IP地址
 * 
 * 主要函数说明：
 * - getURL(): 构建完整的服务器URL
 * - get_heatbeat_wss(): 获取WebSocket心跳检测地址
 * - asr_infer_api(): 语音识别API接口
 * 
 * 使用场景：
 * 1. 需要与后端服务进行通信时
 * 2. 需要进行语音识别处理时
 * 3. 需要建立WebSocket长连接时
 */

const SERVER_PROTOCOL = process.env.NEXT_PUBLIC_ADH_SERVER_PROTOCOL || "http";
const SERVER_PORT = process.env.NEXT_PUBLIC_ADH_SERVER_PORT || "8000";
const VERSION = process.env.NEXT_PUBLIC_ADH_SERVER_VERSION || "v0";

function getURL(): string {
  const SERVER_IP =
    process.env.NEXT_PUBLIC_ADH_SERVER_IP || globalThis.location?.hostname;
  const URL = SERVER_PROTOCOL + "://" + SERVER_IP + ":" + SERVER_PORT;
  return URL;
}

// export async function common_heatbeat_api() {
//     const URL = getURL();
//     let response = await fetch(URL + `/adh/common/${VERSION}/heartbeat`, {
//         method: "GET"
//     });
//     return response.json();
// }

export function get_heatbeat_wss() {
  const URL = getURL();

  const wsURL = URL.replace(/^http:/, "ws:").replace(/^https:/, "wss:");
  return `${wsURL}/adh/common/${VERSION}/heartbeat`;
}

export async function asr_infer_api(
  data: string,
  engine: string = "default",
  format: string = "wav",
  sampleRate: Number = 16000,
  sampleWidth: Number = 2,
  settings: { [key: string]: string } = {}
) {
  const URL = getURL();
  let response = await fetch(URL + `/adh/asr/${VERSION}/infer`, {
    method: "POST",
    body: JSON.stringify({
      engine: engine,
      data: data,
      format: format,
      sampleRate: sampleRate,
      sampleWidth: sampleWidth,
      settings: settings,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.json();
}

export async function tts_infer_api(
  data: string,
  engine: string = "default",
  settings: { [key: string]: string } = {}
) {
  const URL = getURL();
  let response = await fetch(URL + `/adh/tts/${VERSION}/infer`, {
    method: "POST",
    body: JSON.stringify({
      engine: engine,
      data: data,
      settings: settings,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.json();
}

export async function agents_list_api() {
  const URL = getURL();
  let response = await fetch(URL + `/adh/agent/${VERSION}/list`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return await response.json();
}

export async function agent_default_api() {
  const URL = getURL();
  let response = await fetch(URL + `/adh/agent/${VERSION}/default`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return await response.json();
}

export async function agent_settings_api(engine: string) {
  const URL = getURL();
  let response = await fetch(URL + `/adh/agent/${VERSION}/settings`, {
    method: "POST",
    body: JSON.stringify({
      engine: engine,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.json();
}

export async function agent_conversationid_api(
  engine: string = "default",
  settings: { [key: string]: string } = {}
) {
  const URL = getURL();
  let response = await fetch(URL + `/adh/agent/${VERSION}/conversation_id`, {
    method: "POST",
    body: JSON.stringify({
      engine: engine,
      settings: settings,
      streaming: true,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.json();
}

export async function agent_infer_streaming_api(
  data: string,
  engine: string = "default",
  conversationId: string = "",
  settings: { [key: string]: string } = {}
) {
  const URL = getURL();
  // 将conversationId填充到settings中
  settings["conversation_id"] = conversationId;
  let response = await fetch(URL + `/adh/agent/${VERSION}/infer`, {
    method: "POST",
    body: JSON.stringify({
      engine: engine,
      data: data,
      // 默认使用streaming模式
      streaming: true,
      settings: settings,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.body.getReader();
}
