import random as rand
import pygame
import time

pygame.init()
res = (800, 850)
screen = pygame.display.set_mode(res)
pygame.display.set_caption('Minesweeper')

width = screen.get_width()
height = screen.get_height()
topoffset = 50
firstclick = True
gameover = False
timer = False
initial_mines = True
gamewon = False
font = pygame.font.SysFont(None, 48)

#Change for different grid/mine-count
rows = 16
columns = 30
mines = 99

leftover_mines = mines
boxes = rows * columns
total = boxes-mines
box_width = round((width - 30) / columns)
box_height = round((height - 75) / rows)
if box_height <= box_width:
   box_width = box_height

field = []
uncovered = []
uncovered0s = []

light_grey = (197, 199, 196)
dark_grey = (105,105,105)
lighter_grey = (211,211,211)
black = (0, 0, 0)

display_surface = pygame.display.set_mode((width, height))
image1 = pygame.image.load(r'assets\minesweeper\1.png')
image2 = pygame.image.load(r'assets\minesweeper\2.png')
image3 = pygame.image.load(r'assets\minesweeper\3.png')
image4 = pygame.image.load(r'assets\minesweeper\4.png')
image5 = pygame.image.load(r'assets\minesweeper\5.png')
image6 = pygame.image.load(r'assets\minesweeper\6.png')
image7 = pygame.image.load(r'assets\minesweeper\7.png')
image8 = pygame.image.load(r'assets\minesweeper\8.png')
image0 = pygame.image.load(r'assets\minesweeper\0.png')
imagefacingdown = pygame.image.load(r'assets\minesweeper\facingDown.png')
imagebomb = pygame.image.load(r'assets\minesweeper\bomb.png')
imageflagged = pygame.image.load(r'assets\minesweeper\flagged.png')
imagered = pygame.image.load(r'assets\minesweeper\red.png')
imagegameover = pygame.image.load(r'assets\minesweeper\gameover.png')
imagereset = pygame.image.load(r'assets\minesweeper\reset.png')
image1 = pygame.transform.scale(image1, (box_width, box_width))
image2 = pygame.transform.scale(image2, (box_width, box_width))
image3 = pygame.transform.scale(image3, (box_width, box_width))
image4 = pygame.transform.scale(image4, (box_width, box_width))
image5 = pygame.transform.scale(image5, (box_width, box_width))
image6 = pygame.transform.scale(image6, (box_width, box_width))
image7 = pygame.transform.scale(image7, (box_width, box_width))
image8 = pygame.transform.scale(image8, (box_width, box_width))
image0 = pygame.transform.scale(image0, (box_width, box_width))
imagefacingdown = pygame.transform.scale(imagefacingdown, (box_width, box_width))
imagebomb = pygame.transform.scale(imagebomb, (box_width, box_width))
imageflagged = pygame.transform.scale(imageflagged, (box_width, box_width))
imagered = pygame.transform.scale(imagered, (box_width, box_width))
imagegameover = pygame.transform.scale(imagegameover, (100, 100))
imagereset = pygame.transform.scale(imagereset, (80, 40))
def draw_board():
   global font
   j = 1
   h = 0
   box_width = round((width - 30) / columns)
   box_height = round((height - 75) / rows)
   if box_height <= box_width:
       box_width = box_height
   display_surface.fill(light_grey)
   pygame.draw.rect(screen, dark_grey,pygame.Rect(690, 5, 80, 40))
   pygame.draw.rect(screen, lighter_grey, pygame.Rect(693, 8, 74, 34))
   pygame.draw.rect(screen, dark_grey,pygame.Rect(20, 5, 80, 40))
   pygame.draw.rect(screen, lighter_grey, pygame.Rect(23, 8, 74, 34))
   timer_text = font.render('000', True, black)
   mine_text = font.render('000', True, black)
   display_surface.blit(timer_text, (700, 8))
   display_surface.blit(mine_text, (30, 8))
   font = pygame.font.SysFont(None, 24)
   reset_text = font.render('reset', True, black)
   display_surface.blit(imagereset, (595, 5))
   display_surface.blit(reset_text, (615, 18))
   font = pygame.font.SysFont(None, 48)
   for i in range(boxes):
       xpos = (j-1)*box_width+10
       ypos = h*box_width+topoffset
       field[i].left = xpos
       field[i].right = xpos + box_width
       field[i].top = ypos
       field[i].bottom = ypos + box_width
       display_surface.blit(imagefacingdown, (xpos, ypos))
       if j % columns == 0:
           h += 1
           j = 1
       else:
           j += 1
def buildgrid():
   for i in range(boxes):
       f = convertfromi(i)
       class box:
           c = 0
           x = f[0]
           y = f[1]
           left = 0
           right = 0
           top = 0
           bottom = 0
           clicked = False
           flagged = False
       field.append(box)
def converttoi(x, y):
   i = (y - 1) * columns + x - 1
   return i
