import random
import re
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.text import TextCollection
from collections import Counter


def get_wordnet_pos(treebank_tag):  # 得到词性
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''


def read_passage(filename):  # 读文件，分割单词，除去非英文无关内容
    words = []

    with open(filename, 'rt', encoding='utf-8') as f:
        passage = f.read()
        passage = passage.replace("\n", " ").replace(".", " ").replace(",", " ").replace(";", " ").replace(":", " ")

        index = passage.find("Abstract")  # 除去摘要之前内容
        passage = passage[index + 8:]

        index = passage.find("References")  # 除去参考之后内容
        passage = passage[:index + 1]

        words = passage.split()

    return words


txt_list = os.listdir("pdftotext")

passage_word_list = []  # 所有文章的单词列表，按照文章分开
i = 1
for txt in txt_list:
    print("processing " + str(i) + "th passage")
    i += 1

    words = read_passage("pdftotext" + "\\" + txt)

    stop_words = stopwords.words('english')  # 停用词
    new_word = []

    for item in words:  # 除去非英文和停用词并且小写
        if re.match(r'^[A-Za-z-]+$', item) and (len(item) > 1) and (item not in stop_words) and (
                item.lower() not in stop_words):
            new_word.append(item.lower())

    word_pos_tag = nltk.pos_tag(new_word)  # 词性获取
    all_word_list = nltk.corpus.words.words()  # 全部英文单词

    fin_word_list = []  # 每篇文章最终的单词列表

    wordnet_lemmatizer = WordNetLemmatizer()

    for word in word_pos_tag:  # 词性还原
        pos = get_wordnet_pos(word[1])
        if (pos != '') and (word[0] in all_word_list) and (word[0] != 'et') and (word[0] != 'al'):
            fin_word_list.append(wordnet_lemmatizer.lemmatize(word[0], pos))

    passage_word_list.append(fin_word_list)

# 第一种方法 tf-idf
f = open("method1_dic.txt", "w")
text_collection = TextCollection(passage_word_list)

all_word_list = [word for passage in passage_word_list for word in passage]  # 所有文章中的所有单词可重复
i = 1
for passage in passage_word_list:
    vocabulary_set = set([word for word in passage])  # 一个文章中的所有单词不重复

    f.write("passage" + str(i) + '\n')
    i += 1

    passage_dic = {}
    for word in vocabulary_set:  # 每篇文章单词的tf-idf
        word_tf_idf = text_collection.tf_idf(word, all_word_list)
        passage_dic[word] = word_tf_idf

    passage_dic = sorted(passage_dic.items(), key=lambda x: x[1], reverse=True)
    count = 0
    for j in range(0, 20):  # 每篇文章写入tf-idf值前20
        f.write(str(passage_dic[j][0]) + '\t' + str(passage_dic[j][1]) + '\n')
    f.write('\n')

f.close()

# 第二种方法 词频排序
f = open("method2_dic.txt", "w")
word_count = Counter(all_word_list)
word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
all_word_count = len(word_count)
for i in range(0, 900):
    f.write(str(word_count[i][0]) + '\t' + str(word_count[i][1] / all_word_count) + '\n')

f.close()

# 第三种方法 随机数
f = open("method3_dic.txt", "w")
all_word_set = set([word for passage in passage_word_list for word in passage])
random_dic = {}
for word in all_word_set:
    random_dic[word] = random.uniform(0, all_word_count) / all_word_count
random_dic = sorted(random_dic.items(), key=lambda x: x[1], reverse=True)
for i in range(0, 900):
    f.write(str(random_dic[i][0]) + '\t' + str(random_dic[i][1]) + '\n')

f.close()
