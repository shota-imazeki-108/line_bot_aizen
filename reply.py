from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn
)
from linebot.models import (
    PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import random
from googletrans import Translator
import re


# *************************************
# Replyクラスの作成
# *************************************


class Reply:

    def __init__(self):
        pass

    def __call__(self, text, line_bot_api, event):
        message, is_reply = self.make_messsage(text)
        if is_reply:
            line_bot_api.reply_message(event.reply_token, message)
        return is_reply

    def make_messsage(self, text):
        # デフォルトは送られたメッセージをそのまま返す
        return TextSendMessage(text), True

    def __str__(self):
        return "任意のテキスト: テキストの復唱"


class KuroHitugi(Reply):

    def __init__(self):
        self.eisho = [
            "不遜なる狂気の器\n"
            "湧き上がり・否定し\n"
            "痺れ・瞬き",
            "眠りを妨げる\n"
            "爬行する鉄の王女",
            "絶えず自壊する泥の人形\n"
            "結合せよ\n"
            "反発せよ",
            "地に満ち\n"
            "己の無力を知れ！！"
        ]

    def make_messsage(self, text):
        if text == "黒棺":
            messages = list(map(TextSendMessage, self.eisho))
            img = ImageSendMessage(
                original_content_url="https://shota-imazeki.herokuapp.com/static/kurohitsugi.jpg",
                preview_image_url="https://shota-imazeki.herokuapp.com/static/kurohitsugi.jpg",
            )
            messages.append(img)
            return messages, True
        else:
            return None, False

    def __str__(self):
        return "黒棺: 黒棺の詠唱"


class Koji(Reply):

    def make_messsage(self, text):
        if "こーじ" in text or "こうじ" in text:
            return TextSendMessage("こーじはいらない"), True
        else:
            return None, False

    def __str__(self):
        return "こーじ: xxx"


class Imazeki(Reply):

    def make_messsage(self, text):
        if "今関" in text or "ぜき" in text or "ブル関" in text or "ドーム" in text or "ちんこです" in text or "かわいいちんこ" in text or "ぜっきー" in text:
            return TextSendMessage("今関最高！！"), True
        else:
            return None, False

    def __str__(self):
        return "今関: xxx"


class Help(Reply):

    def make_messsage(self, text):
        if "--help" == text or "-h" == text:
            return self.make_help_message(), True
        else:
            return None, False

    def make_help_message(self):
        help_messages = ["send: reply", "-----------"]
        help_messages.extend(list(map(str, STEPS)))
        help_messages = [
            help_message for help_message in help_messages if help_message != "hidden command"]
        return TextSendMessage("\n".join(help_messages))

    def __str__(self):
        return "--help, -h: help"


class Mugetsu(Reply):

    def __call__(self, text, line_bot_api, event):
        message, is_reply = self.make_messsage(text)
        if is_reply:
            line_bot_api.reply_message(event.reply_token, message)
            # グループトークからの退出処理
            if hasattr(event.source, "group_id"):
                line_bot_api.leave_group(event.source.group_id)

            # ルームからの退出処理
            if hasattr(event.source, "room_id"):
                line_bot_api.leave_room(event.source.room_id)
        return is_reply

    def make_messsage(self, text):
        if text == "無月":
            text = TextSendMessage("馬鹿な！そんな筈があるか！人間如きがこの私を超えるなど！")
            img = ImageSendMessage(
                original_content_url="https://shota-imazeki.herokuapp.com/static/mugetsu.jpg",
                preview_image_url="https://shota-imazeki.herokuapp.com/static/mugetsu.jpg",
            )
            return [text, img], True
        return None, False

    def __str__(self):
        return "無月: 藍染を倒す"


class RandomKuroHitugi(Reply):

    def __init__(self):
        self.eisho = [
            "不遜なる狂気の器\n"
            "湧き上がり・否定し\n"
            "痺れ・瞬き",
            "眠りを妨げる\n"
            "爬行する鉄の王女",
            "絶えず自壊する泥の人形\n"
            "結合せよ\n"
            "反発せよ",
            "地に満ち\n"
            "己の無力を知れ！！"
        ]

    def make_messsage(self, text):
        if random.random() < 0.05:
            messages = list(map(TextSendMessage, self.eisho))
            img = ImageSendMessage(
                original_content_url="https://shota-imazeki.herokuapp.com/static/kurohitsugi.jpg",
                preview_image_url="https://shota-imazeki.herokuapp.com/static/kurohitsugi.jpg",
            )
            messages.append(img)
            return messages, True
        else:
            return None, False

    def __str__(self):
        return "hidden command"


class Hagi(Reply):

    def make_messsage(self, text):
        if "ハギ" in text:
            return TextSendMessage("早く酒飲めよ"), True
        else:
            return None, False

    def __str__(self):
        return "ハギ: xxx"


class RandomUnko(Reply):

    def make_messsage(self, text):
        if random.random() < 0.05:
            return TextSendMessage('ちょっとうんこしてくる'), True
        else:
            return None, False

    def __str__(self):
        return "hidden command"


class Shikai(Reply):

    def make_messsage(self, text):
        if text == "始解":
            text1 = TextSendMessage("砕けろ　鏡花水月")
            img = ImageSendMessage(
                original_content_url="https://shota-imazeki.herokuapp.com/static/aizen.jpg",
                preview_image_url="https://shota-imazeki.herokuapp.com/static/aizen.jpg",
            )
            text2 = TextSendMessage("僕の斬魄刀『鏡花水月』\n有する能力は『完全催眠』だ")
            return [text1, img, text2], True
        return None, False

    def __str__(self):
        return "始解: 始解する"


class Tsujima(Reply):

    def make_messsage(self, text):
        if "辻間" in text or "つーじー" in text:
            return TextSendMessage("クソ野郎"), True
        else:
            return None, False

    def __str__(self):
        return "辻間: xxx"


class Tsunoda(Reply):

    def make_messsage(self, text):
        if "角田" in text or "つのだ" in text:
            return TextSendMessage("角田、スマブラで今関パイセンに20連敗したらしいじゃんwwwww"), True
        else:
            return None, False

    def __str__(self):
        return "角田: xxx"


class Zeebra(Reply):
    def __init__(self):

        self.eisho = [
            "俺は東京生まれHIP HOP育ち 悪そうな奴は大体友達\n"
            "悪そうな奴と大体同じ 裏の道歩き見てきたこの街\n"
            "渋谷 六本木 そう思春期も早々に これにぞっこんに\n"
            "カバンなら置き放っしてきた高校に マジ親に迷惑かけた本当に",
            "だが時は経ち今じゃ雑誌のカヴァー そこらじゅうで幅きかすDON DADA\n"
            "マイク掴んだらマジでNo,1 東京代表トップランカーだ\n"
            "そうこの地この国に生を授かり Jahに無敵のマイク預かり\n"
            "仲間たち親たちファンたちに今日も 感謝して進む荒れたオフロード"
        ]

    def make_messsage(self, text):
        if "zeebra" in text or "Zeebra" in text or "飯田" in text:
            return list(map(TextSendMessage, self.eisho)), True
        else:
            return None, False

    def __str__(self):
        return "zeebra: ラップ"


class Saru(Reply):

    def make_messsage(self, text):
        if "栃木" in text or "群馬" in text:
            return TextSendMessage("猿"), True
        else:
            return None, False

    def __str__(self):
        return "栃木 or 群馬: xxx"


class Tanahii(Reply):

    def make_messsage(self, text):
        if "たなひー" in text:
            return TextSendMessage("田中電池アルファソニックテープ赤リング"), True
        else:
            return None, False

    def __str__(self):
        return "たなひー: 名前"


class Sakai(Reply):

    def make_messsage(self, text):
        if "酒井ちゃん" in text:
            return TextSendMessage("酒井ちゃんのベッドに胡椒ばら撒いといた"), True
        else:
            return None, False

    def __str__(self):
        return "酒井ちゃん: xxx"


class Megu(Reply):

    def make_messsage(self, text):
        for key in ["めぐ", "中野恵"]:
            if key in text:
                if random.random() > 0.5:
                    text = text.replace(key, "おばけキャッチ弱者")
                else:
                    text = text.replace(key, "我孫子のド田舎民")
                return TextSendMessage(text), True
        return None, False

    def __str__(self):
        return "めぐ: replace xxx"


class Sekigahara(Reply):

    def make_messsage(self, text):
        if "関ヶ原" in text:
            return TextSendMessage(""), True
        else:
            return None, False

    def __str__(self):
        return "めぐ: xxx"


class Matsumoto(Reply):

    def make_messsage(self, text):
        if "松本" in text or "まつもと" in text:
            return TextSendMessage("部屋の壁の紙はがせよ"), True
        else:
            return None, False

    def __str__(self):
        return "松本: xxx"


class GoogleTranslater(Reply):

    def make_messsage(self, text):
        if text.startswith('--'):
            tmp = text.split('\n')
            cmd = tmp[0]
            text = '\n'.join(tmp[1:])
            languages = cmd[2:].split('->')
            if len(languages) == 2:
                translator = Translator()
                try:
                    trans = translator.translate(
                        text, src=languages[0], dest=languages[1]).text
                except ValueError:
                    trans = '無効なコードです。\n-h-tを送って、コードを確認してください。'
                return TextSendMessage(trans), True
        return None, False

    def __str__(self):
        return "--xx->yy: 多言語翻訳(help: -h-t)"


class GoogleTranslateHelper(Reply):
    def __init__(self):

        self.eisho = [
            "【多言語翻訳機能の使い方】\n"
            "１行目にformatの通りに翻訳元と翻訳先の言語コードを指定する\n"
            "format: --翻訳元->翻訳先\n"
            "例(英和): --en->ja\n"
            "２行目以降に翻訳したい文を記載する",
            "言語コードについては頻繁に使用されるものを下記に示す\n"
            "日本語: ja\n"
            "英語: en\n"
            "韓国語: ko\n"
            "中国語（簡体）: zh-CN\n"
            "フランス語: fr\n"
            "ドイツ語: de\n"
            "イタリア語: it\n"
            "ロシア語: ru\n"
            "ヘブライ語: he",
            "それ以外の詳細は下記リンクを参照するように\n"
            "https://cloud.google.com/translate/docs/languages?hl=ja"
        ]

    def make_messsage(self, text):
        if "-h-t" == text:
            return list(map(TextSendMessage, self.eisho)), True
        else:
            return None, False

    def __str__(self):
        return "hidden command"


class EasyTranslater(Reply):

    def __init__(self):
        self._lang_dict = {
            "和": "ja",
            "英": "en",
            "韓": "ko",
            "中": "zh-CN",
            "仏": "fr",
            "独": "de",
            "伊": "it",
            "露": "ru",
            "西": "es",
            "ヘ": "he"
        }
        self._re = re.compile(r'^[\u4E00-\u9FD0]{2}')

    def make_messsage(self, text):
        texts = text.split('\n')
        if self._re.fullmatch(texts[0]) is not None:
            if texts[0][0] in self._lang_dict.keys() and texts[0][1] in self._lang_dict.keys() and len(texts) > 1:
                temp = "\n".join(texts[1:])
                src, dest = self._lang_dict[texts[0][0]], self._lang_dict[texts[0][1]]
                translator = Translator()
                try:
                    trans = translator.translate(
                        temp, src=src, dest=dest).text
                except ValueError:
                    trans = 'SystemErrorです。お手数ですが、原因を調査しますので、発生状況を管理者に連絡してください。'
                return TextSendMessage(trans), True
        return None, False

    def __str__(self):
        return "和英: 簡易翻訳(help: -h-et)"


class EasyTranslateHelper(Reply):
    def __init__(self):

        self.eisho = [
            "【簡易翻訳機能の使い方】\n"
            "１行目に例の通りに翻訳元と翻訳先の言語を漢字２文字で指定する\n"
            "１文字目が翻訳元、２文字目が翻訳先の言語を指す\n"
            "例: 和英\n"
            "２行目以降に翻訳したい文を記載する",
            "簡易翻訳機能で扱える言語を下記に示す\n"
            "日本語: 和\n"
            "英語: 英\n"
            "韓国語: 韓\n"
            "中国語（簡体）: 中\n"
            "フランス語: 仏\n"
            "ドイツ語: 独\n"
            "イタリア語: 伊\n"
            "ロシア語: 露\n"
            "スペイン語: 西\n"
            "ヘブライ語: ヘ",
            "それ以外の言語を扱いたい場合は多言語翻訳機能を利用してください(help: -h-t)"
        ]

    def make_messsage(self, text):
        if "-h-et" == text:
            return list(map(TextSendMessage, self.eisho)), True
        else:
            return None, False

    def __str__(self):
        return "hidden command"


class Carousel(Reply):

    def make_messsage(self, text):
        if "オッケー藍染" == text or "オッケーあいぜん" == text:
            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://shota-imazeki.herokuapp.com/static/あつもり_魚.jpg',
                            title='あつもり魚検索機能',
                            text='北 or 南半球、対象月を選択することでその時期に取れる魚の種類と値段が分かります。',
                            actions=[
                                URITemplateAction(
                                    label='ダッシュボードへ',
                                    uri='https://public.tableau.com/profile/.43986973#!/vizhome/bugs/fish_1?publish=yes'
                                )
                            ]
                        ),CarouselColumn(
                            thumbnail_image_url='https://shota-imazeki.herokuapp.com/static/あつもり_虫.jpg',
                            title='あつもり昆虫検索機能',
                            text='北 or 南半球、対象月を選択することでその時期に取れる虫の種類と値段が分かります。',
                            actions=[
                                URITemplateAction(
                                    label='ダッシュボードへ',
                                    uri='https://public.tableau.com/profile/.43986973#!/vizhome/bugs/bugs_1?publish=yes'
                                )
                            ]
                        )
                    ]
                )
            )
            return carousel_template_message, True
        else:
            return None, False

    def __str__(self):
        return "カルーセル: xxx"