def convertfromi(i):
   xy = [1, 1]
   while i >= columns:
       i -= columns
       xy[1] += 1
   while i > 0:
       i -= 1
       xy[0] += 1
   return xy
def checkfor0s(i):
   g = convertfromi(i)
   for i in range(9):
       if not (i > 2):
           x2 = g[0] - 1 + i
           y2 = g[1]
           if not (x2 < 1 or x2 > columns):
               j = converttoi(x2, y2)
               if not j in uncovered:
                   uncovered.append(j)
               if field[j].c == 0:
                   field[j].c = '_'
                   uncovered0s.append(j)
       elif not (i > 5):
           x2 = g[0] - 4 + i
           y2 = g[1] - 1
           if not ((x2 < 1 or x2 > columns) or (y2 < 1 or y2 > rows)):
               j = converttoi(x2, y2)
               if not j in uncovered:
                   uncovered.append(j)
               if (field[j].c == 0):
                   field[j].c = '_'
                   uncovered0s.append(j)
       else:
           x2 = g[0] - 7 + i
           y2 = g[1] + 1
           if not ((x2 < 1 or x2 > columns) or (y2 < 1 or y2 > rows)):
               j = converttoi(x2, y2)
               if not j in uncovered:
                   uncovered.append(j)
               if field[j].c == 0:
                   field[j].c = '_'
                   uncovered0s.append(j)
def checkuncovered():
   for j in uncovered0s:
       checkfor0s(j)
def generate_field():
   b = 0
   while b < mines:
       x = rand.randint(0, boxes - 1)
       if field[x].c == 0:
           field[x].c = 'x'
           b += 1
def printfield():
   for i in range(boxes):
       if (i + 1) % columns == 0:
           print(field[i].c)
       else:
           print(field[i].c, end=' ')
def generate_values():
   n = 0
   for i in range(boxes):
       if field[i].c == 0 or field[i].c == "U":
           f = (convertfromi(i))
           for j in range(9):
               if not (j > 2):
                   x2 = f[0] - 1 + j
                   y2 = f[1]
                   if not (x2 < 1 or x2 > columns):
                       j = converttoi(x2, y2)
                       if field[j].c == 'x':
                           n += 1
               elif not (j > 5):
                   x2 = f[0] - 4 + j
                   y2 = f[1] - 1
                   if not ((x2 < 1 or x2 > columns) or (y2 < 1 or y2 > rows)):
                       j = converttoi(x2, y2)
                       if field[j].c == 'x':
                           n += 1
               else:
                   x2 = f[0] - 7 + j
                   y2 = f[1] + 1
                   if not ((x2 < 1 or x2 > columns) or (y2 < 1 or y2 > rows)):
                       j = converttoi(x2, y2)
                       if field[j].c == 'x':
                           n += 1
           field[i].c = n
           n = 0
def update_field():
   global total, initial_mines
   for i in uncovered:
       xpos = field[i].left
       ypos = field[i].top
       if field[i].c == 1:
           display_surface.blit(image1, (xpos, ypos))
       elif field[i].c == 2:
           display_surface.blit(image2, (xpos, ypos))
       elif field[i].c == '_':
           display_surface.blit(image0, (xpos, ypos))
       elif field[i].c == 0:
           display_surface.blit(image0, (xpos, ypos))
       elif field[i].c == 3:
           display_surface.blit(image3, (xpos, ypos))
       elif field[i].c == 4:
           display_surface.blit(image4, (xpos, ypos))
       elif field[i].c == 5:
           display_surface.blit(image5, (xpos, ypos))
       elif field[i].c == 6:
           display_surface.blit(image6, (xpos, ypos))
       elif field[i].c == 7:
           display_surface.blit(image7, (xpos, ypos))
       elif field[i].c == 8:
           display_surface.blit(image8, (xpos, ypos))
       field[i].clicked = True
def update_mines():
   pygame.draw.rect(screen, lighter_grey, pygame.Rect(23, 8, 74, 34))
   if leftover_mines < 10:
       mine_text = font.render('0' + '0' + str(leftover_mines), True, black)
   if leftover_mines < 100:
       mine_text = font.render('0' + str(leftover_mines), True, black)
   else:
       mine_text = font.render(str(leftover_mines), True, black)
   display_surface.blit(mine_text, (30, 8))
def check_total():
   totaluncovered = 0
   for i in(uncovered):
       totaluncovered += 1
   if totaluncovered == total:
       game_won()
def game_won():
   global gamewon, timer, leftover_mines
   gamewon = True
   timer = False
   win_text = font.render('You won!', True, black)
   display_surface.blit(win_text, (width/2-70, 8))
   for i in range(boxes):
       if field[i].c == 'x':
           if not field[i].flagged:
               xpos = field[i].left
               ypos = field[i].top
               display_surface.blit(imageflagged, (xpos, ypos))
               field[i].flagged = True
               leftover_mines -= 1
               update_mines()
