import schedule
import time
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from post_maker import sending_post


LOCAL_TZ = ZoneInfo("Asia/Tashkent")  

def random_minuting(hours: int) -> str:
    random_minut = random.randint(0, 59)
    minutes = f"{random_minut:02}"
    return f"{hours:02}:{minutes}"

def get_local_time_str(hour: int) -> str:
    now = datetime.now(tz=LOCAL_TZ)
    random_min = random.randint(0, 59)
    dt = now.replace(hour=hour, minute=random_min, second=0, microsecond=0)
    return dt.strftime("%H:%M")

def scheduling_post_times():
    schedule.clear('daily_posts')
    print("scheduling")
    schedule.every().day.at(get_local_time_str(10)).do(sending_post).tag('daily_posts')
    schedule.every().day.at(get_local_time_str(14)).do(sending_post).tag('daily_posts')
    schedule.every().day.at(get_local_time_str(20)).do(sending_post).tag('daily_posts')

schedule.every().day.at("11:49").do(scheduling_post_times)
print("hello I am starting")
print(datetime.now())
while True:
    schedule.run_pending()
    time.sleep(30)
