import json
import requests
import random
import datetime
from urllib.parse import quote
import os

# SHARK_BASE_LIST = os.getenv("SHARK_BASE_URLS").split(",")
# QWEATHER_KEY = os.getenv("WEATHER_KEY")
# # 济南城市 ID
# CITY_ID = "101120101"

# ==========【配置区】修改这里 ==========
SHARK_TOKENS = [
    "g5cjSGWfLsNHGvogfk2vs5",
    "8sh4XfkxYRskPGiQ9bEvL4"
]
WEATHER_KEY = "646402d17b0a4fd6a6e925a826a860de"
CITY_ID = "101120101"
PUSH_TITLE = "早安安~又是美好的一天"
PUSH_SUBTITLE = "早安安~又是美好的一天" # 第三段路径 副标题
# =======================================

greet_list = [
    "新的一天，万事顺意，平安喜乐。",
    "晨光启程，愿今日风和日丽，出行顺利。",
    "保持热爱，奔赴今日的生活，早安。",
    "清晨有风，心中有光，祝你一天舒心。",
    "按时出发，从容度日，一切向好。",
    "愿气温适宜，路途顺畅，诸事无忧。",
    "不负晨光，好好生活，今日好运常在。",
    "美好的一天从现在开始，加油！",
    "阳光正好，微风不燥，愿你心情美丽。",
    "新的一天新的开始，祝你好运连连。",
    "早晨的阳光最温暖，愿它照亮你的一天。",
    "今天也要元气满满哦！",
    "愿所有美好如期而至，早安。",
    "每一天都是限量版，好好珍惜今天。"
]

subtitle_list = [
    "又是美好的一天~",
    "早安，加油！",
    "新的一天开始啦",
    "今天也要开心鸭",
    "元气满满的一天",
    "愿你今天好运连连",
    "保持热爱，奔赴生活",
    "美好从清晨开始",
    "阳光总在风雨后",
    "每天都是新的起点"
]

weather_tips = {
    "sunny": [
        "☀️阳光明媚，适合外出走走哦~",
        "🌞今天天气超棒，心情也要美美哒",
        "☀️这么好的天气，别浪费啦"
    ],
    "cloudy": [
        "☁️多云天气，温度适宜出行",
        "🌤️云层遮挡，紫外线不强",
        "⛅今天云淡风轻，很适合散步"
    ],
    "rainy": [
        "🌧️记得带伞，有备无患",
        "💧雨天路滑，注意安全",
        "☔今天有雨，出门记得带雨具"
    ],
    "cold": [
        "❄️气温偏低，记得加件外套",
        "🧥早晚温差大，注意保暖",
        "🌬️天冷了，多穿点衣服哦"
    ],
    "hot": [
        "🌡️气温较高，注意防暑降温",
        "🔥今天较热，多喝水补充水分",
        "☀️高温天气，避免长时间暴晒"
    ],
    "normal": [
        "🌡️温度适宜，是个好天气",
        "🌤️气候舒适，适合各种活动",
        "💨微风不燥，刚刚好"
    ]
}

def get_weather_info():
    try:
        url = f"https://devapi.qweather.com/v7/weather/now?location={CITY_ID}&key={WEATHER_KEY}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, timeout=10, headers=headers)
        print(f"天气API状态码: {resp.status_code}")
        print(f"天气API响应: {resp.text[:200]}")

        data = resp.json()

        if resp.status_code == 403:
            return None

        if data.get("code") == "200":
            now = data["now"]
            return {
                "temp": now["temp"],
                "feelsLike": now["feelsLike"],
                "text": now["text"],
                "windDir": now["windDir"],
                "windScale": now["windScale"]
            }
        else:
            print(f"❌ 天气API返回错误: {data}")
    except Exception as e:
        print(f"⚠️ 天气API请求异常: {e}")
    return None

def get_weather_tip(weather):
    if not weather:
        return random.choice(weather_tips["normal"])

    temp = int(weather["temp"])
    text = weather["text"].lower()

    if "雨" in text:
        return random.choice(weather_tips["rainy"])
    elif "晴" in text and temp >= 28:
        return random.choice(weather_tips["hot"])
    elif "晴" in text or "多云" in text:
        return random.choice(weather_tips["sunny"])
    elif "阴" in text or "云" in text:
        return random.choice(weather_tips["cloudy"])
    elif temp <= 10:
        return random.choice(weather_tips["cold"])
    elif temp >= 28:
        return random.choice(weather_tips["hot"])
    else:
        return random.choice(weather_tips["normal"])

def get_full_content():
    today = datetime.date.today().strftime('%Y年%m月%d日')
    greet = random.choice(greet_list)

    weather = get_weather_info()
    if weather:
        tip = get_weather_tip(weather)
        weather_line = f"🌤️{weather['text']} | {weather['temp']}℃ {tip}"
    else:
        weather_line = "⚠️天气信息获取失败"

    content = (
        f"📅今天是{today}\n"
        f"☀️{greet}\n"
        f"{weather_line}"
    )
    return content

def send_shark_inbox(title, sub_title, content):
    from urllib.parse import quote
    encoded_title = quote(title, safe="")
    encoded_sub_title = quote(sub_title, safe="")
    # 【关键】对中文和特殊字符进行URL编码，保留基本可读性
    encoded_content = quote(content.encode('utf-8'), safe='')

    # 批量推送到所有设备
    for idx, token in enumerate(SHARK_TOKENS, 1):
        try:
            push_url = f"https://shark.xiaobingkj.com/{token}/{encoded_title}/{encoded_sub_title}?style=3&inboxContent={encoded_content}"
            resp = requests.get(push_url, timeout=15)
            print(f"\n📱 设备 {idx}/{len(SHARK_TOKENS)} 推送结果:")
            print(f"   Token: {token[:10]}...")
            print(f"   推送链接: {push_url}")
            print(f"   接口返回: {resp.text}")

            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 200:
                    print(f"   ✅ 设备{idx}推送成功!")
                else:
                    print(f"   ❌ 设备{idx}推送失败: {data.get('message')}")
            else:
                print(f"   ❌ 设备{idx}请求失败: HTTP {resp.status_code}")

        except Exception as e:
            print(f"   ❌ 设备{idx}异常: {e}")

    print("\n原始内容：", content)

if __name__ == "__main__":
    msg_content = get_full_content()
    random_subtitle = random.choice(subtitle_list)
    send_shark_inbox(PUSH_TITLE, random_subtitle, msg_content)
    print("✅推送完成！下拉通知查看完整大窗口")
