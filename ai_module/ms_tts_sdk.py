from __future__ import barry_as_FLUFL
import time

import azure.cognitiveservices.speech as speechsdk
import asyncio
import sys
sys.path.append("E:\\GitHub\\Fay\\")
from core import tts_voice
from core.tts_voice import EnumVoice
from utils import util, config_util
from utils import config_util as cfg
import pygame
import edge_tts
import io
import math




class Speech:
    def __init__(self):
        self.ms_tts = False
        if config_util.key_ms_tts_key and config_util.key_ms_tts_key is not None and config_util.key_ms_tts_key.strip() != "":
            self.__speech_config = speechsdk.SpeechConfig(subscription=cfg.key_ms_tts_key, region=cfg.key_ms_tts_region)
            self.__speech_config.speech_recognition_language = "zh-CN"
            self.__speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
            self.__speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
            self.__synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.__speech_config, audio_config=None)
            self.ms_tts = True
        self.__connection = None
        self.__history_data = []


    def __get_history(self, voice_name, style, text):
        for data in self.__history_data:
            if data[0] == voice_name and data[1] == style and data[2] == text:
                return data[3]
        return None

    def connect(self):
        if self.ms_tts:
            self.__connection = speechsdk.Connection.from_speech_synthesizer(self.__synthesizer)
            self.__connection.open(True)
        util.log(1, "TTS 服务已经连接！")

    def close(self):
        if self.__connection is not None:
            self.__connection.close()

    #生成mp3音频
    async def get_edge_tts(self,text,voice,file_url) -> None:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(file_url)

    """
    文字转语音
    :param text: 文本信息
    :param style: 说话风格、语气
    :returns: 音频文件路径
    """

    def to_sample(self, text, style):
        if self.ms_tts:
            ## show the text
            #print("text: ", text)
            voice_type = tts_voice.get_voice_of(config_util.config["attribute"]["voice"])
            voice_name = EnumVoice.XIAO_XIAO.value["voiceName"]
            if voice_type is not None:
                voice_name = voice_type.value["voiceName"]
            history = self.__get_history(voice_name, style, text)
            if history is not None:
                return history
            ssml = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">' \
                   '<voice name="{}">' \
                   '<mstts:express-as style="{}" styledegree="{}">' \
                   '{}' \
                   '</mstts:express-as>' \
                   '</voice>' \
                   '</speak>'.format(voice_name, style, 1.8, text)
            result = self.__synthesizer.speak_ssml(ssml)
            audio_data_stream = speechsdk.AudioDataStream(result)
            """
            audio_data_bytes = io.BytesIO()
            buffer_size = 4096  # 定义缓冲区的大小

            ret = 1
            while ret != 0:
                # 使用read_data从AudioDataStream读取数据到buffer
                buffer = bytes(buffer_size)
                ret = audio_data_stream.read_data(buffer)
                # 将读取到的数据写入到BytesIO对象中
                audio_data_bytes.write(buffer)
                    
            audio_data_bytes.seek(0)
            """
            file_url = './samples/sample-' + str(int(time.time() * 1000)) + '.mp3'
            audio_data_stream.save_to_wav_file(file_url)
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                self.__history_data.append((voice_name, style, text, file_url))
                return file_url
                #return audio_data_bytes
            else:
                util.log(1, "[x] 语音转换失败！")
                util.log(1, "[x] 原因: " + str(result.reason))
                return None
        else:
            voice_type = tts_voice.get_voice_of(config_util.config["attribute"]["voice"])
            voice_name = EnumVoice.XIAO_XIAO.value["voiceName"]
            if voice_type is not None:
                voice_name = voice_type.value["voiceName"]
            history = self.__get_history(voice_name, style, text)
            if history is not None:
                return history
            ssml = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">' \
                   '<voice name="{}">' \
                   '<mstts:express-as style="{}" styledegree="{}">' \
                   '{}' \
                   '</mstts:express-as>' \
                   '</voice>' \
                   '</speak>'.format(voice_name, style, 1.8, text)
            try:
                file_url = './samples/sample-' + str(int(time.time() * 1000)) + '.mp3'
                asyncio.new_event_loop().run_until_complete(self.get_edge_tts(text,voice_name,file_url))
                self.__history_data.append((voice_name, style, text, file_url))
            except Exception as e :
                util.log(1, "[x] 语音转换失败！")
                util.log(1, "[x] 原因: " + str(str(e)))
                file_url = None
            return file_url


if __name__ == '__main__':
    str1 = "我叫Fay"
    str2 = "我叫Fay,我今年18岁"
    str3 = "我叫Fay,我今年18岁，很年青"
    str4 = "在黎明的光辉中，希望如同绽放的花朵，温暖而明亮，照亮前行的道路"
    str5 = "当夜幕降临，星辰在天际闪烁，我们仰望着那无尽的宇宙，心中充满了对未知世界的无限憧憬与向往"
    str6 = "在这个充满挑战与机遇的时代，我们必须勇敢地面对困难，把握每一个机会，不断学习，努力进步，为实现梦想而不懈奋斗"
    str7 = "生活就像一场旅行，我们在路上遇到各种风景，有时候是晴朗的天空，有时候是风雨交加。重要的是保持乐观的态度，享受旅途中的每一个瞬间"
    str8 = "在这片广阔的天地间，每个人都是独一无二的存在。我们应该珍惜自己的特色，勇敢地追求自己的梦想，即使路途遥远且充满挑战，也不应放弃，因为每一步都离梦想更近"
    str9 = "记住，成功的道路从不会是一帆风顺的。它充满了挑战和困难，但正是这些挑战和困难，塑造了我们的意志和坚韧。只有勇敢面对，积极应对，才能在生命的舞台上绽放出最耀眼的光彩"
    str10 = "在生命的长河中，每个人都在书写着自己的故事。无论是欢笑还是泪水，都是这个故事中不可或缺的一部分。让我们拥抱生活的每一刻，不畏惧挑战，勇敢前行，用心感受生活的美好，把握每一个现在，共同创造一个更加精彩的未来"
    eng1 = "The cat sat."
    eng2 = "A quick brown fox jumps over the lazy dog nearby."
    eng3 = "She opened her book, eager to lose herself in its pages once again."
    eng4 = "As the sun dipped below the horizon, the sky turned a magnificent shade of orange, blending into purple."
    eng5 = "In the heart of the bustling city, a small, unnoticed flower pushed its way through the concrete, seeking sunlight."
    eng6 = "Despite the challenges that lay ahead, she stood at the cliff's edge, taking a deep breath, ready to face her fears with newfound courage."
    eng7 = "The old library held secrets within its walls, whispering tales of ancient times, magic, and adventures that beckoned anyone daring enough to discover them."
    eng8 = "Throughout the centuries, philosophers and scientists have pondered the mysteries of the universe, seeking to understand the laws that govern our existence, leading to groundbreaking discoveries that have shaped the course of human history."
    cfg.load_config()
    sp = Speech()
    sp.connect()
    test_list = [str1, str2, str3, str4, str5, str6, str7, str8, str9, str10]
    eng_list = [eng1, eng2, eng3, eng4, eng5, eng6, eng7, eng8]
    for eng in eng_list:
        tm = time.time()
        s = sp.to_sample(eng, "cheerful")
        print('合成音频完成. 耗时: {} ms'.format(math.floor((time.time() - tm) * 1000)))
    sp.close()

