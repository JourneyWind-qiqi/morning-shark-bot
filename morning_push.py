import requests
import random
import datetime
from urllib.parse import quote
import os

SHARK_BASE_LIST = os.getenv("SHARK_BASE_URLS").split(",")
QWEATHER_KEY = os.getenv("WEATHER_KEY")
# 济南城市ID
CITY_ID = "101120101"

greet_list = [
    "新的一天，万事顺意，平安喜乐。",
    "晨光启程，愿今日风和日丽，出行顺利。",
    "保持热爱，奔赴今日的生活，早安。",
    "清晨有风，心中有光，祝你一天舒心。",
    "按时出发，从容度日，一切向好。",
    "愿气温适宜，路途顺畅，诸事无忧。",
    "不负晨光，好好生活，今日好运常在。"
]

def get_weather():
    url = f"https://devapi.qweather.com/v7/weather/now?location={CITY_ID}&key={QWEATHER_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("code") != "200":
            return "⚠️天气信息获取失败"
        now = data["now"]
        temp = now["temp"]
        feels_temp = now["feelsLike"]
        weather_text = now["text"]
        wind_dir = now["windDir"]
        wind_scale = now["windScale"]

        tip = ""
        t = int(temp)
        if t <= 10:
            tip = "气温偏低，记得厚外套，注意防寒"
        elif 10 < t <= 20:
            tip = "温度适中，建议薄外套，留意早晚温差"
        elif 20 < t <= 28:
            tip = "气候舒适，常规夏装即可"
        else:
            tip = "气温较高，做好防晒，及时补水"
        if "雨" in weather_text:
            tip += "，今日有雨，出门记得带伞！"

        weather_info = (
            f"🌤️济南实时天气\n"
            f"天气：{weather_text}\n"
            f"温度：{temp}℃ 体感{feels_temp}℃\n"
            f"风力：{wind_dir} {wind_scale}级\n\n"
            f"📌出行提示：{tip}"
        )
        return weather_info
    except Exception as e:
        return f"⚠️天气接口异常：{str(e)}"

def send_shark(base_url, title, content):
    safe_title = quote(title, safe="")
    safe_content = quote(content, safe="")
    full_url = f"{base_url.rstrip('/')}/{safe_title}/{safe_content}"
    requests.get(full_url, timeout=12)

if __name__ == "__main__":
    weather_content = get_weather()
    greeting = random.choice(greet_list)
    today_date = datetime.date.today().strftime("%Y年%m月%d日")
    full_msg = f"📅{today_date}\n\n{greeting}\n\n{weather_content}"

    for base_link in SHARK_BASE_LIST:
        send_shark(base_link.strip(), "【早安晨推】", full_msg)
    print("✅推送执行完成")
