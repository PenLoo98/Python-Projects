# import time
from apscheduler.schedulers.background import BackgroundScheduler
from modules.audio_handler import TTS,STT
import playsound
from threading import Thread

# sched = BlockingScheduler()
sched = BackgroundScheduler()
tts = TTS()
stt = STT()

class Alarming():
    def __init__(self):
        self.hr = 0
        self.min = 0

    def set_alarm(self):
        tts.direct_tts("알람을 언제로 설정할까요?")
        recog = stt.get_text(timeout=7, phrase=7)
        print(f"인식된 텍스트: {recog}")
        try: 
            if "시" in recog:
                self.hr = int(recog.split("시")[0])
            if "분" in recog:
                self.min = int(recog.split("분")[0])
        except :
            print(f"인식된 텍스트: {recog}")
            tts.direct_tts("잘 못알아들었어요")
        
        


        print(f"알람 시간은 {self.hr}시 {self.min}분 입니다.")
        tts.direct_tts(f"알람 시간은 {self.hr}시 {self.min}분 입니다.")
        sched.add_job(self.alarm, 'cron', hour=self.hr, minute=self.min)
        sched.start()

    def alarm(self):
        tts.direct_tts("알람이 울립니다.")
        playsound.playsound("alarm.mp3")
        sched.remove_job(self.alarm)

    # print(f"설정시간: {hr}시 {min}분")
    # @sched.scheduled_job('cron', hour=hr, minute=min)
    # def job1():
    #     # 알람이 울릴 때 실행할 코드를 작성합니다.
    #     print("알람이 울립니다.")
    #     tts.direct_tts("알람이 울립니다.")
    #     playsound.playsound("audio_dump.mp3")
        
    # sched.start()
    # while True:
    #     time.sleep(5)




    

