import pygame, sys, os
from . import sim_select
from ui_elements import Button
import checks
import simulations
import display_classes

# defining units
UNITS = {
    "Mass": "kg",
    "Amplitude": "m",
    "Spring Constant": "N/m",
    "Angular Velocity": "rad/s",
    "Period of Oscillation": "s",
    "Position": "m",
    "Velocity": "m/s",
    "Acceleration": "m/s²",
    "Length": "m",
    "Acceleration to Gravity": "m/s²",
    "Initial Angular Displacement": "degrees",
    "Angular Oscillation Frequency": "rad/s",
    "Angular Displacement": "rad",
    "Distance Travelled from Equilibrium": "m",
    "Angular Rotation Velocity": "rad/s",
    "Linear Speed": "m/s",
    "Angular Acceleration": "rad/s²",
    "Launch Speed": "m/s",
    "Launch Angle": "degrees",
    "Maximum Height": "m",
    "Range": "m",
    "Height": "m",
    "Horizontal Distance": "m",
    "Star Mass": "kg",
    "Object Mass": "kg",
    "Orbital Radius": "m",
    "Orbital Time Period": "s",
    "Angular Position in Cycle": "rad",
    "Primary Object Mass": "kg",
    "Secondary Object Mass": "kg",
    "Orbital Separation": "m",
    "Primary Orbit Radius": "m",
    "Secondary Orbit Radius": "m",
    "Orbital Time Period": "s",
    "Primary Angular Position": "rad",
    "Secondary Angular Position": "rad",
    "Object A Speed": "m/s",
    "Object B Speed": "m/s",
    "Final Speed of Object A": "m/s",
    "Final Speed of Object B": "m/s",
    "Total Kinetic Energy Loss": "J",
    "Impulse A on B": "Ns",
    "Impulse B on A": "Ns",
    "Displacement": "m",
    "Object A Mass": "kg",
    "Object B Mass": "kg",
    "Maximum Velocity": "m/s",
    "Maximum Acceleration": "m/s²",
    "Object A Position": "m",
    "Object B Position": "m"   
}

pygame.init()
# initialise the pygame module for later use

clock = pygame.time.Clock()
# set up clock to tick with framerate

def get_font(size): # function to return desired font data
    return pygame.font.SysFont("Times New Roman", size)

def load(framerate, name, simulationID):
    
    # get the correct display class from the simulation id
    match simulationID:
        case "mass_spring":
            display_simulation = display_classes.mass_spring()
        case "pendulum":
            display_simulation = display_classes.pendulum()
        case "projectile":
            display_simulation = display_classes.projectile()
        case "orbit":
            display_simulation = display_classes.orbit()
        case "collision":
            display_simulation = display_classes.collision()
        case "kinematics":
            display_simulation = display_classes.kinematics()
        case None:
            print("Error: No simulation to display")

    
    SCREEN = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    pygame.display.set_caption("MechLab v1.0.0")
    background = pygame.image.load("images\\sim_viewport.png")
    background = pygame.transform.scale(background, SCREEN.get_size())
    # initialise the display and background image
   
    RETURN_BUTTON = Button(
        image=None,
        pos=(1655, 170), # x, y center position of button
        text_input="X",
        font=get_font(30),
        base_colour=(255, 255, 255), # white
        hovering_colour=(0, 0, 0) # black
    )
   
    PAUSE_BUTTON = Button(
        image=None,
        pos=(1594, 168), # x, y center position of button
        text_input="| |",
        font=pygame.font.SysFont("Times New Roman", 25, bold=True),
        base_colour=(255, 255, 255), # white
        hovering_colour=(0, 0, 0) # black
    )
    # pause button instantiation
   
    PLAY_BUTTON = Button(
        image=None,
        pos=(1535, 170), # x, y center position of button
        text_input=">",
        font=pygame.font.SysFont("Times New Roman", 25, bold=True),
        base_colour=(255, 255, 255), # white
        hovering_colour=(0, 0, 0) # black
    )
    # play button instantiation
   
    sim_time = 0.0          # time in seconds
    running = False       # we start paused by default
    last_tick = pygame.time.get_ticks()
    data_checked = False
   
    sim_func = sim_func = getattr(simulations, simulationID)
    sim_values = {}
    
    path = f"images/explanations/{simulationID}.png"
    image =  pygame.image.load(path)
    scaled = pygame.transform.smoothscale_by(image, 0.44)
    # defining path and loading image
    
   
    while True: # main program loop, iterating once per frame
        SCREEN.blit(background, (0, 0))
        mousePos = pygame.mouse.get_pos()
        
        # updating the timer
        current_tick = pygame.time.get_ticks()

        if running:
            delta = (current_tick - last_tick) / 1000.0  # ms converting to  seconds
            sim_time += delta
            
        if running and sim_func is not None: # run the simulation function to populate data
            sim_values = sim_func(sim_time)

        last_tick = current_tick
       
        font = get_font(50)
        text_surface = font.render(name, True, (255, 255, 255))
        SCREEN.blit(text_surface, (270, 135))
        # render and display title
        
        timer_font = get_font(20)
        timer_text = f"t = {sim_time:.2f} s"
        timer_surface = timer_font.render(timer_text, True, (255, 255, 255))


        timer_rect = pygame.Rect(1155, 235, 140, 30)
        pygame.draw.rect(SCREEN, (30, 30, 30), timer_rect)
        pygame.draw.rect(SCREEN, (255, 255, 255), timer_rect, 1)

        SCREEN.blit(timer_surface, (timer_rect.x + 8, timer_rect.y + 4))
       # render and display timer
       
        font = get_font(20)

        x = timer_rect.x
        y = timer_rect.y + 30
        line_gap = 24

        for key in sim_values:
            value = sim_values[key]

            unit = ""
            if key in UNITS:
                unit = " " + UNITS[key]

            if type(value) == int or type(value) == float:
                text = key + ": " + f"{value:.3f}" + unit
            else:
                text = key + ": " + str(value)

            text_surface = font.render(text, True, (255, 255, 255))
            SCREEN.blit(text_surface, (x, y))

            y += line_gap
        # render and display simulation text
       
        for item in [RETURN_BUTTON, PAUSE_BUTTON, PLAY_BUTTON]:
            item.changeColour(mousePos)
            item.update(SCREEN)
        # update the state of all buttons, change colour if hovering
   
        for event in pygame.event.get(): # loop to check events
            if event.type == pygame.QUIT: # check if the user presses X on the window
                pygame.quit()
                sys.exit()
                # exit the program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RETURN_BUTTON.checkForInput(mousePos):
                    sim_select.load(framerate)
                # load the sim_select menu
                if PAUSE_BUTTON.checkForInput(mousePos):
                    running = False
                # register simulation pause
                if PLAY_BUTTON.checkForInput(mousePos):

                    if not data_checked:
                        data_valid, message = checks.check_data(simulationID)
                        data_checked = True

                        if not data_valid:
                            print("Simulation file error:")
                            print(message)
                            return

                    running = True
                    
        display_simulation.draw(SCREEN, sim_time)
        # draw the simulation in the viewport
        
        SCREEN.blit(scaled, (1145, 582))
        # draw the scaled explanation image in the correct position
        
        pygame.display.update()
        clock.tick(int(framerate))