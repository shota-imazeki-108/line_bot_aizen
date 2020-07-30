import re
import json
import time
import collections
import matplotlib.pyplot as plt

from requests_oauthlib import OAuth1Session
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from PIL import Image
import numpy as np


class WordCloudFromTweet:
    KEYS = {  # 自分のアカウントで入手したキーを記載
        'consumer_key': 'n8ZeIZq7fUOZorwyQA2k6mkRj',
        'consumer_secret': '3ofR6fAkL7c94kgP7PfgFJ4GAbdwXSDlJpdG6GPac6VWIUlyLM',
        'access_token': '1279369007749980160-wbS96jVWFj49xZakOZ1ahYaqcLkrb9',
        'access_secret': 'YFE981VvUE1f0M1gxCbzPmcTRPnf2AGLRk48onxJxAp6U',
    }
    twitter = OAuth1Session(KEYS['consumer_key'], KEYS['consumer_secret'],
                            KEYS['access_token'], KEYS['access_secret'])
    url = "https://api.twitter.com/1.1/search/tweets.json"
    # locations = {
    #     '北海道': [43.0351, 141.2049],
    #     '宮城': [38.1608, 140.5219],
    #     '東京': [35.4122, 139.4130],
    #     '大阪': [35.4111, 135.3112],
    #     '広島': [34.2347, 132.2734],
    #     '福岡': [33.3623, 130.2505]
    # }
    locations = {
        '東京': [35.4122, 139.4130]
    }
    shape_path = './shape/twitter_shape.jpg'
    font_path = './font/GenShinGothic-Bold.ttf'

    def __init__(self):
        pass

    def make(self, word: str):
        try:
            tweets = []
            for location in self.locations.values():
                time.sleep(1)
                tmp = self.get_twitter_data(
                    word, location[0], location[1], 100, repeat=1)
                tweets.append(tmp)
            freq_dict = self.count_word(tweets, word)
            self.draw_word_cloud(freq_dict)
            return True
        except Exception:
            return False

    def get_twitter_data(self, key_word, latitude, longitude, radius, repeat=3):
        print(f'get tweet : {key_word}')
        params = {'q': key_word, 'count': '100', 'geocode': '%s,%s,%skm' % (
            latitude, longitude, radius), 'result_type': 'recent'}  # 取得パラメータ
        tweets = []
        mid = -1

        for i in range(repeat):
            params['max_id'] = mid  # midよりも古いIDのツイートのみを取得する
            res = self.twitter.get(self.url, params=params)
            if res.status_code == 200:  # 正常通信出来た場合
                sub_tweets = json.loads(
                    res.text)['statuses']  # レスポンスからツイート情報を取得
                for tweet in sub_tweets:
                    tweets.append(tweet)
            else:  # 正常通信出来なかった場合(2018/9/24に修正しました)
                print("Failed: %d" % res.status_code)

        return tweets

    def exclude_words(self, text, words):
        if text in '質問箱':
            return ''
        if text.startswith('RT '):
            text = text[2:]
        text = re.sub(r'@([a-z0-9]+)', '', text)
        text = re.sub(r'http[s*]://[a-z0-9./]+', '', text)
        words_list = words.split()
        for word in words_list:
            text = text.replace(word, '')
        return text

    def count_word(self, tweet_list, words):
        print(f'count word')
        tmp = [self.exclude_words(tweet["text"], words)
               for tweets in tweet_list for tweet in tweets]

        all_tweet = "\n".join(tmp)

        t = Tokenizer()
        tokens = [token.base_form for token in t.tokenize(all_tweet) if (token.part_of_speech.startswith(
            '名詞') or token.part_of_speech.startswith('形容詞') or token.part_of_speech.startswith('動詞')) and len(token.base_form) > 1]
        c = collections.Counter(tokens)  # 原形に変形、名詞のみ、1文字を除去

        freq_dict = {}
        mc = c.most_common()
        for elem in mc:
            if re.fullmatch(r'[ぁ-ん]{1,2}', elem[0]) is not None:  # 簡易的なstop word
                continue
            freq_dict[elem[0]] = elem[1]

        return freq_dict

    def draw_word_cloud(self, word_freq_dict):
        print(f'make word cloud')
        mask_array = np.array(Image.open(self.shape_path))
        wordcloud = WordCloud(background_color='white', min_font_size=5, font_path=self.font_path,
                              max_font_size=100, width=100, height=100, mask=mask_array)
        wordcloud.generate_from_frequencies(word_freq_dict)
        plt.figure(figsize=[20, 20])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig('./static/wordcloud.jpg', bbox_inches='tight')
