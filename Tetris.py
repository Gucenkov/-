import pygame
import random

# Инициализация Pygame
pygame.font.init()

# Размеры игрового окна
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30

# Определения цветов
COLORS = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (75, 0, 130), (238, 130, 238)
]

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]

# Класс блока
class Piece:
    rows = 20
    cols = 10

    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS[1:])
        self.x = 3
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Игровое поле
class Game:
    def __init__(self):
        self.board = [[0] * Piece.cols for _ in range(Piece.rows)]
        self.current_piece = Piece()
        self.score = 0
        self.level = 1
        self.speed = 500  # Начальная скорость в миллисекундах
        self.fast = True

    def collide(self):
        for i, row in enumerate(self.current_piece.shape):
            for j, val in enumerate(row):
                if val and (self.current_piece.y + i >= Piece.rows or
                             self.current_piece.x + j < 0 or
                             self.current_piece.x + j >= Piece.cols or
                             self.board[self.current_piece.y + i][self.current_piece.x + j]):
                    return True
        return False

    def merge(self):
        for i, row in enumerate(self.current_piece.shape):
            for j, val in enumerate(row):
                if val:
                    self.board[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

    def clear_lines(self):
        cleared_lines = 0
        for i in range(Piece.rows - 1, -1, -1):
            if all(self.board[i]):
                cleared_lines += 1
                del self.board[i]
                self.board.insert(0, [0] * Piece.cols)
        self.score += cleared_lines * 100  # 100 очков за каждую линию
        if cleared_lines > 0:
            self.level = self.score // 1000 + 1
            self.speed = max(100, 500 - (self.level - 1) * 50)  # Увеличение скорости

# Основная функция
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    running = True
    fall_time = 0

    while running:
        win.fill((0, 0, 0))
        fall_time += clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.current_piece.x -= 1
                    if game.collide():
                        game.current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    game.current_piece.x += 1
                    if game.collide():
                        game.current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    game.current_piece.y += 1
                if event.key == pygame.K_UP:
                    game.current_piece.rotate()
                    if game.collide():
                        game.current_piece.rotate()  # Возврат, если ротация не возможна

        # Физика игры
        if fall_time >= game.speed:
            game.current_piece.y += 1
            if game.collide():
                game.current_piece.y -= 1
                game.merge()
                game.clear_lines()
                game.current_piece = Piece()
                if game.collide():
                    print("Game Over")
                    running = False
            fall_time = 0

        # Отрисовка
        for i in range(Piece.rows):
            for j in range(Piece.cols):
                if game.board[i][j]:
                    pygame.draw.rect(win, game.board[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for i, row in enumerate(game.current_piece.shape):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(win, game.current_piece.color,
                                     ((game.current_piece.x + j) * BLOCK_SIZE,
                                      (game.current_piece.y + i) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

        # Отображение очков и уровня
        font = pygame.font.SysFont('Arial', 20)
        score_text = font.render(f'Score: {game.score}', True, (255, 255, 255))
        level_text = font.render(f'Level: {game.level}', True, (255, 255, 255))
        win.blit(score_text, (5, 5))
        win.blit(level_text, (5, 30))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
