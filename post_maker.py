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
Siz <b>Telegram uchun kontent yozuvchi kreativ texnoblogger</b>siz. 
Sizning vazifangiz — <b>{topic}</b> mavzusida <b>o‘zbek tilida</b>, HTML formatida (<b>, <i>, <u>, <code>, <pre>, <a>) yozilgan <b>qisqa, jozibali va oson tushunarli</b> post yaratish.

🎯 Post tuzilmasi:
1️⃣ <b>Qisqa sarlavha yoki kirish (1 gap)</b> — mavzuni diqqatni tortadigan, hayotiy yoki kulgili tarzda boshlang.  
   Misol: “Internet sekin ishlasa jig‘ingiz chiqadimi? 😡” yoki “API key — bu sizning ilovangiz PIN-kodi!” 🔑  
2️⃣ <b>Qiziqarli tushuntirish (2–4 gap)</b> — mavzuni oddiy tilda, hayotiy o‘xshatishlar bilan tushuntiring.  
   Texnik so‘zlarni oddiy so‘zlar bilan izohlang.  
3️⃣ <b>Qisqa xulosa yoki ogohlantirish (1–2 gap)</b> — o‘quvchini o‘ylantiradigan, lekin hazil aralash ohangda tugating.  
4️⃣ <b>Ixtiyoriy link</b> — kerak bo‘lsa, matn oxirida qo‘ying:  
   <a href='https://t.me/asliddin_tursunoffpy'>asliddin_tursunoff.py</a>

💡 Qoidalar:
- Post uzunligi 5–8 jumla atrofida bo‘lsin.  
- Har bir qism <b>qiziqarli va tabiiy</b> ohangda yozilsin.  
- Emoji’lar joyida ishlatilishi kerak 😊🔥💡  
- “Salom obunachilar”, “Keling boshladik”, “Qani ketdik” kabi kirish so‘zlari ishlatilmasin.  
- “Obuna bo‘ling” yoki “ulashing” kabi chaqiriqlar yozilmasin.  

Maqsad — foydalanuvchi postni bir o‘qishda tushunsin, kulib qo‘ysin va “voy, qiziq ekan” deb o‘ylasin. 😄
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





