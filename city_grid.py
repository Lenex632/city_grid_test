from random import randint


class CityGrid:
    def __init__(self, N: int, M: int, R: int, obstructed: float):
        self.N = N
        self.M = M
        self.R = R
        self.obstructed = obstructed

        self.grid = []
        self.towers = []

        self.make_grid()
        for i in range(self.M):
            print(self.grid[i])
        print()

        self.place_towers()
        for i in range(self.M):
            print(self.grid[i])

    def make_grid(self):
        blocks = ['F' for _ in range(self.M * self.N)]

        need_to_obstruct = round(self.M * self.N * self.obstructed / 100)
        obstructed_blocks = []
        for _ in range(need_to_obstruct):
            choose = -1
            while choose in obstructed_blocks or choose == -1:
                choose = randint(0, self.M * self.N - 1)
            obstructed_blocks.append(choose)
            blocks[choose] = 'O'

        # blocks = ['F', 'F', 'O', 'O', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'O', 'O', 'F', 'O', 'F', 'F', 'O', 'O', 'O', 'F', 'F', 'O', 'F', 'F', 'F', 'F']
        # blocks = ['C', 'C', 'O', 'O', 'C', 'C', 'P', 'C', 'P', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'P', 'O', 'C', 'C', 'O', 'O', 'O', 'P', 'C', 'O', 'P', 'C', 'C', 'C']

        grid = [blocks[i:i+self.N] for i in range(0, len(blocks), self.N)]

        self.grid = grid

    def place_towers(self):
        """
        Мне кажется, что данный алгоритм не идеально оптимизирован и можно было бы и сделать получше, но это то, до чего
        я смог додуматься. Кроме того алгоритм всё же справляется с поставленной задачей с некоторой погрешностью.

        Можно изменить начальные параметры (count_n = 0, count_m = 0) и их подсчёт (count_n = -1, count_m = -1), что бы
        вышки располагались ближе к зонам соседних вышек, создавали перекрытие и имели лучший параметр передачи.
        Однако это значит, что покрытие вышками будет не минимальным, что противоречит Заданию 3, поэтому решил
        остановиться на этом варианте.
        """
        count_m = -1
        flag = False  # что бы не сбрасывать count_m сразу же после размещения одной вышки в строке
        for m in range(self.M):
            count_m += 1
            count_n = -1
            for n in range(self.N):
                count_n += 1
                if (m == self.M - 1 or count_m == self.R) \
                        and (n == self.N - 1 or count_n == self.R) \
                        and self.grid[m][n] == 'F':
                    self.cover_blocks(n, m)
                    self.grid[m][n] = 'P'
                    self.towers.append((n, m))
                    flag = True
                    count_n = -2
            if flag:
                count_m = -2
                flag = False

        self.final_check()

    def cover_blocks(self, n: int, m: int):
        for i in range(max(0, m - self.R), min(self.M, m + self.R + 1)):
            for j in range(max(0, n - self.R), min(self.N, n + self.R + 1)):
                if self.grid[i][j] != 'O':
                    self.grid[i][j] = 'C'

    def final_check(self):
        for m in range(self.M):
            for n in range(self.N):
                if self.grid[m][n] == 'F':
                    self.cover_blocks(n, m)
                    self.grid[m][n] = 'P'
                    self.towers.append((n, m))

    def find_path(self):
        pass

    def visualization(self):
        pass


if __name__ == '__main__':
    columns, rows, range_num, obstructed_num = 5, 6, 1, 30
    city = CityGrid(columns, rows, range_num, obstructed_num)
