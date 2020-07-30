from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage
)
import os
from reply import WrapperReply
from environ import ROOT, ACCESS_TOKEN, CHANNEL_SECRET
from pathlib import Path

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ[ACCESS_TOKEN]
YOUR_CHANNEL_SECRET = os.environ[CHANNEL_SECRET]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN, timeout=5)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "test:Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return
    # 退出処理
    if event.message.text == "無月":
        text = TextSendMessage("馬鹿な！そんな筈があるか！人間如きがこの私を超えるなど！")
        img = ImageSendMessage(
            original_content_url="https://shota-imazeki.herokuapp.com/static/mugetsu.jpg",
            preview_image_url="https://shota-imazeki.herokuapp.com/static/mugetsu.jpg",
        )
        line_bot_api.reply_message(event.reply_token, [text, img])

        # グループトークからの退出処理
        if hasattr(event.source, "group_id"):
            line_bot_api.leave_group(event.source.group_id)

        # ルームからの退出処理
        if hasattr(event.source, "room_id"):
            line_bot_api.leave_room(event.source.room_id)

        return

    WrapperReply(line_bot_api, event).reply(event.message.text)
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=text))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id

    src_image_path = "static/{}.jpg".format(message_id)

    # 画像を保存
    save_image(message_id, src_image_path)

    # 画像の送信
    image_message = ImageSendMessage(
        original_content_url=f"https://shota-imazeki.herokuapp.com/{src_image_path}",
        preview_image_url=f"https://shota-imazeki.herokuapp.com/{src_image_path}",
    )
    line_bot_api.reply_message(event.reply_token, image_message)


def save_image(message_id: str, save_path: str) -> None:
    message_content = line_bot_api.get_message_content(message_id)
    with open(Path(save_path).absolute(), "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
