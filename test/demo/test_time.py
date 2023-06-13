from playsound import playsound
import time

def alarm():
    print("时间到！")
    playsound('alarm.mp3')  # 播放提醒音频文件

alarm_time = input("请输入闹钟时间（格式为HH:MM:SS）：")
print(f"闹钟时间为{alarm_time}，倒计时开始...")

while True:
    current_time = time.strftime("%H:%M:%S")
    if current_time == alarm_time:
        alarm()
        break
    time.sleep(1)
