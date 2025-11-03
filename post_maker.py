from swe_topics import SWE_TOPICS_EXTENDED

import requests
from google import genai
import os
from dotenv import load_dotenv
import random
import time
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANEL_ID")
GEMINI_KEY = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=GEMINI_KEY)


def choosing_topic():
    topic = random.choice(SWE_TOPICS_EXTENDED)
    return topic

def ai_response(topic, retries=3):
    promt = f"""
Siz professional kontent yaratuvchisiz. Sizga <b>{topic}</b> mavzusida <b>o‘zbek tilida</b> yozilgan, Telegram uchun HTML formatda (<b>, <i>, <u>, <a>, <code>, <pre>) chiroyli va o‘qilishi yoqimli post yaratish topshirig‘i berilgan.

🎯 Talablar:
- Post <b>qisqa (4–8 gap)</b>, <b>qiziqarli</b> va <b>kreativ ohangda</b> bo‘lsin.
- Texnik mavzular oddiy tilda tushuntirilsin, misollar hayotiy bo‘lsin.
- Kirishda diqqatni tortadigan fakt, hazil yoki taqqoslash ishlatilsin.
- Emoji’lar joyida, ma’noga mos qo‘llansin (masalan: 💡🔥😅).
- Oxirida "obuna bo‘ling", "ulashing" kabi chaqiriqlar bo‘lmasin.
- Quyidagi havolani <i>ixtiyoriy</i> tarzda ishlatish mumkin: 
  <a href='https://t.me/asliddin_tursunoffpy'>asliddin_tursunoff.py</a>

❌ Yozilmasin:
- “Salom obunachilar”, “Keling boshladik”, “Qani ketdik” kabi so‘zlar.
- Juda uzun izohlar yoki darslik ohangida gaplar.

Postni tabiiy, inson yozgandek uslubda yozing.
"""


    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=promt
            )
            if hasattr(response, "text") and response.text:
                return response.text
            else:
                print(f"Javob bo'sh yoki noto‘g‘ri formatda, urinish {attempt}")
        except Exception as e:
            print(f"Gemini API xato berdi, urinish {attempt}: {e}")
    print(f"{retries} martadan keyin ham javob olmadi 🚨")
    return None


def sending_post():
    print("I am starting")
    for attempt in range(1, 4):
        post_text = ai_response(choosing_topic())
        post_text = post_text.replace("<br>", "\n\n")

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": post_text,
            "parse_mode": "HTML"
        }

        try:
            r = requests.post(url, data=payload)
            r.raise_for_status()  
            print("Post sent successfully!")
            break  

        except requests.exceptions.HTTPError as e:
            if r.status_code == 400:
                print(f"Skipped invalid request: {e}")
                break 
            else:
                print(f"HTTP error on attempt {attempt}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Network error on attempt {attempt}: {e}")

        time.sleep(2)  





