import pygame
import random


from gui import *
from settings import *
from sprites import *


class States:
    share = {}
    def __init__(self):
        self.running = True
        self.next = None

    def setup(self):
        pass
    
    def cleanup(self):
        pass

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class MainMenu(States):
    def __init__(self):
        States.__init__(self)

    def setup(self):
        self.running = True

        self.title = Text("Pong", screen_width // 2, 40, font_size=32)

        self.start_game = Button("Start Game", self.switch_to_game, screen_width // 2 - 50, 100, 100, 20)

    def switch_to_game(self):
        self.next = "game"
        self.running = False

    def cleanup(self):
        del self.title

    def handle_events(self, event):
        self.start_game.check_clicked(event)

    def update(self):
        self.start_game.check_hover()


    def draw(self, screen):
        screen.fill(black)

        self.title.draw(screen)

        self.start_game.draw(screen)

        pygame.display.flip()


class GameOver(States):
    def __init__(self):
        States.__init__(self)

    def setup(self):
        self.running = True

        self.title = Text("Game Over!", screen_width // 2, 40, font_size=48)

    def draw(self, screen):
        screen.fill(black)

        self.title.draw(screen)

        pygame.display.flip()


class Game(States):
    def __init__(self):
        States.__init__(self)

    def setup(self):
        self.running = True
        self.next = "game over"

        self.paddle_1 = Paddle(30, pygame.K_w, pygame.K_s, red)
        self.paddle_2 = Paddle(screen_width - 40, pygame.K_UP, pygame.K_DOWN, blue)
        
        self.paddle_1_score = Text(str(self.paddle_1.score), (screen_width // 2) - 20, screen_height // 2, font_colour=red)
        self.paddle_2_score = Text(str(self.paddle_1.score), (screen_width // 2) + 20, screen_height // 2, font_colour=blue)

        self.paddles = [self.paddle_1, self.paddle_2]

        self.ball = Ball()
        self.ball.dx = random.choice((-5, 5))
        self.ball.dy = random.choice((-5, 5))
        
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.paddle_1)
        self.sprites.add(self.paddle_2)
        self.sprites.add(self.ball)

        self.paddle_hit = False
        self.paddle_hit_count = 0

    def cleanup(self):
        del self.paddle_1, self.paddle_2, self.ball
        del self.sprites, self.paddles
        del self.paddle_1_score, self.paddle_2_score

    def reset_sprites(self):
        self.paddle_hit_count = 0
        self.ball.reset()
        for paddle in self.paddles:
            paddle.reset()

    def update(self):
        self.sprites.update()
    
        for paddle in self.paddles:
            if self.ball.rect.colliderect(paddle.rect):
                self.paddle_hit = True
                if abs(paddle.rect.left - self.ball.rect.right) < collision_tolerance and self.ball.dx > 0:
                    self.ball.dx *= -1
                if abs(paddle.rect.right - self.ball.rect.left) < collision_tolerance and self.ball.dx < 0:
                    self.ball.dx *= -1
                if abs(paddle.rect.top - self.ball.rect.bottom) < collision_tolerance and self.ball.dy > 0:
                    self.ball.dy *= -1
                if abs(paddle.rect.bottom - self.ball.rect.top) < collision_tolerance and self.ball.dy < 0:
                    self.ball.dy *= -1
    
            if not(self.ball.rect.colliderect(paddle.rect)) and self.paddle_hit:
                if (self.paddle_hit_count % 3) == 0:
                    if self.ball.dx > 0:
                        self.ball.dx += random.randint(0, 2)
                    else:
                        self.ball.dx -= random.randint(0, 2)
    
                    if self.ball.dy > 0:
                        self.ball.dy += random.randint(0, 2)
                    else:
                        self.ball.dy -= random.randint(0, 2)
    
                self.paddle_hit = False
                self.paddle_hit_count += 1
    
        if self.ball.rect.x >= screen_width - self.ball.size:
            self.paddle_1.score += 1
            self.paddle_1_score.update_text(str(self.paddle_1.score))
            self.reset_sprites()
            self.ball.dx = -5
            self.ball.dy = random.choice((-5, 5))
    
        if self.ball.rect.x <= 0:
            self.paddle_2.score += 1
            self.paddle_2_score.update_text(str(self.paddle_2.score))
            self.reset_sprites()
            self.ball.dx = 5
            self.ball.dy = random.choice((-5, 5))

        if self.paddle_1.score >= 11 or self.paddle_2.score >= 11:
            States.share["paddle_1_score"] = self.paddle_1.score
            States.share["paddle_2_score"] = self.paddle_2.score

            self.running = False

    def draw(self, screen):
        screen.fill(black)
    
        pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)
        
        self.paddle_1_score.draw(screen)
        self.paddle_2_score.draw(screen)
    
        self.sprites.draw(screen)
    
        pygame.display.flip()


class Control:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_dict = None
        self.current_state = None

    def setup(self, state_dict, start_state):
        self.state_dict = state_dict
        self.current_state = self.state_dict[start_state]
        self.current_state.setup()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.current_state.handle_events(event)

        if not(self.current_state.running):
            self.change_state()

    def change_state(self):
        new_state = self.current_state.next
        self.current_state.cleanup()
        self.current_state = self.state_dict[new_state]
        self.current_state.setup()

    def main_loop(self):
        while self.running:
            self.clock.tick(fps)
            self.handle_events()
            self.current_state.update()
            self.current_state.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    
    state_dict = {
            "mainmenu": MainMenu(),
            "game": Game(),
            "game over": GameOver()
            }
    
    app = Control()
    app.setup(state_dict, "mainmenu")
    app.main_loop()
    
    pygame.quit()
