import math
import numpy as np
import pygame
import sys
import button as b

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (205, 128, 0)

# board size
ROW_COUNT = 15
COL_COUNT = 15

# game variables
EMPTY = 0
BLACK_PIECE = 1
WHITE_PIECE = 2
DUMMY = 3

# screen size
BLOCKSIZE = 50
S_WIDTH = COL_COUNT * BLOCKSIZE
S_HEIGHT = ROW_COUNT * BLOCKSIZE
SCREENSIZE = (S_WIDTH, S_HEIGHT)
RADIUS = 20


class Omok:
    def __init__(self, rows: int, cols: int):
        self.row_count = rows
        self.col_count = cols
        self.board = np.zeros((self.row_count, self.col_count)).astype(int)
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.players = ['Black', 'White']
        self.turn = BLACK_PIECE
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def draw_board(self):
        # fill board with rectangles
        for x in range(0, S_WIDTH, BLOCKSIZE):
            for y in range(0, S_HEIGHT, BLOCKSIZE):
                rect = (x, y, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(self.screen, BROWN, rect)

        # draw vertical grid lines
        for x in range(BLOCKSIZE // 2, S_WIDTH - BLOCKSIZE // 2 + BLOCKSIZE, BLOCKSIZE):
            pygame.draw.line(
                self.screen, BLACK,
                start_pos=(x, BLOCKSIZE // 2),
                end_pos=(x, S_WIDTH - BLOCKSIZE // 2),
                width=2
            )

        # draw horizontal grid lines
        for y in range(BLOCKSIZE // 2, S_HEIGHT - BLOCKSIZE // 2 + BLOCKSIZE, BLOCKSIZE):
            pygame.draw.line(
                self.screen, BLACK,
                start_pos=(BLOCKSIZE // 2, y),
                end_pos=(S_HEIGHT - BLOCKSIZE // 2, y),
                width=2
            )

    def clear_board(self):
        for y, x in np.argwhere(self.board):
            self.board[x][y] = EMPTY
        self.draw_board()

    def drop_piece(self, row: int, col: int, piece: int):
        self.board[row][col] = piece

    def draw_piece(self):
        for y, x in np.argwhere(self.board):
            if self.board[y][x] == BLACK_PIECE:
                pygame.draw.circle(
                    self.screen, BLACK,
                    center=(x * BLOCKSIZE + BLOCKSIZE // 2, y * BLOCKSIZE + BLOCKSIZE // 2),
                    radius=RADIUS
                )

            elif self.board[y][x] == WHITE_PIECE:
                pygame.draw.circle(
                    self.screen, WHITE,
                    center=(x * BLOCKSIZE + BLOCKSIZE // 2, y * BLOCKSIZE + BLOCKSIZE // 2),
                    radius=RADIUS
                )

    def is_valid_loc(self, row: int, col: int) -> bool:
        return self.board[row][col] == EMPTY

    def make_invalid(self):
        self.board = np.where(self.board == EMPTY, DUMMY, DUMMY)

    def horizontal_win(self, piece) -> bool:
        for c in range(self.col_count - 4):
            for r in range(self.row_count):
                if np.all(self.board[r, c:c + 5] == piece):
                    return True

    def vertical_win(self, piece: int) -> bool:
        for c in range(self.col_count):
            for r in range(self.row_count - 4):
                if np.all(self.board[r:r + 5, c] == piece):
                    return True

    def right_diagonal_win(self, piece: int) -> bool:
        for c in range(self.col_count - 4):
            for r in range(4, self.row_count):
                if (
                        self.board[r][c] == piece
                        and self.board[r - 1][c + 1] == piece
                        and self.board[r - 2][c + 2] == piece
                        and self.board[r - 3][c + 3] == piece
                        and self.board[r - 4][c + 4] == piece
                ):
                    return True

    def left_diagonal_win(self, piece: int) -> bool:
        for c in range(self.col_count - 4):
            for r in range(self.row_count - 4):
                if (
                        self.board[r][c] == piece
                        and self.board[r + 1][c + 1] == piece
                        and self.board[r + 2][c + 2] == piece
                        and self.board[r + 3][c + 3] == piece
                        and self.board[r + 4][c + 4] == piece
                ):
                    return True

    def is_won(self, piece: int) -> bool:
        return (
                self.horizontal_win(piece)
                or self.vertical_win(piece)
                or self.right_diagonal_win(piece)
                or self.left_diagonal_win(piece)
        )

    def end_banner(self, player):
        label = self.font.render(f'{player} wins!', True, WHITE, BLACK)
        self.screen.blit(label, (280, 50))

    def restart(self, x, y):
        label = self.font.render('New game', True, WHITE, BLACK)
        return b.Button(x, y, label)

    def _exit(self, x, y):
        label = self.font.render('Exit', True, WHITE, BLACK)
        return b.Button(x, y, label)

    def play(self):
        self.draw_board()
        restart_button = self.restart(230, 650)
        exit_button = self._exit(440, 650)

        while True:
            for event in pygame.event.get():
                x_pos, y_pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col = math.floor(x_pos / BLOCKSIZE)
                    row = math.floor(y_pos / BLOCKSIZE)

                    if self.is_valid_loc(row, col):
                        self.drop_piece(row, col, self.turn)
                        self.draw_piece()

                        if self.is_won(self.turn):
                            name = self.players[0] if self.turn == BLACK_PIECE else self.players[1]
                            self.end_banner(name)
                            self.make_invalid()
                            restart_button.draw(self.screen)
                            exit_button.draw(self.screen)

                        self.turn = 3 - self.turn

            if restart_button.is_clicked():
                self.clear_board()
                self.turn = BLACK_PIECE

            elif exit_button.is_clicked():
                pygame.quit()
                sys.exit()

            pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption('Gomoku')
    Omok(ROW_COUNT, COL_COUNT).play()


if __name__ == '__main__':
    main()
