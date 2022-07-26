import time
from datetime import datetime
import threading
from functools import wraps
import random
from argparse import ArgumentParser

import requests

import config


FEISHU_BOT_URL = config.FEISHU_BOT_URL
WAIT_SEC = config.WAIT_SEC
RESTAURANT_SELECTION = config.RESTAURANT_SELECTION


def async_execute(daemon=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            threading.Thread(target=func, args=args, kwargs=kwargs, daemon=daemon).start()
        return wrapper
    return decorator


@async_execute()
def async_notify_feishu(text, title=""):
    try:
        resp = requests.post(FEISHU_BOT_URL, json={
            "msg_type": "text",
            "content": {
                'text': f'{title}\n\n{text}',
            }
        })
        print(resp.content)
    except Exception as e:
        print(e)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--delivery", action="store_true", help="Whether to order delivery at dinner time.")
    parser.set_defaults(delivery=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    if args.delivery:
        lunch_time = (11, 45)
        dinner_time = (18, 0)
        snack_time = (15, 17)
        lunch_text = "午饭时间到！\n天气恶劣，记得点外卖！"
        dinner_text = "晚饭时间到！\n天气恶劣，记得点外卖！"
        snack_text = "零食时间到！\n天气恶劣，记得点外卖！"

    else:
        lunch_time = (12, 45)
        dinner_time = (19, 0)
        lunch_text = "午饭时间到！\n推荐餐厅：" + random.choice(RESTAURANT_SELECTION)
        dinner_text = "晚饭时间到！\n推荐餐厅：" + random.choice(RESTAURANT_SELECTION)
        snack_text = "零食时间到！\n推荐餐厅：" + random.choice(RESTAURANT_SELECTION)
    title = "干饭提醒🍔"
    
    while True:
        cur_time = datetime.now()
        if cur_time.hour == lunch_time[0] and cur_time.minute == lunch_time[1]:
            async_notify_feishu(text=lunch_text, title=title)
        if cur_time.hour == dinner_time[0] and cur_time.minute == dinner_time[1]:
            async_notify_feishu(text=dinner_text, title=title)
        if cur_time.hour == snack_time[0] and cur_time.minute == snack_time[1]:
            async_notify_feishu(text=snack_text, title=title)
        print(f"Current Time: {cur_time}")
        time.sleep(WAIT_SEC)


if __name__ == "__main__":
    main()
