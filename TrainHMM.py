"""
训练hmm模型的三个参数，并保存在json文件中，避免每次运行都要重新计算参数
"""
import re
import os
import pypinyin
import json


def load():
    file = 'corpus/corpus_processed.txt'
    chinese = re.compile(r'[\u4e00-\u9fa5]{2,}')
    with open(file, 'r', encoding='utf-8') as f:
        seqs = chinese.findall(f.read())
    return seqs


class HMM:
    def __init__(self, data):
        self.data = data
        self.pi = self.get_pi()  # 初始状态概率
        self.A = self.get_A()  # 转移矩阵
        self.B = self.get_B()  # 发射矩阵
        self.S = self.get_state()

    def get_pi(self):
        """
        初始状态概率
        :param self.data:
        :return:
        """
        l = len(self.data)
        pi = {}
        for s in self.data:
            if len(s) == 0:
                continue
            if s[0] not in pi:
                pi[s[0]] = 1
            else:
                pi[s[0]] += 1
        for key in pi.keys():
            pi[key] = pi.get(key) / l

        self.writing(filename='PI', data=pi)
        print("pi finished!")
        return pi
        # print(pi)

    def get_A(self):
        """
        转移矩阵
        :param self.data:
        :return:
        """
        # l = len(self.data)
        a = {}
        for s in self.data:
            lst = list(s)
            lst.insert(0, 'BOS')
            lst.append('EOS')
            for index, word in enumerate(lst):
                if index:
                    preword = lst[index - 1]
                    if lst[index] not in a:
                        a[lst[index]] = {}
                    a[lst[index]][preword] = a[lst[index]].get(preword, 0) + 1
        for word in a.keys():
            count = sum(a.get(word).values())
            for pre in a.get(word).keys():
                a[word][pre] = a[word][pre] / count
        # print(a)
        self.writing(filename='A', data=a)
        print("a finished!")
        return a

    def get_B(self):
        """
        发射矩阵
        :param self.data:
        :return:
        """
        # l = len(self.data)
        b = {}
        for s in self.data:
            pylst = pypinyin.lazy_pinyin(s)
            for pinyin, word in zip(pylst, s):
                if word not in b:
                    b[word] = {}
                b[word][pinyin] = b[word].get(pinyin, 0) + 1

        for word in b.keys():
            count = sum(b.get(word).values())
            for py in b.get(word).keys():
                b[word][py] = b[word][py] / count
        # print(b)
        self.writing(filename='B', data=b)
        print("b finished!")
        return b

    def get_state(self):

        with open('TrainingData' + '/B.json') as f:
            b = json.load(f)

        data = {}
        for key in b.keys():
            for pinyin in b.get(key):
                if not data.get(pinyin, None):
                    data[pinyin] = []
                data[pinyin].append(key)

        self.writing(filename='STATE', data=data)
        print("state finished!")
        return data

    def writing(self, filename, data):
        """
        写入数据
        :return:
        """
        os.remove(path='TrainingData' + '/' + filename + '.json')
        with open('TrainingData' + '/' + filename + '.json', 'w') as f:
            json.dump(data, f, indent=2)


def training():
    a = load()
    hmm = HMM(a)


def update():
    fr = open(file='corpus/updated.txt', mode='r', encoding='utf-8', errors='ignore')
    fw = open(file='corpus/corpus_processed.txt', mode='a+', encoding='utf-8', errors='ignore')
    for s in fr:
        for i in range(100):
            fw.write(s)
    fr.close()
    fw.close()
    os.remove(file='corpus/updated.txt')
    x = load()
    hmm = HMM(x)
    print("update finished!")


if __name__ == '__main__':
    update()
