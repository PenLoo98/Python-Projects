# 라이브러리 불러오기 
# 기가지니 호출
# 알람 시간 설정
# 알람 울림,해제

## 필요한 파일 다운 받기: 음성, 호출어 모델


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


import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import user_auth as UA
import os
HOST = 'gate.gigagenie.ai' 
PORT = 4080


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

def test(key_word = '기가지니'):
    rc = ktkws.init("../data/kwsmodel.pack") 
    print ('init rc = %d' % (rc))
    rc = ktkws.start()
    print ('start rc = %d' % (rc))
    print ('\n호출어를 불러보세요~\n')
    ktkws.set_keyword(KWSID.index(key_word)) 
    rc = detect()
    print ('detect rc = %d' % (rc))
    print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n') 
    ktkws.stop()
    return rc


### 알람 시간 설정
import time
import datetime

def set_alarm(alarm_time: int):
    now = datetime.datetime.now()
    print("현재 시간은 %d:%d:%d 입니다." % (now.hour, now.minute, now.second))
    after = now + datetime.timedelta(minutes=alarm_time)
    print("알람 시간은 %d:%d:%d 입니다." % (after.hour, after.minute, after.second))

    while(now.hour != after.hour or now.minute != after.minute):
        now = datetime.datetime.now()
        print("현재 시간은 %d:%d:%d 입니다." % (now.hour, now.minute, now.second))
        time.sleep(15)

    # 버튼을 누르면 알람 해제
    while btn_status == False:
        # print("알람이 울립니다.")
        MS.play_file("wav/alarm bbbb.wav")
    print("알람이 해제되었습니다.")
    

### 메인 함수
def main(): 
    test()

    # 10분 뒤에 알람이 울립니다.
    set_alarm(10)
if __name__ == '__main__': 
    main()