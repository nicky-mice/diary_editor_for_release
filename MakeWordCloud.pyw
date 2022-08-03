import re
import os
import sys
from glob import iglob
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer

FONT_PATH = "NotoSansJP-Bold.otf"
TXT_NAME = ''

def load_file(file):

    _text = ''

    for path in iglob(file):
        with open(path, 'r', encoding='utf-8') as f:
            _text += f.read().strip()

    return _text

def get_word_str(text):

    t = Tokenizer()
    token = t.tokenize(text)
    word_list = []

    for line in token:
        tmp = re.split('\t|,', str(line))

        print(tmp)

        #名詞のみ対象
        if tmp[1] in ["名詞"] and tmp[2] in ["一般", "固有名詞"]:
            word_list.append(tmp[0])

    return " ".join(word_list)



def make_word_cloud(word_str):

    #画像作成
    wc = WordCloud(background_color="white",font_path=FONT_PATH, max_font_size=40).generate(word_str)

    #画像保存
    wc.to_file("wordcloud.png")



def main(*files):
    input_text = ''

    for file in files:
        input_text += load_file(file)

    make_word_cloud(get_word_str(input_text))


if __name__ == '__main__':
    main('*.txt')


#参考リンク
#
#WordCloud（ワードクラウド）を日本語で作成する【Python】
#https://self-development.info/wordcloud%ef%bc%88%e3%83%af%e3%83%bc%e3%83%89%e3%82%af%e3%83%a9%e3%82%a6%e3%83%89%ef%bc%89%e3%82%92%e6%97%a5%e6%9c%ac%e8%aa%9e%e3%81%a7%e4%bd%9c%e6%88%90%e3%81%99%e3%82%8b%e3%80%90python%e3%80%91/
#
#Windowsで簡単に形態素解析をする方法【Python + Janome
#https://self-development.info/windows%e3%81%a7%e7%b0%a1%e5%8d%98%e3%81%ab%e5%bd%a2%e6%85%8b%e7%b4%a0%e8%a7%a3%e6%9e%90%e3%82%92%e3%81%99%e3%82%8b%e6%96%b9%e6%b3%95%e3%80%90python-janome%e3%80%91/
#
#pythonはver3.6以上