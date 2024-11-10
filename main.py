import pygame
import math
from datetime import datetime, timedelta
from time import time
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')
FONT = pygame.font.SysFont('verdana', 12)

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
SCALE = 13 / AU # Bigger number = zoom in
TIMESTEP = 1440 # 1 day/sec (1440 seconds per frame @ 60fps)
bodies = []
elapsed_time = datetime(2000, 1, 1)

# Schedule an event which updates the onscreen text once every 500ms
UPDATE_TEXT_EVENT = pygame.USEREVENT
UPDATE_DELAY = 500
pygame.time.set_timer(UPDATE_TEXT_EVENT, UPDATE_DELAY)

class Planet:
    def __init__(self, name, x, y, radius, colour, mass):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.distance_in_au = 0
        self.speed = 0
        self.show_path = True

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        # Draw a circle on screen to represent the planet
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.colour, (x, y), self.radius)

        # Render the orbital path
        if (len(self.orbit) > 10) & (self.sun == False):
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            if self.show_path:
                pygame.draw.lines(win, self.colour, False, updated_points, 1)

        if not self.sun:
            # Render the planet's name
            planet_text = FONT.render(f'{self.name}', 1, WHITE)
            win.blit(planet_text, (10, ((bodies.index(self) - 1) * 18) + 10))

            # Render the distance to the sun in AU
            distance_text = FONT.render(f'{self.distance_in_au} AU', 1, WHITE)
            win.blit(distance_text, (70, ((bodies.index(self) - 1) * 18) + 10))

            # Render the planet's absolute velocity (speed)
            speed_text = FONT.render(f'{self.speed:.3f} Km/s', 1, WHITE)
            win.blit(speed_text, (150, ((bodies.index(self) - 1) * 18) + 10))

    # Sum the gravitational forces on a planet from all other planets
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
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        
        self.orbit.append((self.x, self.y))
                
def main():
    run = True
    paused = False
    clock = pygame.time.Clock()

    # Define all planets and their properties (name, radius, colour, mass etc.)
    sun = Planet('Sol', 0, 0, 1, WHITE, 1.9889 * 10**30)
    sun.sun = True

    mercury = Planet('Mercury', -0.387 * AU, 0, 2, DARK_GREY, 3.285 * 10**23)
    mercury.y_vel = 47.4 * 1000

    venus = Planet('Venus', -0.723 * AU, 0, 2, YELLOW_WHITE, 4.8685 * 10**24)
    venus.y_vel = 35.02 * 1000

    earth = Planet('Earth', -1 * AU, 0, 2, BLUE, 5.972 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet('Mars', -1.524 * AU, 0, 2, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet('Jupiter', -5.2038 * AU, 0, 2, ORANGE_WHITE, 1.8982 * 10**27)
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet('Saturn', -9.5826 * AU, 0, 2, CREAM, 5.6834 * 10**26)
    saturn.y_vel = 9.68 * 1000

    uranus = Planet('Uranus', -19.191 * AU, 0, 2, PALE_BLUE, 8.6810 * 10**25)
    uranus.y_vel = 6.80 * 1000

    neptune = Planet('Neptune', -30.07 * AU, 0, 2, DARK_BLUE, 1.0241 * 10**26)
    neptune.y_vel = 5.43 * 1000

    global bodies
    bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        # The game loop will run a maximum of 60 times per second
        clock.tick(60) 

        # Fill the window with an RGB colour
        WIN.fill(BLACK)

        # Loop through each game event (keypresses etc.)
        global TIMESTEP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == UPDATE_TEXT_EVENT:
                # Update calculated values
                for body in bodies:
                    body.speed = math.sqrt(body.x_vel ** 2 + body.y_vel ** 2) / 1000
                    body.distance_in_au = round(body.distance_to_sun/AU, 3)
                global elapsed_time
                elapsed_time = elapsed_time + timedelta(seconds=TIMESTEP * (UPDATE_DELAY * 60 / 1000))

            if event.type == pygame.KEYDOWN:
                # Increase/decrease timestep with +/-
                if event.key == pygame.K_KP_PLUS:
                    if paused:
                        paused = False
                    elif multiplier >= 7:
                        TIMESTEP += 1440 * 7
                    elif multiplier >= 1:
                        TIMESTEP += 1440
                    else:
                        continue
                if event.key == pygame.K_KP_MINUS:
                    if multiplier >= 14:
                        TIMESTEP -= 1440 * 7
                    elif multiplier > 1:
                        TIMESTEP -= 1440
                    else:
                        paused = True
                if event.key == pygame.K_PAUSE:
                    paused = not paused
                # Press home to toggle orbital path lines
                if event.key == pygame.K_HOME:
                    for body in bodies:
                        body.show_path = not body.show_path

        # Draw the planets and orbital paths
        for body in bodies:
            if not paused:
                body.update_position(bodies)

            body.draw(WIN)

        # Render the current time multiplier
        multiplier = int((TIMESTEP) / (1440))
        multiplier_text = FONT.render('PAUSED' if paused else f'{multiplier} day/s', 1, WHITE)
        WIN.blit(multiplier_text, (10, 20 + ((len(bodies) - 1) * 18)))

        # Render the control tips
        multiplier_tip = FONT.render('NUMPAD +/- to speed up or slow down time', 1, WHITE)
        WIN.blit(multiplier_tip, (10, 780))
        path_tip = FONT.render('HOME to toggle orbital paths', 1, WHITE)
        WIN.blit(path_tip, (10, 762))

        # Render the simulation datetime
        date_text = FONT.render(f'Date: {elapsed_time}', 1, WHITE)
        WIN.blit(date_text, (10, 744))

        # Tell pygame to draw the next frame
        pygame.display.update()

    pygame.quit()

main()