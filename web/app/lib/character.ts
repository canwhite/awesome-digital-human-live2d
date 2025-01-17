import { LAppDelegate } from '@/app/lib/live2d/lappdelegate';

/**
 * CharacterManager 类用于管理角色相关功能
 * 这是一个单例类，提供以下功能：
 * 1. 获取Live2D角色肖像列表
 * 2. 获取/设置当前角色
 * 3. 获取背景图片列表
 * 4. 管理TTS音频队列
 * 
 * 该类通过LAppDelegate与Live2D引擎交互
 * 使用单例模式确保全局只有一个实例
 * 
 * 主要方法：
 * - getInstance(): 获取单例实例
 * - getLive2dPortraits(): 获取所有角色肖像
 * - getCharacter(): 获取当前角色
 * - setCharacter(): 设置当前角色
 * - getBackImages(): 获取背景图片
 * - pushAudioQueue(): 添加音频到队列
 * - popAudioQueue(): 从队列取出音频
 * - clearAudioQueue(): 清空音频队列
 */

export class CharacterManager {
    // 单例
    public static getInstance(): CharacterManager {
        if (! this._instance) {
            this._instance = new CharacterManager();
        }

        return this._instance;
    }

    public getLive2dPortraits(): {[key: string]: string} {
      return LAppDelegate.getInstance().getPortraits();
    }

    public getCharacter(): string {
      return LAppDelegate.getInstance().getCharacter();
    }

    public setCharacter(character: string): void {
      LAppDelegate.getInstance().changeCharacter(character);
    }

    public getBackImages(): {[key: string]: string} {
      return LAppDelegate.getInstance().getBackImages();
    }

    // public getBackground(): string {
    //   return LAppDelegate.getInstance().getBackground();
    // }

    // public setBackground(background: string | null): void {
    //   LAppDelegate.getInstance().changeBackground(background);
    // }

    public pushAudioQueue(audioData: ArrayBuffer): void {
      this._ttsQueue.push(audioData);
    }

    public popAudioQueue(): ArrayBuffer | null {
      if (this._ttsQueue.length > 0) {
        const audioData = this._ttsQueue.shift();
        return audioData;
      } else {
        return null;
      }
    }

    public clearAudioQueue(): void {
      this._ttsQueue = [];
    }

    private static _instance: CharacterManager;
    private _ttsQueue: ArrayBuffer[] = [];
  }