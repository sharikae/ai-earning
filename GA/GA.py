import random

POP_SIZE = 5
G_LENGTH = 10
MAX_GEN = 20
M_RATE = 0.1


def init_gene():
    population = []

    for i in range(POP_SIZE):
        population.append([random.randint(0, 1) for j in range(G_LENGTH)])
    return population


def calc_fitness(pop):
    fitness = []

    for p in pop:
        count_bit = 0
        count_bit += p[0:5].count(0)
        count_bit += p[5:10].count(1)
        fitness.append(count_bit)
    return fitness


class GA:
    def __init__(self):
        self.gene = init_gene()
        self.fitness = calc_fitness(self.gene)
        self.file = open('result.dat', 'w')
        self.t = 0

    def show_gene(self):
        ave_fit = sum(self.fitness) / POP_SIZE
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
        new_gene = [[0 for _ in range(G_LENGTH)] for _ in range(POP_SIZE)]

        for p in range(1, POP_SIZE):
            r = sum_of_fitness * random.random()
            num = 0
            border = self.fitness[0]

            while border < r:
                num += 1
                border += self.fitness[num]

            for i in range(G_LENGTH):
                new_gene[p][i] = self.gene[num][i]

        for p in range(1, POP_SIZE):
            for i in range(G_LENGTH):
                self.gene[p][i] = new_gene[p][i]

    def crossover(self):
        c_pos = random.randint(1, G_LENGTH - 1)
        for i in range(1, POP_SIZE, 2):
            self.gene[i][c_pos:G_LENGTH], self.gene[i + 1][c_pos:G_LENGTH] = \
                self.gene[i + 1][c_pos:G_LENGTH], self.gene[i][c_pos:G_LENGTH]

    def two_crossover(self):
        c_pos1 = random.randint(1, G_LENGTH - 1)
        c_pos2 = random.randint(1, G_LENGTH - 1)

        if c_pos2 < c_pos1:
            c_pos1, c_pos2 = c_pos2, c_pos1
        for i in range(1, POP_SIZE, 2):
            self.gene[i][c_pos1:c_pos2], self.gene[i + 1][c_pos1: c_pos2] = \
                self.gene[i + 1][c_pos1: c_pos2], self.gene[i][c_pos1: c_pos2]

    def mutation(self):
        for i in range(POP_SIZE):
            for j in range(G_LENGTH):
                if random.random() <= M_RATE:
                    if self.gene[i][j] == 1:
                        self.gene[i][j] = 0
                    elif self.gene[i][j] == 0:
                        self.gene[i][j] = 1

    def __del__(self):
        self.file.close()


def main():
    print("個体数　　　: {0}".format(POP_SIZE))
    print("遺伝子長　　: {0}".format(G_LENGTH))
    print("突然変異率　: {0}".format(M_RATE))

    ga = GA()   # 初期化
    print("<< 初期個体群 >>")
    print(ga.gene)  # 初期化遺伝子の表示

    ga.show_gene()  # 遺伝子の表示

    for t in range(MAX_GEN):
        ga.t = t
        print("<< 世代数 {0} >>".format(t))
        ga.elite()
        ga.reproduction()
        ga.crossover()
        ga.mutation()
        ga.fitness = calc_fitness(ga.gene)
        ga.show_gene()

    del ga


if __name__ == "__main__":
    main()
