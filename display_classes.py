import math
import simulations
import pygame

# defining viewport position
VIEW_X = 274
VIEW_Y = 230
VIEW_W = 842 # 1116 - 274, width
VIEW_H = 696 # 926 - 230, height

def get_font(size): # function to return desired font data
    return pygame.font.SysFont("Times New Roman", size)

# display class for mass spring system
class mass_spring:
    # class constructor method
    def __init__(self):
        self.visual_amplitude = 120
        self.mass_radius = 20
        self.spring_thickness = 4
        self.wall_thickness = 8
        # constants for visual representation

        self.eq_x = VIEW_X + VIEW_W // 2
        self.eq_y = VIEW_Y + VIEW_H // 2
        # define equilibrium as centre of screen
        
    # draw method
    def draw(self, surface, t):
        sim_data = simulations.mass_spring(t)

        if "Error" in sim_data:
            return

        angular_velocity = sim_data["Angular Velocity"]

        # purely visual oscillation
        x_offset = self.visual_amplitude * math.cos(angular_velocity * t)

        mass_x = int(self.eq_x + x_offset)
        mass_y = self.eq_y
        
        anchor_x = self.eq_x - self.visual_amplitude
        anchor_y = self.eq_y

        # draw the "spring"
        pygame.draw.line(
            surface,
            (200, 200, 200),
            (anchor_x - 40, anchor_y),
            (mass_x - self.mass_radius, mass_y),
            self.spring_thickness
        )
        
        # draw the "mass"
        pygame.draw.circle(
            surface,
            (255, 0, 0),
            (mass_x, mass_y),
            self.mass_radius
        )
        
        # draw the surface 
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (VIEW_X, anchor_y + self.mass_radius + (self.wall_thickness / 2)),
            (VIEW_X + VIEW_W, mass_y + self.mass_radius + (self.wall_thickness / 2)),
            self.wall_thickness
        )
        
        # draw the wall
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (self.eq_x - 20 - self.mass_radius - self.visual_amplitude, self.eq_y - self.mass_radius),
            (self.eq_x - 20 - self.mass_radius - self.visual_amplitude, self.eq_y + 25),
            self.wall_thickness
        )
        
# display class for simple pendulum system
class pendulum:
    def __init__(self):
        self.visual_length = 200
        self.bob_radius = 18
        self.string_thickness = 3
        self.support_width = 60
        self.support_thickness = 6

        # pivot point 
        self.pivot_x = VIEW_X + VIEW_W // 2
        self.pivot_y = VIEW_Y + 160

    def draw(self, surface, t):
        sim_data = simulations.pendulum(t)

        if "Error" in sim_data:
            return

        # angular displacement (radians)
        theta = sim_data["Angular Displacement"]

        # bob position
        bob_x = int(self.pivot_x + self.visual_length * math.sin(theta))
        bob_y = int(self.pivot_y + self.visual_length * math.cos(theta))

        # draw ceiling support
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (self.pivot_x - self.support_width // 2, self.pivot_y),
            (self.pivot_x + self.support_width // 2, self.pivot_y),
            self.support_thickness
        )

        # draw string
        pygame.draw.line(
            surface,
            (200, 200, 200),
            (self.pivot_x, self.pivot_y),
            (bob_x, bob_y),
            self.string_thickness
        )

        # draw bob
        pygame.draw.circle(
            surface,
            (255, 0, 0),
            (bob_x, bob_y),
            self.bob_radius
        )
        
# display class for projectile motion system
class projectile:
    def __init__(self):
        self.projectile_radius = 10
        self.ground_thickness = 6

        # visual scaling
        self.scale = 30  # approximate pixels per metre for scaling

        # launch position
        self.start_x = VIEW_X + 50
        self.ground_y = VIEW_Y + VIEW_H - 60

    def draw(self, surface, t):
        sim_data = simulations.projectile(t)

        if "Error" in sim_data:
            return

        height = sim_data["Height"]
        horizontal = sim_data["Horizontal Distance"]

        # stop drawing once projectile hits ground
        if height < 0:
            height = 0

        # convert to screen coordinates
        proj_x = int(self.start_x + horizontal * self.scale)
        proj_y = int(self.ground_y - height * self.scale)

        # draw ground
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (VIEW_X, self.ground_y),
            (VIEW_X + VIEW_W, self.ground_y),
            self.ground_thickness
        )

        # draw projectile if on screen
        if VIEW_X <= proj_x <= VIEW_X + VIEW_W and VIEW_Y <= proj_y < VIEW_Y + VIEW_H:
            pygame.draw.circle(
                surface,
                (255, 0, 0),
                (proj_x, proj_y),
                self.projectile_radius
            )
            
# display class for planetary orbit system
class orbit:
    def __init__(self):
        self.star_radius = 18
        self.planet_radius = 10
        self.orbit_thickness = 1

        # visual scaling
        self.visual_radius = 220

        # centre of orbit at the centre
        self.centre_x = VIEW_X + VIEW_W // 2
        self.centre_y = VIEW_Y + VIEW_H // 2

    def draw(self, surface, t):
        sim_data = simulations.orbit(t)

        if "Error" in sim_data:
            return

        theta = sim_data["Angular Position in Cycle"]

        # planet position - circular orbit
        planet_x = int(self.centre_x + self.visual_radius * math.cos(theta))
        planet_y = int(self.centre_y + self.visual_radius * math.sin(theta))

        # draw orbit path
        pygame.draw.circle(
            surface,
            (120, 120, 120),
            (self.centre_x, self.centre_y),
            self.visual_radius,
            self.orbit_thickness
        )

        # draw star at the centre
        pygame.draw.circle(
            surface,
            (255, 220, 0),
            (self.centre_x, self.centre_y),
            self.star_radius
        )

        # draw planet
        pygame.draw.circle(
            surface,
            (100, 150, 255),
            (planet_x, planet_y),
            self.planet_radius
        )

# display class for 1D direct collision system
class collision:
    def __init__(self):
        self.radius_a = 16
        self.radius_b = 16

        self.track_thickness = 6

        # visual scaling
        self.scale = 60  # pixels per unit distance

        # baseline - collision for surface
        self.track_y = VIEW_Y + VIEW_H // 2

        # starting reference position
        self.origin_x = VIEW_X + VIEW_W // 2

    def draw(self, surface, t):
        sim_data = simulations.collision(t)

        if "Error" in sim_data:
            return

        pos_a = sim_data["Object A Position"]
        pos_b = sim_data["Object B Position"]

        # convert to screen coordinates
        x_a = int(self.origin_x + pos_a * self.scale)
        x_b = int(self.origin_x + pos_b * self.scale)

        # draw track
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (VIEW_X, self.track_y),
            (VIEW_X + VIEW_W, self.track_y),
            self.track_thickness
        )

        if VIEW_X <= x_a <= VIEW_X + VIEW_W:
            # draw object A
            pygame.draw.circle(
                surface,
                (255, 80, 80),
                (x_a, self.track_y - self.radius_a),
                self.radius_a
                )
        if VIEW_X <= x_b <= VIEW_X + VIEW_W:
                # draw object B
            pygame.draw.circle(
                surface,
                (80, 160, 255),
                (x_b, self.track_y - self.radius_b),
                self.radius_b
        )
        
# kinematics system display class
class kinematics:
    def __init__(self):
        self.text = "Nothing to display"
        
    def draw(self, surface, t):
        font = get_font(20)
        text_surface = font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, ((VIEW_X + 5, VIEW_Y + 5)))