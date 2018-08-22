import random, sys


class GA:
    def __init__(self, pop_size=5, g_length=10, max_gen=20, m_rate=0.1):
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
        population = []
        for i in range(pop_size):
            population.append([random.randint(0, 1) for _ in range(g_length)])
        return population

    @staticmethod
    def calc_fitness(gene):
        fitness = []
        for p in gene:
            count_bit = 0
            count_bit += p[0:5].count(0)
            count_bit += p[5:10].count(1)
            fitness.append(count_bit)
        return fitness

    def show_gene(self):
        ave_fit = sum(self.fitness) / self.POP_SIZE
        max_fit = max(self.fitness)

        for g, f in zip(self.gene, self.fitness):
            print('個体 {0} , 適応度 {1}'.format(g, f))

        print('平均適応度 : {}'.format(max_fit))
        print('最大適応度 : {}'.format(ave_fit))

        self.file.write('{} {} {}'.format(self.t, ave_fit, max_fit))

    def __swap_gene(self, p1, p2):
        self.gene[p1][:], self.gene[p2][:] = self.gene[p2][:], self.gene[p1][:]
        self.fitness[p1], self.fitness[p2] = self.fitness[p2], self.fitness[p1]

    def __copy_gene(self, p1, p2):
        self.gene[p2][:] = self.gene[p1][:]
        self.fitness[p2] = self.fitness[p1]

    def elite(self):
        max_p = self.fitness.index(max(self.fitness))
        min_p = self.fitness.index(min(self.fitness))
        self.__copy_gene(max_p, min_p)
        self.__swap_gene(0, max_p)

    def reproduction(self):
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
        c_pos = random.randint(1, self.G_LENGTH - 1)
        for i in range(1, self.POP_SIZE, 2):
            self.gene[i][c_pos:self.G_LENGTH], self.gene[i + 1][c_pos:self.G_LENGTH] = \
                self.gene[i + 1][c_pos:self.G_LENGTH], self.gene[i][c_pos:self.G_LENGTH]

    def two_crossover(self):
        c_pos1 = random.randint(1, self.G_LENGTH - 1)
        c_pos2 = random.randint(1, self.G_LENGTH - 1)

        if c_pos2 < c_pos1:
            c_pos1, c_pos2 = c_pos2, c_pos1
        for i in range(1, self.POP_SIZE, 2):
            self.gene[i][c_pos1:c_pos2], self.gene[i + 1][c_pos1: c_pos2] = \
                self.gene[i + 1][c_pos1: c_pos2], self.gene[i][c_pos1: c_pos2]

    def mutation(self):
        for i in range(self.POP_SIZE):
            for j in range(self.G_LENGTH):
                if random.random() <= self.M_RATE:
                    if self.gene[i][j] == 1:
                        self.gene[i][j] = 0
                    elif self.gene[i][j] == 0:
                        self.gene[i][j] = 1

    def __del__(self):
        self.file.close()


def main(arg):
    if len(arg) == 5:
        ga = GA(args[1], args[2], args[3], args[4])
    else:
        ga = GA()

    print("個体数　　　: {0}".format(ga.POP_SIZE))
    print("遺伝子長　　: {0}".format(ga.G_LENGTH))
    print("突然変異率　: {0}".format(ga.M_RATE))

    ga = GA()   # 初期化
    print("<< 初期個体群 >>")
    print(ga.gene)  # 初期化遺伝子の表示

    ga.show_gene()  # 遺伝子の表示

    for t in range(ga.MAX_GEN):
        ga.t = t
        print("<< 世代数 {0} >>".format(t))
        ga.elite()
        ga.reproduction()
        ga.crossover()
        ga.mutation()
        ga.fitness = ga.calc_fitness(ga.gene)
        ga.show_gene()

    del ga


if __name__ == "__main__":
    args = sys.argv
    main(args)
