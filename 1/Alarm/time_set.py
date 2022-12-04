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

    # print("알람이 울립니다.")
    

# 10분 뒤에 알람이 울립니다.
set_alarm(10)