def first_click(x, y):
   global start_time, timer, initial_mines
   for i in range(9):
       if not (i > 2):
           x2 = int(x) - 1 + i
           y2 = int(y)
           if not (x2 < 1 or x2 > columns):
               j = converttoi(x2, y2)
               field[j].c = "U"
       elif not (i > 5):
           x2 = int(x) - 4 + i
           y2 = int(y) - 1
           if not ((x2 < 1 or x2 > columns) or (y2 < 1 or y2 > rows)):
               j = converttoi(x2, y2)
               field[j].c = "U"
       else:
           x2 = int(x) - 7 + i
           y2 = int(y) + 1
           if not ((x2 < 1 or x2 > columns) or (y2 < 1 or y2 > rows)):
               j = converttoi(x2, y2)
               field[j].c = "U"
   j = converttoi(int(x), int(y))
   field[j].c = "_"
   uncovered0s.append(j)
   uncovered.append(j)
   generate_field()
   generate_values()
   checkuncovered()
   for i in uncovered:
       update_field()
   update_mines()
   start_time =time.time()
   timer = True
   initial_mines = False
   check_total()
def game_over():
    global gameover, timer
    for box in field:
       if box.c =='x':
           xpos = box.left
           ypos = box.top
           display_surface.blit(image0, (xpos, ypos))
           display_surface.blit(imagebomb, (xpos, ypos))
    timer = False
    gameover = True
    display_surface.blit(imagegameover, (width/2-50, -25))
def reset():
   global firstclick, gameover, timer, initial_mines, gamewon, total, leftover_mines, field, uncovered, uncovered0s
   firstclick = True
   gameover = False
   timer = False
   initial_mines = True
   gamewon = False
   total = boxes - mines
   leftover_mines = mines
   field = []
   uncovered = []
   uncovered0s = []
   buildgrid()
   draw_board()

buildgrid()
draw_board()
while True:
   if timer:
       elapsed_time = int(time.time() - start_time)
       pygame.draw.rect(screen, lighter_grey, pygame.Rect(693, 8, 74, 34))
       if elapsed_time<10:
           timer_text = font.render('0' + '0' + str(elapsed_time), True, black)
           display_surface.blit(timer_text, (700, 8))
       elif elapsed_time<100:
           timer_text = font.render('0' + str(elapsed_time), True, black)
           display_surface.blit(timer_text, (700, 8))
       elif elapsed_time <1000:
           timer_text = font.render(str(elapsed_time), True, black)
           display_surface.blit(timer_text, (700, 8))
       else: timer = False
   pygame.display.update()
   for ev in pygame.event.get():
       if ev.type == pygame.QUIT:
           pygame.quit()
       if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame:
           mouse = pygame.mouse.get_pos()
           print(mouse)
           if mouse[0]>10:
               if mouse[0]<(box_width*columns+10):
                   if mouse[1] > 50:
                       if mouse[1] < (box_width*rows+50):
                           for i in range(boxes):
                               if mouse[0] < field[i].right:
                                   if mouse[0] > field[i].left:
                                       if mouse[1] < field[i].bottom:
                                           if mouse[1] > field[i].top:
                                               x = field[i].x
                                               y = field[i].y
                                               ypos = field[i].top
                                               xpos = field[i].left
                                               if firstclick:
                                                   if ev.button == 1:
                                                       first_click(x, y)
                                                       firstclick = False
                                               else:
                                                   if not gameover:
                                                       if not gamewon:
                                                           if not field[i].clicked:
                                                               if not field[i].flagged:
                                                                   if ev.button == 1:
                                                                       if field[i].c == 'x':
                                                                           field[i].c = 'l'
                                                                           display_surface.blit(imagered, (xpos, ypos))
                                                                           display_surface.blit(imagebomb, (xpos, ypos))
                                                                           game_over()
                                                                       else:
                                                                           uncovered.append(i)
                                                                           if field[i].c==0:
                                                                               uncovered0s.append(i)
                                                                               for j in uncovered0s:
                                                                                   checkfor0s(j)
                                                                           update_field()
                                                                           check_total()
                                                                           field[i].clicked = True
                                                               if ev.button == 3:
                                                                   if not field[i].clicked:
                                                                       if not field[i].flagged:
                                                                               display_surface.blit(imageflagged, (xpos, ypos))
                                                                               field[i].flagged = True
                                                                               leftover_mines -= 1
                                                                               update_mines()
                                                                       else:
                                                                           display_surface.blit(imagefacingdown, (xpos, ypos))
                                                                           field[i].flagged = False
                                                                           leftover_mines += 1
                                                                           update_mines()
                   elif mouse[0] < 672:
                       if mouse[0] > 598:
                           if mouse[1] > 8:
                               if mouse[1] < 42:
                                   if ev.button == 1:
                                       reset()

