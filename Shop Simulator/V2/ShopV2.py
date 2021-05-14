import pygame
import sys

pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Shop Sim V2")
run = True
while run == True:
    win.fill((255,255,255))
    button = pygame.Rect(300, 100, 50, 50)
    pygame.draw.rect(win, [255, 0, 0], button)
    font = pygame.font.SysFont("comic sans",15)
    button2 = pygame.Rect(300, 200, 50, 50)
    pygame.draw.rect(win, [255, 0, 0], button2)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button.collidepoint(mouse_pos):
                    pass
            elif button2.collidepoint(mouse_pos):
                    # prints current location of mouse
                    pass
                
   


