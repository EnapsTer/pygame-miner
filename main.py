# здесь подключаются модули
import pygame

from minerobj import *
import settings

pygame.init()


sc = pygame.display.set_mode((settings.DIS_WIDTH, settings.DIS_HEIGHT))
clock = pygame.time.Clock()
marked_bombs = 0
text = ''


font = pygame.font.SysFont('serif', settings.DIS_WIDTH//8)
cell_font = pygame.font.SysFont('serif', Cell.cell_width//2)
pygame.display.update()
pygame.display.set_caption("Miner")
field = Field()
field.create_empty_field(sc, WHITE)


first_play = True
game_active = True

#main loop
while game_active:

    clock.tick(settings.FPS)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:

                #cell opening loop
                for i in range(settings.CELLS):
                    for j in range(settings.CELLS):
                        #checks for pressing
                        if field.cells[i][j].collide(event.pos):
                            if first_play:
                                first_play = False
                                field.create_field(sc, settings.WHITE, i, j)
                            field.cells[i][j].active()
                            zero_indexes = set()
                            #recursive opening of null cells
                            def open_ceil(i, j):
                                if field.cells[i][j].value == 0:
                                    field.cells[i][j].active()
                                    zero_indexes.add((i, j))
                                    for item in field.cells[i][j].neighbor:
                                        if item[0] >= 0 and item[0] < CELLS and item[1] >= 0 and item[1] < settings.CELLS:
                                            if (item[0], item[1]) not in zero_indexes:
                                                field.cells[item[0]][item[1]].active()
                                    for x in [-1, 0, 1]:
                                        for y in [-1, 0, 1]:
                                            if (x + i >= 0 and x + i < CELLS) and (y + j >= 0 and y + j < settings.CELLS) and (
                                            i + x, j + y) not in zero_indexes:
                                                open_ceil(i + x, j + y)
                                else:
                                    return 1


                            open_ceil(i, j)
                            #Lose event
                            if field.cells[i][j].value == '*':
                                game_active = False
                                text = 'YOU LOSE'


            elif event.button == 3:
                #cell labeling loop
                for i in range(CELLS):
                    for j in range(CELLS):
                        if field.cells[i][j].collide(event.pos):
                            field.cells[i][j].active_flag()
                            if field.cells[i][j].value =='*' and field.cells[i][j].flag:
                                marked_bombs+= 1
                            elif field.cells[i][j].value =='*' and not field.cells[i][j].flag:
                                marked_bombs -= 1
                #win event
                if (marked_bombs == settings.BOMBS):
                    game_active = False
                    text = 'YOU WON!'


    #pygame draw loop
    for i in range(settings.CELLS):
        for j in range(settings.CELLS):
            rect, cell_text = field.cells[i][j].get()
            pygame.draw.rect(rect[0], (rect[1][0], rect[1][1], rect[1][2]), (rect[2][0], rect[2][1], rect[2][2], rect[2][3]))
            rect[0].blit(cell_font.render(str(cell_text[0]),1, (0,0,255)), (cell_text[1][0], cell_text[1][1]))


    pygame.display.update()
else:
    #end game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        game_end = font.render(text, 1, (255, 255, 255))
        sc.fill((0, 0, 0))
        sc.blit(game_end, (settings.DIS_WIDTH // 5, settings.DIS_HEIGHT // 2.5))
        pygame.display.update()