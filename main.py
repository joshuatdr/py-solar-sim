import pygame
import math
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

global TIMESTEP
TIMESTEP = 86400

global bodies
bodies = []


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
        self.circumference = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.colour, (x, y), self.radius)

        if (len(self.orbit) > 10) & (self.sun == False):
            updated_points = []
            for point in self.orbit:
                # Remove the oldest points in the orbit line
                # if self.circumference != 0:
                #     if len(updated_points) > (self.circumference - 50):
                #         self.orbit.pop(0)

                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.colour, False, updated_points, 1)

        if not self.sun:
            # Render the distance to the sun in AU
            distance_text = FONT.render(f'{round(self.distance_to_sun/AU, 3)} AU', 1, WHITE)
            win.blit(distance_text, (70, (bodies.index(self) * 18)))

            # Render the planet's name
            planet_text = FONT.render(f'{self.name}', 1, WHITE)
            win.blit(planet_text, (10, (bodies.index(self) * 18)))

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

        # if self.circumference != 0:
        #     return
        # if (len(self.orbit) > 50) & (self.sun == False):
        #     curr_x = round(self.x * SCALE, 0)
        #     curr_y = round(self.y * SCALE, 0)
        #     start_x = round(self.orbit[0][0] * SCALE, 0)
        #     start_y = round(self.orbit[0][1] * SCALE, 0)

        #     if (curr_x, curr_y) == (start_x, start_y):
        #         self.circumference = len(self.orbit)
                # print(f'{self.name} Circumference: {self.circumference}')
                
def main():
    run = True
    paused = False
    clock = pygame.time.Clock()

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                global TIMESTEP
                # Increase/decrease timestep by 0.5x with +/-
                if event.key == pygame.K_KP_PLUS:
                    if paused:
                        paused = False
                    TIMESTEP += 86400 / 2
                if event.key == pygame.K_KP_MINUS:
                    if TIMESTEP != 0:
                        TIMESTEP -= 86400 / 2
                    else:
                        paused = True
                # Press home to toggle orbital path lines
                if event.key == pygame.K_HOME:
                    for body in bodies:
                        body.orbit = []

        if not paused:
            for body in bodies:
                body.update_position(bodies)
                body.draw(WIN)

        timestep_text = FONT.render(f'{'PAUSED' if TIMESTEP == 0 else str(TIMESTEP/86400) + ' yr/sec'}', 1, WHITE)
        WIN.blit(timestep_text, (10, (len(bodies) * 18)))

        # Tell pygame to draw the next frame
        pygame.display.update()

    pygame.quit()

main()