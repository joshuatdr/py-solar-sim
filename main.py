import pygame
import math
from datetime import datetime, timedelta
from time import time
pygame.init()

# Initialise window, fonts
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sol.py')
FONT = pygame.font.SysFont('verdana', 12)
LABEL_FONT = pygame.font.SysFont('verdana', 8)

# Define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
YELLOW_WHITE = (255, 242, 128)
ORANGE_WHITE = (217, 175, 139)
CREAM = (237, 226, 209)
PALE_BLUE = (199, 221, 237)
DARK_BLUE = (40, 61, 153)
AU = 149.6e9 
G  = 6.67428e-11 

# Declare global variables
scale = 13 / AU # Bigger number = zoom in
timestep = 1440 # 1 day/sec (1440 seconds per frame @ 60fps)
bodies = []
elapsed_time = datetime(2266, 1, 1)
multiplier = (timestep) / (1440)
show_ui = True

# Schedule an event which calculates game data every 50ms
UPDATE = pygame.USEREVENT
UPDATE_DELAY = 50
pygame.time.set_timer(UPDATE, UPDATE_DELAY)

class Planet:
    def __init__(self, name, label, x, y, radius, colour, mass, path_length):
        self.name = name
        self.label = label
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass
        self.path_length = path_length

        self.orbit = []
        self.updated_points = []
        self.sun = False
        self.distance_to_sun = 0
        self.distance_in_au = 0
        self.speed = 0
        self.show_path = True
        self.show_label = False

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        global show_ui

        # Draw a circle on screen to represent the planet
        x = self.x * scale + WIDTH / 2
        y = self.y * scale + HEIGHT / 2
        pygame.draw.circle(win, self.colour, (x, y), self.radius)

        # Render the orbital path
        if (len(self.updated_points) > 2) & (self.sun == False):
            if self.show_path:
                pygame.draw.lines(win, self.colour, False, self.updated_points, 1)

        if not self.sun:
            if self.show_label:
                # Render the planet's label
                planet_label = LABEL_FONT.render(f'{self.label}', 1, WHITE)
                win.blit(planet_label, (x - 3, y + 5))

            if show_ui:
                # Render the planet's name
                planet_text = FONT.render(f'{self.name}', 1, WHITE)
                win.blit(planet_text, (10, ((bodies.index(self) - 1) * 18) + 10))

                # Render the distance to the sun in AU
                distance_text = FONT.render(f'{self.distance_in_au} AU', 1, WHITE)
                win.blit(distance_text, (70, ((bodies.index(self) - 1) * 18) + 10))

                # Render the planet's absolute velocity (speed)
                speed_text = FONT.render(f'{self.speed:.3f} Km/s', 1, WHITE)
                win.blit(speed_text, (150, ((bodies.index(self) - 1) * 18) + 10))

    # Sum the gravitational forces on a planet from all other bodies
    # And return the net force
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = (G * self.mass * other.mass) / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    # Calculate the position of the planet for this frame
    def update_position(self, planets):
        if self.sun:
            return
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * timestep
        self.y_vel += total_fy / self.mass * timestep

        self.x += self.x_vel * timestep
        self.y += self.y_vel * timestep
                
