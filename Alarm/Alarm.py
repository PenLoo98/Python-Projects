# 라이브러리 불러오기 
# 기가지니 호출
# 알람 시간 설정
# 알람 해제


### 라이브러리 불러오기
#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from __future__ import print_function 

import audioop
from ctypes import *
import RPi.GPIO as GPIO
import ktkws # KWS
import MicrophoneStream as MS
KWSID = ['기가지니', '지니야', '친구야', '자기야'] 
RATE = 16000
CHUNK = 512

GPIO.setmode(GPIO.BOARD) # GPIO 핀 설정 보드번호로 설정
GPIO.setwarnings(False) # setwarning false 오류방지
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP) #핀 입출력모드 지정
GPIO.setup(31, GPIO.OUT) #핀 입출력모드 지정
btn_status = False # 버튼이 눌려지지 않은 상태에서 시작

# 버튼이 눌려지면 btn_status를 True로 변경
def callback(channel): 
    print("falling edge detected from pin {}".format(channel)) 
    global btn_status 
    btn_status = True  
    print(btn_status)

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10) 

# Error Handler
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p) 
def py_error_handler(filename, line, function, err, fmt): 
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler) 
asound = cdll.LoadLibrary('libasound.so') 
asound.snd_lib_error_set_handler(c_error_handler) 


### 기가지니 호출
# 마이크에서 음성을 받아서 호출어를 인식하는 함수
def detect(): 
    with MS.MicrophoneStream(RATE, CHUNK) as stream: 
        audio_generator = stream.generator() 

        for content in audio_generator: 
            

            rc = ktkws.detect(content)                                                              
            rms = audioop.rms(content,2) 
            print('audio rms = %d' % (rms)) 

            # 마이크에서 음성을 받아서 호출어를 인식하면 1을 리턴
            if (rc == 1): 
                MS.play_file("../data/sample_sound.wav") # 호출어 인식시 음성 출력
                return 200 





### 알람 시간 설정





### 알람 울림/해제






