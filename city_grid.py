from random import sample
import heapq
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class CityGrid:
    def __init__(self, N: int, M: int, R: int, obstructed: float):
        self.N = N
        self.M = M
        self.R = R
        self.obstructed = obstructed

        self.grid = []
        self.towers = []
        self.connections = {}
        self.distances = {}

        self.make_grid()
        for i in range(self.M):
            print(self.grid[i])
        print()

        self.place_towers()
        self.towers.sort(key=lambda t: (t[1], t[0]))
        for i in range(self.M):
            print(self.grid[i])
        print()
        print(self.towers)

        self.find_connections()
        for k, v in self.connections.items():
            print(k, ':', v)
        print()

        for tower in self.towers:
            self.dijkstra(tower)

        for k, v in self.distances.items():
            print(k, ':', v)

    def make_grid(self):
        """
        Создаёт сетку N * M, имитирующую город.
        """
        blocks = [0 for _ in range(self.M * self.N)]

        need_to_obstruct = round(self.M * self.N * self.obstructed / 100)
        obstructed_blocks = sample(range(self.M * self.N), need_to_obstruct)
        for block in obstructed_blocks:
            blocks[block] = 1

        # blocks = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0]
        # blocks = [2, 2, 1, 1, 2, 2, 'P', 2, 'P', 2, 2, 2, 2, 2, 1, 1, 'P', 1, 2, 2, 1, 1, 1, 'P', 2, 1, 'P', 2, 2, 2]
        # blocks = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0]
        # blocks = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        print(blocks, '\n')

        self.grid = [blocks[i:i+self.N] for i in range(0, len(blocks), self.N)]

    def place_towers(self):
        """
        Размещает вышки на сетке в соответствии с Заданием 3.

        Мне кажется, что данный алгоритм не идеально оптимизирован и можно было бы и сделать получше, но это то, до чего
        я смог додуматься. Однако алгоритм всё же справляется с поставленной задачей при небольших данных с
        некоторой погрешностью.

        Можно изменить начальные параметры (count_n = 0, count_m = 0) и их подсчёт (count_n = -1, count_m = -1), что бы
        вышки точно располагались в зонах соседних вышек, создавали перекрытие и имели лучший параметр передачи.
        Однако это значит, что покрытие вышками будет не минимальным, что противоречит Заданию 3, поэтому решил
        остановиться на варианте без однозначных пересечений.
        """
        count_m = -1
        flag = False  # что бы не сбрасывать count_m сразу же после размещения одной вышки в строке
        for m in range(self.M):
            count_m += 1
            count_n = -1
            for n in range(self.N):
                count_n += 1
                if (m == self.M - 1 or count_m == self.R) and (n == self.N - 1 or count_n == self.R):
                    self.place_one_tower(n, m)
                    flag = True
                    count_n = -2
            if flag:
                count_m = -2
                flag = False

        self.final_check()

    def place_one_tower(self, n: int, m: int):
        """
        Поставить на сетку одну вышку с координатами n, m.
        """
        if self.grid[m][n] == 0:
            self.cover_blocks(n, m)
            self.grid[m][n] = 3
            self.towers.append((n, m))

    def cover_blocks(self, n: int, m: int):
        """
        Пометить как "покрытые" все клетки в радиусе R от вышки с координатами n, m.
        """
        for i in range(max(0, m - self.R), min(self.M, m + self.R + 1)):
            for j in range(max(0, n - self.R), min(self.N, n + self.R + 1)):
                if self.grid[i][j] != 1:
                    self.grid[i][j] = 2

    def final_check(self):
        """
        Проверяет, сетку на наличие непокрытых блоков, если находит такие - ставит туда вышку.

        Повторюсь, алгоритм не оптимальный, но какой есть.
        """
        for m in range(self.M):
            for n in range(self.N):
                self.place_one_tower(n, m)

    def find_connections(self):
        """
        Создаёт граф, который отображает связи между вышками.
        """
        for tower in self.towers:
            self.connections[tower] = []
            for other in self.towers:
                if self.is_connected(tower, other):
                    self.connections[tower].append(other)

    def is_connected(self, tower: tuple[int, int], other: tuple[int, int]) -> bool:
        """
        Проверяет есть ли связь между вышками tower и other.
        """
        if tower == other:
            return False
        elif abs(tower[0] - other[0]) > self.R * 2 or abs(tower[1] - other[1]) > self.R * 2:
            return False
        else:
            return True

    def dijkstra(self, start: tuple[int, int]):
        """
        Находит оптимальный путь для вышки start в графе graph.
        """
        distances = {tower: float('infinity') for tower in self.connections}

        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_tower = heapq.heappop(priority_queue)

            if current_distance > distances[current_tower]:
                continue

            for other_tower in self.connections[current_tower]:
                distance = current_distance + 1
                if distance < distances[other_tower]:
                    distances[other_tower] = distance
                    heapq.heappush(priority_queue, (distance, other_tower))

        distances = dict(map(lambda x: (x[0], None if x[1] == float('infinity') or x[1] == 0 else x[1]), distances.items()))
        self.distances[start] = distances
        return distances

    def visualization(self):
        plt.pcolormesh(self.grid, edgecolors='black')
        plt.show()


if __name__ == '__main__':
    columns, rows, range_num, obstructed_num = 10, 10, 2, 30
    city = CityGrid(columns, rows, range_num, obstructed_num)

    city.visualization()
