import sys
import pygame

TILE_SIZE = 128

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        self.screen = pygame.display.set_mode((TILE_SIZE*3, TILE_SIZE*3))
        self.clock = pygame.time.Clock()
        self.player = 1
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.win_state = False
        self.font = pygame.font.SysFont(None, int(TILE_SIZE / 3))
        self.jumpscare_img = pygame.image.load("./assets/jumpscare.png")
        self.the_real_jumpscare = pygame.image.load("./assets/the_real_jumpscare.png")

    def process_click(self, event):
        mouse_x, mouse_y = event.pos
        x = int(mouse_x / TILE_SIZE)
        y = int(mouse_y / TILE_SIZE)
        idx = y*3 + x%3

        if (self.board[y][x] != 0):
            self.screen.blit(self.jumpscare_img, (0,0))
            pygame.mixer.Sound("./assets/jumpscare.mp3").play()
            pygame.display.update()
            pygame.time.delay(1000)
            return

        self.board[y][x] = self.player

        row_check = True
        col_check = True
        prim_diag_check = True
        sec_diag_check = True
        for cell in range(9):
            if int(cell / 3) - int(idx / 3) == 0:
                if self.board[int(cell / 3)][cell % 3] != self.player:
                    row_check = False
            if abs(idx - cell) % 3 == 0:
                if self.board[int(cell / 3)][cell % 3] != self.player:
                    col_check = False
            if int(cell / 3) == cell % 3:
                if self.board[int(cell / 3)][cell % 3] != self.player:
                    prim_diag_check = False
            if int(cell / 3) + cell%3 == 2:
                if self.board[int(cell / 3)][cell % 3] != self.player:
                    sec_diag_check = False

        if row_check or col_check or prim_diag_check or sec_diag_check:
            pygame.mixer.Sound("./assets/you_win_in_life.mp3").play()
            self.win_state = True
            return

        self.player = (1 + 2) - self.player

    def render_win(self):
        if self.win_state:
            img = pygame.transform.scale(self.the_real_jumpscare, (TILE_SIZE * 3, TILE_SIZE * 3))
            self.screen.blit(img, (0,0))
            # pygame.draw.rect(self.screen, (255,255,255), (0,0,TILE_SIZE*3, TILE_SIZE*3), 0)
            text = self.font.render("Player" + str(self.player) + " WINS!", True, (255,0,0))
            self.screen.blit(text, (TILE_SIZE * 3 / 4, TILE_SIZE * 3 / 2.5))

    def run(self):
        while(True):
            for idx in range(9):
                x = int(idx % 3)
                y = int(idx / 3)
                pygame.draw.rect(self.screen, (0,0,0), (TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE), 0)
                pygame.draw.rect(self.screen, (255,255,255), (TILE_SIZE * x + 1, TILE_SIZE * y + 1, TILE_SIZE-1, TILE_SIZE-1), 0)

                if self.board[y][x] == 1:
                    pygame.draw.aaline(self.screen, (255,0,0), (TILE_SIZE * x + TILE_SIZE / 3, TILE_SIZE * y + TILE_SIZE / 3), (TILE_SIZE * x + 2 * TILE_SIZE / 3, TILE_SIZE * y + 2 * TILE_SIZE / 3), 1)
                    pygame.draw.aaline(self.screen, (255,0,0), (TILE_SIZE * x + TILE_SIZE / 3, TILE_SIZE * y + 2 * TILE_SIZE / 3), (TILE_SIZE * x + 2 * TILE_SIZE / 3, TILE_SIZE * y + TILE_SIZE / 3), 1)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(self.screen, (255,0,0), (TILE_SIZE * x + TILE_SIZE / 2, TILE_SIZE * y + TILE_SIZE / 2), (TILE_SIZE / 4), 1)

            self.render_win()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.win_state:
                    self.process_click(event)

            pygame.display.update()
            self.clock.tick(60)


if __name__=='__main__':
    Game().run()