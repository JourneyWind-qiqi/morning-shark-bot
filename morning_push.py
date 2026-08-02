import json
import requests
import random
import datetime
from urllib.parse import quote
import os
import pytz  # 新增时区库

# SHARK_BASE_LIST = os.getenv("SHARK_BASE_URLS").split(",")
# QWEATHER_KEY = os.getenv("WEATHER_KEY")
# # 济南城市 ID
# CITY_ID = "101120101"

# ==========【配置区】修改这里 ==========
SHARK_TOKENS = [
    "g5cjSGWfLsNHGvogfk2vs5",
    "8sh4XfkxYRskPGiQ9bEvL4"
]
WEATHER_KEY = "d7612de6ffea7556082bf1c1b019dd98"
CITY_NAME = "济南"
PUSH_TITLE = "早安安~又是美好的一天"
# =======================================

greet_list = [
    "新的一天，万事顺意，期待如约而至",
    "晨光启程，风和日丽，遇见美好",
    "保持热爱，早安，未来可期",
    "清晨有风，祝你一天舒心愉快",
    "按时出发，一切向好",
    "气温适宜，诸事无忧，今天幸运哦",
    "不负晨光，好运常在",
    "美好的一天从现在开始加油！",
    "阳光正好，愿你心情美丽",
    "新的一天，祝你好运连连"
]

noon_greet_list = [
    "中午好，忙碌了一上午辛苦啦",
    "午安，记得吃午饭休息一下",
    "正午时光，补充能量继续加油",
    "中午到了，好好吃饭好好休息",
    "半日已过，下午继续努力呀",
    "阳光正好，享受午餐时光吧",
    "忙碌的上午结束了，该犒劳自己了",
    "午间小憩，让身心都充充电",
    "吃饱喝足，下午元气满满",
    "中场休息时间到，放松一下吧",
    "美好午餐开启美好下午",
    "暂别工作，享受片刻宁静",
    "营养午餐是下午的动力源泉",
    "放下手头的事，先照顾好胃",
    "午后时光慢下来，感受生活美好",
    "一半的时间已过，你很棒哦",
    "午餐时刻，对自己好一点",
    "短暂休整是为了走更远的路",
    "阳光洒在餐桌上，心情也变好了",
    "中午愉快，下午继续发光发热"
]

evening_greet_list = [
    "晚安，今天辛苦了好好休息",
    "夜深了，早点休息明天见",
    "忙碌了一天，该放松下来了",
    "晚安，愿今晚做个好梦",
    "夜色温柔，祝你一夜好眠",
    "卸下疲惫，让心灵得到安宁",
    "今天也很努力，值得好好休息",
    "星星眨眼，是时候入睡了",
    "把烦恼都留在今天，明天重新开始",
    "夜晚是治愈身心的最佳时刻",
    "忙碌的一天结束了，好好犒劳自己",
    "月光洒进窗前，伴你安然入眠",
    "放下手机，享受宁静的夜晚时光",
    "今天的你很棒，明天会更好",
    "夜深人静，正是休息的好时候",
    "感谢今天的努力，现在可以放松了",
    "闭上眼，让梦境带你去远方",
    "世界安静下来，听听内心的声音",
    "一觉醒来，又是崭新的一天",
    "晚安，愿你被这个世界温柔以待",
    "星空守护着你，安心睡吧"
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
    "每天都是新的起点",
    "早安呀~",
    "今天也要棒棒的！",
    "新的一天冲冲冲",
    "又是元气满满的一天",
    "保持微笑，开启美好",
    "今天会有好事发生哦",
    "向着阳光奔跑吧",
    "每一天都值得期待",
    "做个快乐的打工人",
    "美好生活从这里开始"
]

