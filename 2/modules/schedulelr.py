# import datetime
# from apscheduler.schedulers.blocking import BlockingScheduler
import time
from apscheduler.schedulers.background import BackgroundScheduler
from audio_handler import TTS,STT
import playsound

# sched = BlockingScheduler()
sched = BackgroundScheduler()
tts = TTS()
stt = STT()

class set_alarm():
    print("알람을 원하는 시간을 입력하세요.:")
    hr = int(input("시간: "))
    min = int(input("분: "))


    print(f"설정시간: {hr}시 {min}분")
    @sched.scheduled_job('cron', hour=hr, minute=min)
    def job1():
        # 알람이 울릴 때 실행할 코드를 작성합니다.
        print("알람이 울립니다.")
        tts.direct_tts("알람이 울립니다.")
        playsound.playsound("audio_dump.mp3")
        
    sched.start()
    while True:
        time.sleep(5)

# txt = "오후 4시 30분"
# result = txt.split(str,int)
# print(result)



    

