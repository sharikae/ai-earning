# -*- coding: utf-8 -*-
"""
遺伝的アルゴリズム
"""
import random
import sys

__author__ = "Shota Harikae"
__version__ = "1.0"
__date__ = "23 Aug 2018"


class GA:
    def __init__(self, pop_size=5, g_length=10, max_gen=20, m_rate=0.1):
        """
        クラスの初期化
        引数に基づいて定数の設定と遺伝子のセットアップを行う

        :param pop_size: 個体数(奇数にすること)
        :param g_length:　個体の遺伝子型のビット数
        :param max_gen:　世代数
        :param m_rate:　突然変異率(0-1)
        """

        self.POP_SIZE = pop_size
        self.G_LENGTH = g_length
        self.MAX_GEN = max_gen
        self.M_RATE = m_rate

        self.gene = self.init_gene(self.POP_SIZE, self.G_LENGTH)
        self.fitness = self.calc_fitness(self.gene)
        self.file = open('result.dat', 'w')
        self.t = 0

    @staticmethod
    def init_gene(pop_size, g_length):
        """
        遺伝子の初期化
        0,1の遺伝子を作成
        初期化時にも呼ばれるためstaticmethodとする

        :param pop_size:　
        :param g_length:
        :return:　初期化された遺伝子配列を返却
        """

        population = []
        for i in range(pop_size):
            population.append([random.randint(0, 1) for _ in range(g_length)])
        return population

    @staticmethod
    def calc_fitness(gene):
        """
        適応度の計算
        前半の5bitは0の数 後半の5bitは1の数
        初期化時にも呼ばれるためstaticmethodとする

        :param gene: 遺伝子配列
        :return:
        """

        fitness = []
        for p in gene:
            count_bit = 0
            count_bit += p[0:5].count(0)
            count_bit += p[5:10].count(1)
            fitness.append(count_bit)
        return fitness

    def __output_file(self, _t, _avg_fit, _max_fit):
        """
        datファイルへの書き出し

        :param _t:  世代数
        :param _avg_fit: 平均適応度
        :param _max_fit: 最大適応度
        :return: None
        """
        self.file.write('{} {} {}\n'.format(_t, _avg_fit, _max_fit))

    def __avg_fit(self):
        """
        平均適応度の計算

        :return: 平均適応度
        """
        return sum(self.fitness) / self.POP_SIZE

    def __max_fit(self):
        """
        最大適応度の計算

        :return: 最大適応度
        """
        return max(self.fitness)

    def show_gene(self):
        """
        遺伝子の表示
        最大適応度、平均適応度の表示
        ファイルへの書き込み依頼
        :return: None
        """

        for g, f in zip(self.gene, self.fitness):
            print('個体 {0} , 適応度 {1}'.format(g, f))

        print('平均適応度 : {}'.format(self.__avg_fit()))
        print('最大適応度 : {}'.format(self.__avg_fit()))

        self.__output_file(self.t, self.__avg_fit(), self.__max_fit())

    def __swap_gene(self, p1, p2):
        """
        個体番号 p1 と p2 の適応度と遺伝子を交換

        :param p1: 移動先
        :param p2: 個体番号

        :return: None
        """
        self.gene[p1][:], self.gene[p2][:] = self.gene[p2][:], self.gene[p1][:]
        self.fitness[p1], self.fitness[p2] = self.fitness[p2], self.fitness[p1]

    def __copy_gene(self, p1, p2):
        """
        個体番号 p1 の適応度と遺伝子型を p2 にコピー
        :param p1: 個体番号
        :param p2: 遺伝子型

        :return: None
        """
        self.gene[p2][:] = self.gene[p1][:]
        self.fitness[p2] = self.fitness[p1]

    def elite(self):
        """
        エリート保存
        最大適応度の個体(max_p)と最小適応度の個体(min_p)を見つける
        最小適応度の個体に最大適応度の個体のデータをコピー
        最大適応度の個体を0番目に移動

        :return: None
        """

        max_p = self.fitness.index(max(self.fitness))
        min_p = self.fitness.index(min(self.fitness))
        self.__copy_gene(max_p, min_p)
        self.__swap_gene(0, max_p)

    def reproduction(self):
        """
        ルーレット選択
        ルーレットの1周分 sum_of_fitness を求める
        ルーレットを POP_SIZE 回だけ回して次世代の個体を選ぶ
        選ばれた場所に該当する個体が何番か調べる

        :return: None
        """

        sum_of_fitness = sum(self.fitness)
        new_gene = [[0 for _ in range(self.G_LENGTH)] for _ in range(self.POP_SIZE)]

        for p in range(1, self.POP_SIZE):
            r = sum_of_fitness * random.random()
            num = 0
            border = self.fitness[0]

            while border < r:
                num += 1
                border += self.fitness[num]

            for i in range(self.G_LENGTH):
                new_gene[p][i] = self.gene[num][i]

        for p in range(1, self.POP_SIZE):
            for i in range(self.G_LENGTH):
                self.gene[p][i] = new_gene[p][i]

    def crossover(self):
        """
         一点交叉
        交叉位置を1〜G_LENGTH-1の範囲でランダムに決め、
        それより後ろを入れ替える。

        :return: None
        """

        c_pos = random.randint(1, self.G_LENGTH - 1)
        for i in range(1, self.POP_SIZE, 2):
            self.gene[i][c_pos:self.G_LENGTH], self.gene[i + 1][c_pos:self.G_LENGTH] = \
                self.gene[i + 1][c_pos:self.G_LENGTH], self.gene[i][c_pos:self.G_LENGTH]

    def two_crossover(self):
        """
        二点交叉
        交叉位置を1〜G_LENGTH-1の範囲でランダムに2つ決め、その間を入れ替える

        :return: None
        """

        c_pos1 = random.randint(1, self.G_LENGTH - 1)
        c_pos2 = random.randint(1, self.G_LENGTH - 1)

        if c_pos2 < c_pos1:
            c_pos1, c_pos2 = c_pos2, c_pos1
        for i in range(1, self.POP_SIZE, 2):
            self.gene[i][c_pos1:c_pos2], self.gene[i + 1][c_pos1: c_pos2] = \
                self.gene[i + 1][c_pos1: c_pos2], self.gene[i][c_pos1: c_pos2]

    def mutation(self):
        """
        突然変異
        0〜1の乱数を発生させ、その値が M_RATE 以下ならば
        遺伝子の値をランダムに変える (0ならば1、1ならば0)

        :return: None
        """

        for i in range(self.POP_SIZE):
            for j in range(self.G_LENGTH):
                if random.random() <= self.M_RATE:
                    if self.gene[i][j] == 1:
                        self.gene[i][j] = 0
                    elif self.gene[i][j] == 0:
                        self.gene[i][j] = 1


