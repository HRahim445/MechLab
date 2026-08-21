import sys, pygame
from ui_elements import Button
from . import sim_select


pygame.init()
# initialise the pygame module for later use


prefs = open("userprefs.txt", "r")
framerate = int(prefs.readline().strip())
# retrieve saved framerate data


clock = pygame.time.Clock()
# set up clock to tick with framerate


def get_font(size): # function to return desired font data
    return pygame.font.SysFont("Times New Roman", size)


def load():
    global framerate
    SCREEN = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    pygame.display.set_caption("MechLab v1.0.0")
    background = pygame.image.load("images\\main_bg.png")
    background = pygame.transform.scale(background, SCREEN.get_size())
    # set up a borderless fullscreen window and load background
   
    EXIT_BUTTON = Button(
        image=None,
        pos=(960, 608), # x, y center position of button
        text_input="EXIT",
        font=get_font(30),
        base_colour=(255, 255, 255), # white
        hovering_colour=(0, 0, 0) # black
    )
    # instantiate EXIT_BUTTON from Button class
   
    SIMULATIONS_BUTTON = Button(
        image=None,
        pos=(960, 540), # x, y center position of button
        text_input="SIMULATIONS",
        font=get_font(30),
        base_colour=(0, 0, 0), # black
        hovering_colour=(0, 255, 0)  #green
    )
    # instantiate SIMULATIONS_BUTTON from Button class
   
    FRAMERATE_SEL = Button(
        image=None,
        pos=(960, 800), # x, y center position of button
        text_input="Current Framerate: " + str(framerate) + " >>",
        font=get_font(20),
        base_colour=(255,255,255), # white
        hovering_colour=(0, 255, 0) # green
    )
    # instantiate FRAMERATE_SEL from Button class
   
    while True: # main "game loop", iterates once per frame
        SCREEN.blit(background, (0, 0))
        mousePos = pygame.mouse.get_pos() # get mouse position
        for item in [EXIT_BUTTON, SIMULATIONS_BUTTON, FRAMERATE_SEL]:
            item.changeColour(mousePos)
            item.update(SCREEN)
        # update the state of all buttons, change colour if hovering
       
        for event in pygame.event.get(): # loop to check events
            if event.type == pygame.QUIT: # check if the user presses X on the window
                pygame.quit()
                sys.exit()
                # exit the program
               
            if event.type == pygame.MOUSEBUTTONDOWN: # check for mouse button click event
                if EXIT_BUTTON.checkForInput(mousePos):
                    pygame.quit()
                    sys.exit()
                    # exit the program if exit is clicked
                   
                if SIMULATIONS_BUTTON.checkForInput(mousePos):
                    sim_select.load(int(framerate))
                    # load the simulations menu if clicked
                   
                if FRAMERATE_SEL.checkForInput(mousePos):
                   
                    match framerate:
                        case 24:
                            framerate = 40
                        case 40:
                            framerate = 60
                        case 60:
                            framerate = 24
                   
                    FRAMERATE_SEL.set_text("Current Framerate: " + str(framerate) + " >>")
                    with open("userprefs.txt", "w") as prefs_file:
                        prefs_file.write(str(framerate))
                   
        pygame.display.update()
        clock.tick(int(framerate))
        # update the display
