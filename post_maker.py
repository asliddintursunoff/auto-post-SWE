from swe_topics import SWE_TOPICS_EXTENDED

import requests
from google import genai
import os
from dotenv import load_dotenv
import random
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
Siz professional kontent yaratuvchisisiz. Sizning vazifangiz — quyidagi {topic} asosida Telegram uchun <b>o'zbek tilida</b>, HTML parse yordamida (<b>, <i>, <u>, <code>, <pre>, <a>) chiroyli, tushunarli va qiziqarli post yaratish. Post shunday bo‘lsinki:

- O‘quvchi har qanday darajada bo‘lishidan qat’i nazar, mavzuni tushunadi.
- Post interaktiv, hazil-mutoyiba yoki qiziqarli faktlar bilan boyitilgan bo‘lishi mumkin.
- Emoji’lar <b>faqat ohirida emas</b>, gaplarga mos ravishda kreativ ishlatilishi mumkin.
- Uzunligi mavzu hajmiga qarab moslashadi; 4-6 jumla majburiy emas.
- Postni o‘quvchi sevib o‘qishi va oson tushunishi kerak.
- Faqat post matnini chiqarish, tushuntirish yoki qo‘shimcha izoh yozmang.
- Telegram kanal linki <b><a href='https://telegram.com/asliddin_tursunoffpy'>asliddin_tursunoff.py</a></b>
- Telegram kanal linkini qushish majburiy emas obuna bo'ling degan gaplar ham yozilmasin! agarda link kerak bo'lib qolsa ishlat
- Hech qanday salom obunachilar va qani ketdik qani boshladik va shunga o'xshash narsalarni yozilmasin!

Mavzu: {topic}
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
    for _ in range(3):
        post_text = ai_response(choosing_topic())
        
        post_text = post_text.replace("<br>", "\n\n")

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": post_text,
            "parse_mode": "HTML"
        }
        r = requests.post(url, data=payload)      
        try:
            if r.status_code == 400:
                pass
            else:
                break            
        except Exception as e:
            print("Javobni o'qib bo'lmadi:", e)

    




