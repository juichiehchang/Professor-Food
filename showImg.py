def show_image(path, crashed, res_list):
    import pygame
    import glob
    from time import sleep
    from speech.speechRecognizer import listener
    listen = listener()
    image = glob.glob(path+'*')

    pygame.init()

    display_width = 1380
    display_height = 800

    white = (255,255,255)
    black = (0,0,0)
    font = pygame.font.Font('/System/Library/Fonts/PingFang.ttc',13)

    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A bit Racey')

    
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        gameDisplay.fill(white)

        for i in range(9):
            x = 280 * (i%5)
            y = 100 + int(i/5) * 400
            text = font.render(res_list[i].text, True, black, white)
            textRect = text.get_rect()
            textRect.center = (130 + (i%5) * 280, 80 + int(i/5) * 400)
            img = pygame.image.load(image[i])
            gameDisplay.blit(text, textRect)
            gameDisplay.blit(pygame.transform.scale(img,(260,200)), (x, y))

        

        pygame.display.update()
        choice = listen.recognize()
        crashed = True

    pygame.quit()


    return choice

def show_text():
    