weather_tips = {
    "sunny": [
        "阳光正好适合外出",
        "天气超棒心情美美哒",
        "好天气别浪费啦",
        "约上朋友去户外吧",
        "晴朗日子适合拍照",
        "记得涂防晒霜哦",
        "温暖天适合野餐",
        "阳光足心情也好",
        "好天气让人想唱歌",
        "蓝天白云好运来",
        "晒太阳补维生素D",
        "视野开阔心情舒畅",
        "趁天晴晒晒被子"
    ],
    "cloudy": [
        "多云天适宜出行",
        "紫外线不强放心出门",
        "云淡风轻适合散步",
        "不晒不热刚刚好",
        "可能转晴哦",
        "云朵像棉花糖",
        "拍照自带滤镜",
        "温度舒适不纠结",
        "抬头看看云彩吧",
        "适合户外运动",
        "光线柔和眼睛舒服",
        "云卷云舒静享生活",
        "阴凉适中好散步"
    ],
    "rainy": [
        "记得带伞有备无患",
        "雨天路滑注意安全",
        "出门带好雨具",
        "听雨声也很治愈",
        "适合宅家看书追剧",
        "等雨停再出门",
        "撑伞漫步别样风情",
        "开车骑车要小心",
        "春雨贵如油",
        "关好窗户防雨水",
        "注意防潮防霉",
        "雨中漫步很浪漫",
        "备好雨具从容应对"
    ],
    "cold": [
        "记得加件外套",
        "早晚温差注意保暖",
        "天冷多穿衣",
        "围巾手套安排上",
        "多层穿衣方便增减",
        "注意防风保暖",
        "喝杯热水暖身子",
        "羽绒服派上用场",
        "进出注意添衣",
        "早睡晚起待日光",
        "帽子围巾三件套",
        "低温预热再开车",
        "泡热水澡驱寒气"
    ],
    "hot": [
        "注意防暑降温",
        "多喝水补充水分",
        "避免长时间暴晒",
        "空调温度别太低",
        "午后少外出",
        "清凉饮品解暑",
        "穿透气薄衣物",
        "避免剧烈运动",
        "遮阳伞防晒必备",
        "多吃水果降火",
        "保持通风防闷热",
        "早晚凉爽适合外出",
        "关注高温预警"
    ],
    "normal": [
        "温度适宜好天气",
        "气候舒适啥都行",
        "微风不燥刚刚好",
        "不冷不热最舒适",
        "做什么都合适",
        "空气好适合通风",
        "体感舒适心情美",
        "宜出行的好日子",
        "微风拂面神清爽",
        "珍惜黄金温度",
        "完美平衡不闷不冷",
        "风力柔适合放风筝",
        "气候温和最舒服"
    ]
}

def get_weather_info():
    try:
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={WEATHER_KEY}&city={CITY_NAME}&extensions=all"
        resp = requests.get(url, timeout=10)
        print(f"天气API状态码: {resp.status_code}")
        print(f"天气API响应: {resp.text[:300]}")

        data = resp.json()

        if data.get("status") == "1":
            if data.get("forecasts"):
                forecast = data["forecasts"][0]
                today_cast = forecast["casts"][0] if forecast.get("casts") else None
                if today_cast:
                    return {
                        "temp_low": today_cast["nighttemp"],
                        "temp_high": today_cast["daytemp"],
                        "weather": today_cast.get("dayweather", ""),
                        "windDir": today_cast.get("daywind", ""),
                        "windPower": today_cast.get("daypower", ""),
                        "city": forecast["city"]
                    }
            elif data.get("lives"):
                live = data["lives"][0]
                return {
                    "temp": live["temperature"],
                    "temp_low": live["temperature"],
                    "temp_high": live["temperature"],
                    "weather": live["weather"],
                    "windDir": live["winddirection"],
                    "windPower": live["windpower"],
                    "humidity": live["humidity"]
                }
            print(f"❌ 高德天气API返回数据异常")
        else:
            print(f"❌ 高德天气API返回错误: {data.get('info', '未知错误')}")
    except Exception as e:
        print(f"⚠️ 天气API请求异常: {e}")
    return None

def get_weather_tip(weather):
    if not weather:
        return random.choice(weather_tips["normal"])

    temp_high = int(weather.get("temp_high", weather.get("temp", 20)))
    temp_low = int(weather.get("temp_low", weather.get("temp", 20)))
    temp_avg = (temp_high + temp_low) // 2
    weather_text = weather.get("weather", "").lower()

    if "雨" in weather_text:
        return random.choice(weather_tips["rainy"])
    elif "晴" in weather_text and temp_avg >= 28:
        return random.choice(weather_tips["hot"])
    elif "晴" in weather_text or "多云" in weather_text:
        return random.choice(weather_tips["sunny"])
    elif "阴" in weather_text or "云" in weather_text:
        return random.choice(weather_tips["cloudy"])
    elif temp_low <= 10:
        return random.choice(weather_tips["cold"])
    elif temp_high >= 28:
        return random.choice(weather_tips["hot"])
    else:
        return random.choice(weather_tips["normal"])

def get_weather_icon(weather):
    if not weather:
        return "🌡️"
    
    weather_text = weather.get("weather", "").lower()
    
    if "晴" in weather_text:
        return "☀️"
    elif "多云" in weather_text:
        return "⛅"
    elif "阴" in weather_text:
        return "☁️"
    elif "雨" in weather_text:
        return "🌧️"
    elif "雪" in weather_text:
        return "❄️"
    elif "雾" in weather_text or "霾" in weather_text:
        return "🌫️"
    elif "雷" in weather_text or "暴" in weather_text:
        return "⛈️"
    else:
        return "🌤️"

def get_cn_now():
    tz_cn = pytz.timezone("Asia/Shanghai")
    return datetime.datetime.now(tz_cn)

def get_weekday_desc():
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_descs = [
        "普通星期一",
        "牛马星期二",
        "盒马星期三",
        "期待星期四",
        "美好星期五",
        "哈哈星期六",
        "惬意星期日"
    ]

    today_weekday = get_cn_now().weekday()
    return weekday_descs[today_weekday]

