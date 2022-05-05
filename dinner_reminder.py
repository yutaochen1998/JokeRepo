import requests
import time
from datetime import datetime
import threading
from functools import wraps
import config

FEISHU_BOT_URL = config.FEISHU_BOT_URL
WAIT_SEC = config.WAIT_SEC


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


def main():
    while True:
        cur_time = datetime.now()
        title = "干饭提醒🍔"
        if cur_time.hour == 12 and cur_time.minute == 45:
            text = "午饭时间到！"
            async_notify_feishu(text=text, title=title)
        if cur_time.hour == 18 and cur_time.minute == 45:
            text = "晚饭时间到！"
            async_notify_feishu(text=text, title=title)
        print(f"Current Time: {cur_time}")
        time.sleep(WAIT_SEC)


if __name__ == "__main__":
    main()
