"""
Viterbi类
"""
import json
from SplitPinyin import getSplit


class Viterbi:
    def __init__(self, filenames):
        self.filenames = filenames
        self.pi, self.A, self.B, self.S = self.getParameter()

    def getParameter(self):
        data = []
        for filename in self.filenames:
            with open('TrainingData/' + filename + '.json', 'r') as f:
                data.append(json.load(f))
        return data[0], data[1], data[2], data[3]

    def predict(self, seq):
        res = []

        length = len(seq)  # 每一个观测序列的长度，seq[n]是一组观测序列
        dp = {}
        pre = {}
        for i in range(length):
            dp[i] = {}
            pre[i] = {}

        # 初始化
        for s in self.S.get(seq[0]):
            dp[0][s] = self.pi.get(s, 0) * self.B.get(s, {}).get(seq[0], 0)
            pre[0][s] = -1

        # DP
        for i in range(1, length):
            for s in self.S.get(seq[i]):
                dp[i][s] = max(
                    [dp[i - 1][prew] * self.B.get(s, {}).get(seq[i], 0)
                     * self.A.get(s, {}).get(prew, 0) for prew in
                     self.S.get(seq[i - 1])])
                minp = -1
                for z in self.S.get(seq[i - 1]):
                    if dp[i - 1][z] * self.A.get(s, {}).get(z, 0) > minp:
                        minp = dp[i - 1][z] * self.A.get(s, {}).get(z, 0)
                        pre[i][s] = z

        # 获取前10个最可能状态序列
        words_list = sorted(dp[length - 1].items(), key=lambda x: x[1], reverse=True)
        for i in range(min(len(words_list), 20)):
            words = [None] * length
            words[-1] = words_list[i][0]

            for n in range(length - 2, -1, -1):
                words[n] = pre[n + 1][words[n + 1]]

            res.append((i, ''.join(w for w in words), words_list[i][1]))
        res = list(set(res))
        res.sort(key=lambda x: x[0])
        return [(x[1], x[2]) for x in res]


if __name__ == '__main__':
    v = Viterbi(['pi', 'A', 'B', 'STATE'])
    while True:
        print("Please Input:")
        s = getSplit(input())
        while not s:
            print("Wrong Pinyin, Input Again:")
            s = getSplit(input())
        print(v.predict(s))
