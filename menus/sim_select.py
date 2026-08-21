import pygame, sys
from ui_elements import Button, Tile
from . import main_menu, sim_viewport
import command_parser


pygame.init()
# re-initialise pygame within this module


clock = pygame.time.Clock()
# set up clock to tick with framerate

def get_font(size): # function to return desired font data
    return pygame.font.SysFont("Times New Roman", size)

def load(framerate):
    SCREEN = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    pygame.display.set_caption("MechLab v1.0.0")
    background = pygame.image.load("images\\select_bg.png")
    background = pygame.transform.scale(background, SCREEN.get_size())
    # initialise the display and background image
    
    command_text = ""
    command_active = False
    command_message = "Commands are set, show, reset, format. Type \"help\" after each for information."    
    # setting up the command window
    
    #instantiation of return button
    RETURN_BUTTON = Button(
        image=None,
        pos=(261, 156), # x, y center position of button
        text_input="X",
        font=get_font(30),
        base_colour=(255, 255, 255), # white
        hovering_colour=(0, 0, 0) # black
    )
   
   # instantiating selection tiles
    MS_TILE = Tile(
        title = "Mass-Spring System",
        image = "mass_spring.png",
        position = (540, 375),
    )
   
    PEN_TILE = Tile(
        title = "Simple Pendulum",
        image = "pendulum.png",
        position = (960, 375),
    )
   
    PROJ_TILE = Tile(
        title = "Projectile Motion",
        image = "projectile.png",
        position = (1380, 375),
    )

    ORBIT1_TILE = Tile(
        title = "Planetary Orbit",
        image = "orbit.png",
        position = (540, 600),
    )

    COLLISION_TILE = Tile(
        title = "Direct Collision",
        image = "collision.png",
        position = (960, 600),
    )
    
    KINEMATICS_TILE = Tile(
        title = "Kinematics",
        image = "kinematics.png",
        position = (1380, 600),
    )
    

    while True: # main program loop, iterating once per frame
        SCREEN.blit(background, (0, 0))
        mousePos = pygame.mouse.get_pos() # get mouse position
       
        for tile in [MS_TILE, PEN_TILE, PROJ_TILE, ORBIT1_TILE, COLLISION_TILE, KINEMATICS_TILE]:
            tile.update(SCREEN)
        # update the state of each tile per frame
       
        for item in [RETURN_BUTTON]:
            item.changeColour(mousePos)
            item.update(SCREEN)
        # update the state of all buttons, change colour if hovering
        
        cmd_rect = pygame.Rect(560, 730, 800, 40)

        pygame.draw.rect(SCREEN, (30, 30, 30), cmd_rect)
        pygame.draw.rect(SCREEN, (255, 255, 255), cmd_rect, 1)

        cmd_surface = get_font(20).render(command_text, True, (255, 255, 255))
        SCREEN.blit(cmd_surface, (cmd_rect.x + 8, cmd_rect.y + 8))
        # draw the command window

        # handling re-colouring error messages
        error_words = ["Invalid", "Error", "not found", "Unknown"]

        is_error = False
        for word in error_words:
            if word in command_message:
                is_error = True

        if is_error:
            msg_colour = (255, 100, 100)  
        else:
            msg_colour = (255, 255, 255)  
        
        msg_surface = get_font(18).render(command_message, True, msg_colour)
        SCREEN.blit(msg_surface, (cmd_rect.x, cmd_rect.y + 50))
        # draw the command output beneath the command line
       
        for event in pygame.event.get(): # event checker
           
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # checking for user exit request
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RETURN_BUTTON.checkForInput(mousePos):
                    main_menu.load()
                if MS_TILE.update(SCREEN):
                    sim_viewport.load(framerate, "MASS-SPRING SYSTEM", "mass_spring")
                elif PEN_TILE.update(SCREEN):
                    sim_viewport.load(framerate, "SIMPLE PENDULUM", "pendulum")
                elif PROJ_TILE.update(SCREEN):
                    sim_viewport.load(framerate, "PROJECTILE MOTION", "projectile")
                elif ORBIT1_TILE.update(SCREEN):
                    sim_viewport.load(framerate, "PLANETARY ORBIT", "orbit")
                elif COLLISION_TILE.update(SCREEN):
                    sim_viewport.load(framerate, "DIRECT COLLISION", "collision")
                elif KINEMATICS_TILE.update(SCREEN):
                    sim_viewport.load(framerate, "KINEMATICS", "kinematics")
                elif cmd_rect.collidepoint(mousePos):
                    command_active = True
                else:
                    command_active = False
                    break
                # checking for and handling button clicks
            if event.type == pygame.KEYDOWN:
                if command_active:
                    if event.key == pygame.K_BACKSPACE:
                        command_text = command_text[:-1]

                    elif event.key == pygame.K_RETURN:
                        command_message = command_parser.run_command(command_text)
                        command_text = ""

                    elif len(command_text) <= 50:
                        # prevent text from leaking out of the command box
                        command_text += event.unicode
                        command_message = ""
                # checking for and handling key presses
   
        pygame.display.update()
        clock.tick(framerate)
         # tick the clock forward per frame
         
