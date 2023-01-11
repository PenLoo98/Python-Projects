# import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError
from modules.audio_handler import TTS,STT
import playsound

from modules.youtube import YoutubePlayer
youtube = YoutubePlayer()

# sched = BlockingScheduler()
sched = BackgroundScheduler()
tts = TTS()
stt = STT()

class Alarming():
    def __init__(self):
        self.hr:int
        self.min:int

    def set_alarm(self):
        tts.direct_tts("알람을 언제로 설정할까요?")
        recog = stt.get_text(timeout=5, phrase=5)
        print(f"인식된 텍스트: {recog}")
        try: 
            recog2 = recog.split(" ")
            self.hr = int(recog2[0].split("시")[0])
            self.min = int(recog2[1].split("분")[0])
        
        except ValueError: 
            print("ValueError")
            tts.direct_tts("잘 못알아들었어요")
            # 테스트
            self.hr, self.min = map(int,input("시간을 입력해주세요 h m\n:").split())
            

        try:
            print(f"알람 시간은 {self.hr}시 {self.min}분 입니다.")
            tts.direct_tts(f"알람 시간은 {self.hr}시 {self.min}분 입니다.")
            sched.add_job(self.alarm, 'cron', hour=self.hr, minute=self.min)
            sched.start()
        except SchedulerAlreadyRunningError:
            print("SchedulerAlreadyRunningError")
            tts.direct_tts("이미 알람이 설정되어 있습니다.")

    def alarm(self):
        if youtube.is_set():
            youtube.pause()

        tts.direct_tts("알람이 울립니다.")
        playsound.playsound("alarm.mp3")
        sched.remove_job(self.alarm)

        if youtube.is_set():
            youtube.play()




    