def main(arg):
    """
    メインプログラム

    :param arg: 遺伝子設定を取得。なければGAのデフォルト設定を使う
    :return: None
    """

    if len(arg) == 5:
        ga = GA(args[1], args[2], args[3], args[4])
    else:
        ga = GA()

    print("個体数　　　: {0}".format(ga.POP_SIZE))
    print("遺伝子長　　: {0}".format(ga.G_LENGTH))
    print("突然変異率　: {0}".format(ga.M_RATE))

    ga = GA()                                   # クラス初期化
    print("<< 初期個体群 >>")
    print(ga.gene)                              # 初期化遺伝子の表示

    ga.show_gene()                              # 遺伝子の表示

    for t in range(ga.MAX_GEN):
        ga.t = t                                # 世代数
        print("<< 世代数 {0} >>".format(t))
        ga.elite()                              # エリート保存
        ga.reproduction()                       # ルーレット選択
        ga.crossover()                          # 単純交叉
        ga.two_crossover()                      # 二点交叉
        ga.mutation()                           # 突然変異
        ga.fitness = ga.calc_fitness(ga.gene)   # 適応度の計算
        ga.show_gene()                          # 遺伝子の表示

    ga.file.close()                             # ファイルクローズ


if __name__ == "__main__":
    args = sys.argv
    main(args)