class WordCloud(Reply):

    def __init__(self):
        pass

    def make_messsage(self, text):
        text = text.split('\n')
        if text[0] == "ワードクラウド":
            from word_cloud import WordCloudFromTweet
            flg = WordCloudFromTweet().make(' '.join(text[1:]))
            if flg:
                res = ImageSendMessage(
                    original_content_url="https://shota-imazeki.herokuapp.com/static/wordcloud.jpg",
                    preview_image_url="https://shota-imazeki.herokuapp.com/static/wordcloud.jpg",
                )
            else:
                res = TextSendMessage("ワードクラウドが作成できませんでした。15分後程度に再度実行するか管理者に連絡をお願いいたします。")
            return res, True
        else:
            return None, False

    def __str__(self):
        return "ワードクラウド: ワードクラウドの作成"

# *************************************
# WrapperReplyクラスの作成
# *************************************


STEPS = [WordCloud(), Carousel(), Mugetsu(), Help(), EasyTranslater(), EasyTranslateHelper(), GoogleTranslateHelper(), GoogleTranslater(), KuroHitugi(), Shikai(), Koji(), Imazeki(),
         Hagi(), Tsujima(), Tsunoda(), Matsumoto(), Zeebra(), Saru(), Tanahii(), Sakai(), Megu(), RandomKuroHitugi(), RandomUnko(), Reply()]


class WrapperReply:

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        pass

    def reply(self, text):
        for step in STEPS:
            is_reply = step(text, self.line_bot_api, self.event)
            if is_reply:
                break
