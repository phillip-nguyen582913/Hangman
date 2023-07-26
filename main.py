import pygame
import math
import random

# set up display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN LAUNCHER")

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 50)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

def text_objects(text, font):
  textSurface = font.render(text, True, BLACK)
  return textSurface, textSurface.get_rect()

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# game variables
hangman_status = 0
words = ["HEATS", "SUNS", "CELTICS", "WARRIORS", "ROCKETS", "MAGICS", "CAVALIERS", "BUCKS", "LAKERS", "GRIZZLIES",
         "KNICKS", "MAVERICKS", "NETS", "JAZZ", "BULLS", "HEATS", "RAPTORS", "SPURS", "TIMBERWOLVES", "CLIPPERS",
         "PISTONS", "PELICANS", "HORNETS", "KINGS", "HAWKS", "BLAZERS", "THUNDERS", "PACERS", "NUGGETS", "WIZARDS"]
word = random.choice(words)
guessed = []

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up game loop here
FPS = 60
clock = pygame.time.Clock()
run = True

def draw():
    win.fill(WHITE)
    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    
  
    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    global hangman_status
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(400)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

def reset_game():
  global hangman_status
  global word
  global guessed 
  global letters
  global i
  global x
  global y
  hangman_status = 0
  word = random.choice(words)
  guessed = []
  letters = []
  for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])
  
def quit():
  pygame.quit()
  
def end_game():
  RADIUS = 40
  end = True
  global run
  while end:
    win.fill(WHITE)
    text = TITLE_FONT.render("Do you want to play again?", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))
    
    pygame.draw.circle(win, BLACK, (600, 320), RADIUS, 3)
    text = LETTER_FONT.render("No", 1, BLACK)
    win.blit(text, (600 - text.get_width() / 2, 320 - text.get_height() / 2))

    pygame.draw.circle(win, BLACK, (200, 320), RADIUS, 3)
    text = LETTER_FONT.render("Yes", 1, BLACK)
    win.blit(text, (200 - text.get_width() / 2, 320 - text.get_height() / 2))

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                disno = math.sqrt((600 - m_x) ** 2 + (320 - m_y) ** 2)
                if disno < RADIUS:
                  run = False 
                  quit()
                  return
                disyes = math.sqrt((200 - m_x) ** 2 + (320 - m_y) ** 2)
                if disyes < RADIUS:
                  run = True
                  reset_game()
                  return
    pygame.display.update()
    clock.tick(15)
    
def main():
    FPS = 60
    clock = pygame.time.Clock()
    global run
    run = True
    global hangman_status
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                              hangman_status += 1
                              
        draw()
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
        if won:
            display_message("You WON!")
            pygame.time.delay(1000)
            end_game()
        elif hangman_status == 6:
            display_message("You LOST!")
            pygame.time.delay(1000)
            end_game()
          
main()
pygame.quit()