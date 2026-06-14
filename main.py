import sys
import pygame
from screens import MenuScreen

W, H = 1024, 768
FPS  = 60
TITLE = "Flag Quiz"


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    current = MenuScreen()

    while True:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            current.handle_event(event)

        current.update(dt)
        current.draw(screen)
        pygame.display.flip()

        nxt = current.next_screen()
        if nxt is not None:
            current = nxt


if __name__ == "__main__":
    main()