def main():
    run = True
    paused = False
    clock = pygame.time.Clock()

    # Define all planets and their properties (name, radius, colour, mass etc.)
    sun = Planet('Sol', 'S', 0, 0, 1, WHITE, 1.9889 * 10**30, 0)
    sun.sun = True

    mercury = Planet('Mercury', 'Me', -0.387 * AU, 0, 2, DARK_GREY, 3.285 * 10**23, 4)
    mercury.y_vel = 47.4 * 1000

    venus = Planet('Venus', 'V', -0.723 * AU, 0, 2, YELLOW_WHITE, 4.8685 * 10**24, 10)
    venus.y_vel = 35.02 * 1000

    earth = Planet('Earth', 'E', -1 * AU, 0, 2, BLUE, 5.972 * 10**24, 18)
    earth.y_vel = 29.783 * 1000

    mars = Planet('Mars', 'Ma', -1.524 * AU, 0, 2, RED, 6.39 * 10**23, 34)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet('Jupiter', 'J', -5.2038 * AU, 0, 2, ORANGE_WHITE, 1.8982 * 10**27, 220)
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet('Saturn', 'S', -9.5826 * AU, 0, 2, CREAM, 5.6834 * 10**26, 570)
    saturn.y_vel = 9.68 * 1000

    uranus = Planet('Uranus', 'U', -19.191 * AU, 0, 2, PALE_BLUE, 8.6810 * 10**25, 1600)
    uranus.y_vel = 6.80 * 1000

    neptune = Planet('Neptune', 'N', -30.07 * AU, 0, 2, DARK_BLUE, 1.0241 * 10**26, 3200)
    neptune.y_vel = 5.43 * 1000

    global bodies
    bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        # The game loop will run a maximum of 60 times per second
        clock.tick(60) 

        # Fill the window with an RGB colour
        WIN.fill(BLACK)

        # Get global variables
        global timestep
        global scale
        global show_ui

        # Loop through each game event (keypresses etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == UPDATE:
                if not paused:
                    # Update calculated values
                    for body in bodies:
                        # Absolute velocity of the planet
                        body.speed = math.sqrt(body.x_vel ** 2 + body.y_vel ** 2) / 1000
                        # Distance in AU to the sun
                        body.distance_in_au = round(body.distance_to_sun/AU, 3)

                        if body.path_length == 0:
                            continue
                        # Add the current coordinates of the planet to its orbit path
                        body.orbit.append((body.x, body.y))

                        # Remove the oldest points first if orbit exceeds the path length
                        # Path length is scaled to the current time multiplier
                        body.updated_points = []
                        path_scale = int(body.path_length * (365 / multiplier))
                        if len(body.orbit) > path_scale:
                            body.orbit = body.orbit[-path_scale:]

                        for point in body.orbit:
                            x, y = point
                            x = x * scale + WIDTH / 2
                            y = y * scale + HEIGHT / 2
                            body.updated_points.append((x, y))

                    # Calculate the current datetime since program was started
                    global elapsed_time
                    elapsed_time = elapsed_time + timedelta(seconds=timestep * (UPDATE_DELAY * 60 / 1000))

            if event.type == pygame.KEYDOWN:
                # Increase/decrease timestep with +/-
                if event.key == pygame.K_KP_PLUS:
                    if paused:
                        paused = False
                    elif (multiplier >= 7) & (multiplier < 365):
                        if multiplier >= 364:
                            timestep = 525600
                            continue
                        timestep += 1440 * 7
                    elif (multiplier >= 1) & (multiplier < 7):
                        timestep += 1440
                    elif (multiplier >= (60/1440)) & (multiplier < 1):
                        timestep += 60
                    else:
                        continue
                if event.key == pygame.K_KP_MINUS:
                    if multiplier >= 14:
                        timestep -= 1440 * 7
                    elif multiplier > 1:
                        timestep -= 1440
                    elif multiplier > (60/1440):
                        timestep -= 60
                    else:
                        paused = True
                # Press PAUSE to pause the simulation
                if event.key == pygame.K_PAUSE:
                    paused = not paused
                # Press HOME to toggle orbital path lines
                if event.key == pygame.K_HOME:
                    for body in bodies:
                        body.show_path = not body.show_path
                # Press DEL to reset orbital path lines
                if event.key == pygame.K_DELETE:
                    for body in bodies:
                        body.orbit = []
                # Press L to toggle planet labels
                if event.key == pygame.K_l:
                    for body in bodies:
                        body.show_label = not body.show_label
                # Press H to toggle UI
                if event.key == pygame.K_h:
                    show_ui = not show_ui
                # Zoom with PgUp/PgDown
                if event.key == pygame.K_PAGEUP:
                    scale = scale * 2
                if event.key == pygame.K_PAGEDOWN:
                    scale = scale / 2

        # Calculate the next position of the planet if not paused
        # And draw the planets / path lines
        for body in bodies:
            if not paused:
                body.update_position(bodies)

            body.draw(WIN)

        multiplier = (timestep) / (1440)
        if show_ui:
            # Render the current time multiplier
            if multiplier == 365:
                multiplier_format = '1 year/s'
            elif multiplier >= 1:
                multiplier_format = f'{multiplier:.0f} day/s'
            else:
                multiplier_format = f'{multiplier / (60/1440):.0f} hr/s'

            multiplier_text = FONT.render('PAUSED' if paused else multiplier_format, 1, BLUE)
            WIN.blit(multiplier_text, (10, 38 + ((len(bodies) - 1) * 18)))

            # Render the control tips
            multiplier_tip = FONT.render('PgUp/PgDn to zoom', 1, WHITE)
            WIN.blit(multiplier_tip, (10, 780))

            multiplier_tip = FONT.render('NUMPAD +/- to speed up or slow down time', 1, WHITE)
            WIN.blit(multiplier_tip, (10, 762))

            path_tip = FONT.render('HOME to toggle orbital paths', 1, WHITE)
            WIN.blit(path_tip, (10, 744))

            label_tip = FONT.render('L to toggle planet labels', 1, WHITE)
            WIN.blit(label_tip, (10, 726))

            pause_tip = FONT.render('PAUSE to pause', 1, WHITE)
            WIN.blit(pause_tip, (10, 708))

            hide_ui_tip = FONT.render('H to hide the UI', 1, WHITE)
            WIN.blit(hide_ui_tip, (10, 690))

            # Render the simulation datetime
            date_text = FONT.render(f'Date: {elapsed_time}', 1, WHITE)
            WIN.blit(date_text, (10, 20 + ((len(bodies) - 1) * 18)))

            # Render the frames per second
            fps_text = FONT.render(f'FPS: {clock.get_fps():.1f}', 1, WHITE)
            WIN.blit(fps_text, (730, 10))

        # Tell pygame to draw the next frame
        pygame.display.update()

    pygame.quit()

main()