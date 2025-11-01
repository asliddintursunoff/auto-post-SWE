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
    prompt = f"""
Siz professional kontent yaratuvchisisiz. Sizning vazifangiz — quyidagi <b>{topic}</b> mavzusi asosida Telegram uchun <b>o'zbek tilida</b> HTML parse formatida (<b>, <i>, <u>, <code>, <pre>, <a>) chiroyli, o‘qilishi yoqimli va hammaga tushunarli post yaratish.

📋 Post yozish qoidalari:
- Post <b>qiziqarli, kreativ va tabiiy ohangda</b> yozilsin.
- Har qanday darajadagi o‘quvchi mavzuni tushuna olsin — texnik atamalar oddiy tilda izohlangan bo‘lsin.
- Post <b>diqqatni tortadigan yoki hazil-mutoyiba, hayotiy misol, yoki noodatiy fakt</b> bilan boshlansin.
- Emoji’lar <b>faqat ohirida emas</b>, balki joyida, matnga mos holda ishlatilsin 😊🔥💡
- Uzunlik mavzuga qarab moslashadi (majburiy 4–6 jumla emas), ammo o‘qishda zeriktirmasligi kerak.
- Matnda o‘quvchini "siz", "sen" kabi so‘zlar bilan bevosita jalb etish mumkin.
- Post yakunida hech qanday “obuna bo‘ling”, “do‘stlaringizga ulashing” yoki shunga o‘xshash chaqiriqlar bo‘lmasin.
- Istalgan joyda quyidagi havoladan foydalanish mumkin, lekin majburiy emas:  
  <b><a href='https://telegram.com/asliddin_tursunoffpy'>asliddin_tursunoff.py</a></b>

🚫 Quyidagilar yozilmasin:
- “Salom obunachilar”, “Keling boshladik”, “Qani ketdik” va shunga o‘xshash kirish gaplar.
- Qo‘shimcha tushuntirish, prompt izohi yoki texnik izohlar.

🎯 Maqsad: O‘quvchi postni bir o‘qishda tushunsin, zavqlansin va unda qiziqish uyg‘onsin.

Mavzu: <b>{topic}</b>
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





