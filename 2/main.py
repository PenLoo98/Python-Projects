from modules.audio_handler import TTS,STT
from modules.youtube import YoutubePlayer
from modules.schedulelr import set_alarm

def main():
    stt = STT()
    tts = TTS()
    youtube = YoutubePlayer()

    while True:
        recog = stt.get_text(timeout=2, phrase=3)
        if not recog in ["지니야", "기가지니"]:
            continue
        print("start command mode")
        if youtube.is_set():
            youtube.pause()
        tts.direct_tts("네")
        command = stt.get_text(timeout=2, phrase=3)
        if command is None:
            tts.direct_tts("잘 못알아들었어요")
            continue
        print(f"인식된 텍스트: {command}")
        if "유튜브" in command:
            if "재생" in command or "틀어" in command:
                thr = tts.direct_tts("유튜브에서 오디오를 재생합니다.", wait=False)
                youtube.set_with_text("음악")
                thr.join()
                
            elif "중지" in command or "꺼" in command:
                tts.direct_tts("오디오를 종료합니다.")
                youtube.stop()
        elif "알람" in command:
            try:
                if "시" or "분" in command:
                    hr = int(command[0])
                    min = int(command[2])
                    print(f"설정시간: {hr}시 {min}분")
                    set_alarm()
            except(ValueError):
                # tts.direct_tts("무슨 말인지 모르겠어요")
                set_alarm()
                continue
        if youtube.is_set():
            youtube.play()
                
                
if __name__ == "__main__":
    main()