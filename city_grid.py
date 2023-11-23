from random import randint


class CityGrid:
    def __init__(self, N: int, M: int, R: int, obstructed: float):
        self.N = N
        self.M = M
        self.R = R
        self.obstructed = obstructed
        self.grid = []

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

        blocks = ['F', 'F', 'O', 'O', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'O', 'O', 'F', 'O', 'F', 'F', 'O', 'O', 'O', 'F', 'F', 'O', 'F', 'F', 'F', 'F']
        # blocks = ['C', 'C', 'O', 'O', 'C', 'C', 'P', 'C', 'P', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'P', 'O', 'C', 'C', 'O', 'O', 'O', 'P', 'C', 'O', 'P', 'C', 'C', 'C']
        print(blocks)

        grid = [blocks[i:i+self.N] for i in range(0, len(blocks), self.N)]

        self.grid = grid

    def place_tower(self):
        dp = [['0' for _ in range(self.N + 2)]]
        for i in range(len(self.grid)):
            dp.append(['0'] + self.grid[i] + ['0'])
        dp.append(['0' for _ in range(self.N + 2)])

        for m in range(self.M + 2):
            print(dp[m])
        print('\n')

        # for m in range(self.M):
        #     count = 0
        #     for n in range(self.N):

    def find_path(self):
        pass


if __name__ == '__main__':
    N, M, R, obstructed = 5, 6, 1, 30
    city = CityGrid(N, M, R, obstructed)
    city.make_grid()
    city.place_tower()

    for i in range(M):
        print(city.grid[i])
    print('\n')
