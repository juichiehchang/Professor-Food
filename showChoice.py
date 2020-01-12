def show_image(path, crashed, res_list):
    import pygame
    import glob, os
    from time import sleep
    from speech.speechRecognizer import listener
    from speech.speaker import speaker
    from pygame import mixer
    listen = listener()
    say = speaker()
    image = sorted(glob.glob(path+'*'), key = os.path.getmtime)
    print(res_list)
    print(image)
    pygame.init()

    display_width = 1380
    display_height = 800

    white = (255,255,255)
    black = (0,0,0)
    font = pygame.font.Font('/System/Library/Fonts/PingFang.ttc',13)

    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A bit Racey')

    t = 0
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        gameDisplay.fill(white)

        for i in range(10):
            x = 280 * (i%5)
            y = 100 + int(i/5) * 400
            text = font.render(res_list[i], True, black, white)
            textRect = text.get_rect()
            textRect.center = (130 + (i%5) * 280, 80 + int(i/5) * 400)
            img = pygame.image.load(image[i])
            gameDisplay.blit(text, textRect)
            gameDisplay.blit(pygame.transform.scale(img,(260,200)), (x, y))

        if t > 2:
            sentence = "請挑選您想要的餐廳"
            say.speak(sentence)
            
            mixer.music.load('./hintVoice/short.mp3')
            mixer.music.play()
            #choice = listen.recognize()
            choice = input('input restaurant: \n')
            crashed = True
        pygame.display.update()
        t += 1


    pygame.quit()


    return choice

def show_text(crashed, text_lists, pick:str):

    import pygame
    import glob
    from time import sleep
    from speech.speechRecognizer import listener
    from speech.speaker import speaker
    from pygame import mixer
    listen = listener()
    say = speaker()

    pygame.init()

    display_width = 1380
    display_height = 800

    white = (255,255,255)
    black = (0,0,0)
    font = pygame.font.Font('/System/Library/Fonts/PingFang.ttc',20)

    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A bit Racey')

    t = 0 
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        gameDisplay.fill(white)

        for i in range(len(text_lists)):
            x = 280 * (i%5) + 140
            y = 100 + int(i/5) * 200
            text = font.render(text_lists[i], True, black, white)
            textRect = text.get_rect()
            textRect.center = (x, y)
            gameDisplay.blit(text, textRect)

        if t > 2:
            sentence = "請挑選您想要的" + pick
            say.speak(sentence)
            mixer.music.load('./hintVoice/short.mp3')
            mixer.music.play()
            #choice = listen.recognize()
            choice = input('input something: \n')
            crashed = True
        pygame.display.update()
        t += 1

    pygame.quit()


    return choice

def show_need(need):
    
    import pygame
    import glob
    from time import sleep
    from speech.speechRecognizer import listener
    from speech.speaker import speaker
    from pygame import mixer
    listen = listener()
    say = speaker()

    pygame.init()

    display_width = 1380
    display_height = 800

    white = (255,255,255)
    black = (0,0,0)
    font = pygame.font.Font('/System/Library/Fonts/PingFang.ttc',20)

    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('A bit Racey')

    t = 0 
    crashed = False

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        gameDisplay.fill(white)

        for i in range(len(need)):
            x = 400 + 500*i
            y = 400
            text = font.render(need[i], True, black, white)
            textRect = text.get_rect()
            textRect.center = (x, y)
            gameDisplay.blit(text, textRect)

        if t > 2:
            mixer.music.load('./hintVoice/short.mp3')
            mixer.music.play()
            # choice = listen.recognize()
            choice = input('input something: \n')
            crashed = True
        pygame.display.update()
        t += 1

    pygame.quit()


    return choice
#choice = show_need(['需要', '不需要'])

#choice = show_image('./res_img/', False, ["5","6","7","8","9","10","7","8","9","10"])
#show_text(False, ["aaaaaa","2","3","4","5","6","7","8","9","10","11","12"], "餐點")