SEND_WINDOWS = {
    "morning": (5, 8.5),
    "noon":    (11, 12.5),
    "evening": (20, 23),
}

def get_current_window():
    now = get_cn_now()
    cur_hour = now.hour + now.minute / 60
    for period, (start, end) in SEND_WINDOWS.items():
        if start <= cur_hour < end:
            return period
    return None

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "send_state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_noon_tip():
    noon_tips = [
        "🍱记得按时吃饭，身体是革命的本钱",
        "☕喝杯水休息一下，下午继续加油",
        "🌞午后小憩15分钟，精神会更好哦",
        "📵放下手机，享受片刻宁静时光",
        "💪半程已过，坚持就是胜利"
    ]
    return random.choice(noon_tips)

def get_evening_tip():
    evening_tips = [
        "🌙放下一天的疲惫，好好放松自己",
        "📖睡前看会儿书，让心灵安静下来",
        "🎵听听轻音乐，缓解一天的压力",
        "✨回顾今天的收获，明天会更好",
        "🛏️早点休息，充足的睡眠很重要"
    ]
    return random.choice(evening_tips)

def get_full_content(time_period):
    cn_now = get_cn_now()
    today = cn_now.strftime('%Y年%m月%d日')
    weekday_desc = get_weekday_desc()

    print(f"\n⏰ 北京时间: {cn_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 发送时段: {time_period} (早5:00-8:30 / 午11:00-12:30 / 晚19:00-23:00)")

    if time_period == "morning":
        greet = random.choice(greet_list).rstrip('')
        weather = get_weather_info()
        if weather:
            tip = get_weather_tip(weather)
            icon = get_weather_icon(weather)
            temp_low = weather.get('temp_low', weather.get('temp', '--'))
            temp_high = weather.get('temp_high', weather.get('temp', '--'))
            weather_line = f"{icon}{weather['weather']} {temp_low}~{temp_high}℃ {tip}"
        else:
            weather_line = "🌡️天气获取失败"

        content = (
            f"📅今天是{today}  {weekday_desc}|"
            f"☀️{greet}|"
            f"{weather_line}"
        )
    elif time_period == "noon":
        noon_greet = random.choice(noon_greet_list)
        noon_tip = get_noon_tip()

        content = (
            f"📅今天是{today}  {weekday_desc}|"
            f"🌤️{noon_greet}|"
            f"{noon_tip}"
        )
    else:
        evening_greet = random.choice(evening_greet_list)
        evening_tip = get_evening_tip()

        content = (
            f"📅今天是{today}  {weekday_desc}|"
            f"🌙{evening_greet}|"
            f"{evening_tip}"
        )

    print(f"\n=== 原始内容 ===")
    print(content)
    print(f"\n=== 编码后内容 ===")
    from urllib.parse import quote
    encoded = quote(content.encode('utf-8'), safe='')
    print(encoded)
    print(f"\n原始长度: {len(content)}")
    print(f"编码后长度: {len(encoded)}")

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
            # push_url = f"https://shark.xiaobingkj.com/{token}/{encoded_title}/{encoded_sub_title}?style=3&inboxContent={encoded_content}"
            push_url = f"https://shark.xiaobingkj.com/{token}/{title}/{sub_title}?style=3&inboxContent={content}"
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
    cn_now = get_cn_now()
    today_str = cn_now.strftime("%Y-%m-%d")
    print(f"🚀 脚本启动，北京时间: {cn_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🕒 发送窗口配置: 早5:00-8:30、午11:00-12:30、晚19:00-23:00")

    current_window = get_current_window()
    if current_window is None:
        print(f"⏭️  当前不在任何发送窗口内，跳过本次执行")
        exit(0)

    print(f"📍 当前属于 [{current_window}] 时段窗口")

    state = load_state()
    print(f"📋 已发送状态: {state}")

    if state.get("date") == today_str and state.get(current_window):
        print(f"⏭️  今天[{today_str}]的[{current_window}]时段已经发过了，跳过重复发送")
        exit(0)

    print(f"✅ 未发送过，开始推送[{current_window}]时段消息...")

    if current_window == "morning":
        title = "早安安~又是美好的一天"
        subtitle = random.choice(subtitle_list)
    elif current_window == "noon":
        title = "午安安~忙碌了一上午辛苦啦"
        subtitle = "记得好好休息哦"
    else:
        title = "晚安安~今天辛苦了早点休息"
        subtitle = "做个好梦"

    msg_content = get_full_content(current_window)
    send_shark_inbox(title, subtitle, msg_content)

    new_state = state if state.get("date") == today_str else {"date": today_str}
    new_state[current_window] = True
    new_state["last_send_time"] = cn_now.strftime("%Y-%m-%d %H:%M:%S")
    save_state(new_state)
    print(f"💾 状态已保存: {new_state}")
    print("✅推送完成！下拉通知查看完整大窗口")
