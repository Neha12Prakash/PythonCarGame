import pygame
import time
import math
from Run_result import *

pygame.font.init()

global point


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 0, 0))
    win.blit(render, (win.get_width() / 2 - render.get_width() /
                      2, win.get_height() / 2 - render.get_height() / 2))
    pygame.display.update()


GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/map.png"), 0.7)

TRACK_BORDER = scale_image(pygame.image.load("imgs/eborder.png"), 6.1)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)
ARROW = scale_image(pygame.image.load("imgs/arrow.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HTN Plan in Autonomous car!")
MAIN_FONT = pygame.font.SysFont("comicsans", 40)
PLAN_FONT = pygame.font.SysFont("comicsans", 15)
FPS = 60


points = {'Osterreichischer_Platz': (89, 496), 'StadtPalais': (561, 504), 'Staatsgalerie': (872, 410),
          'Stuttgart_hbf': (809, 95), 'Gewerschaftshaus': (539, 207), 'Pursuits': (154, 245)}
PATH = []
for i in path:
    PATH.append(points[i])


class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0
        self.plan = plan
        self.path = path
        self.route = route
        self.trust = trust
        self.elapsed_time = elapsed_time

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def stop_time(self):
        self.started = False
        self.level_start_time = self.level_start_time

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 270
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = points[path[0]]

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()


class Arrow(AbstractCar):
    IMG = ARROW
    START_POS = points[path[0]]

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()


def draw(win, images, car, game_info, run):
    for img, pos in images:
        win.blit(img, pos)
    if run:
        arrow.draw(win)
        computer_car.draw_points(win)

        start_text = PLAN_FONT.render(
            f"Source", 1, (200, 0, 50))
        win.blit(start_text, PATH[0])

        end_text = PLAN_FONT.render(
            f"Destination", 1, (200, 0, 50))
        win.blit(end_text, PATH[-1])

        path_text = PLAN_FONT.render(
            f"Path to be taken is:: {game_info.path}", 1, (200, 0, 250))
        win.blit(path_text, (20, HEIGHT - path_text.get_height() - 560))

        route_text = PLAN_FONT.render(
            f"The respective route: {game_info.route}", 1, (200, 0, 250))
        win.blit(route_text, (20, HEIGHT - route_text.get_height() - 540))

        trust_text = PLAN_FONT.render(
            f"The average trust value of the route is: {game_info.trust}%", 1, (200, 0, 250))
        win.blit(trust_text, (20, HEIGHT - trust_text.get_height() - 520))

        elapsed_time_text = PLAN_FONT.render(
            f"Time taken to generate the plan: {game_info.elapsed_time}s", 1, (200, 0, 250))
        win.blit(elapsed_time_text, (20, HEIGHT - elapsed_time_text.get_height() - 500))

        htn_plan = PLAN_FONT.render("HTN Plan:", 1, (200, 0, 250))
        win.blit(htn_plan, (20, HEIGHT - htn_plan.get_height() - 480))

        for ii in range(len(plan)):
            plan_text = PLAN_FONT.render(
                f"{game_info.plan[ii]}", 1, (180, 180, 180))
            win.blit(plan_text, (25, HEIGHT - plan_text.get_height() - (460 - ii * 15)))

    car.draw(win)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, computer_car):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()


def ccp(c_car):
    rect = pygame.Rect(
        c_car.x, c_car.y, c_car.img.get_width(), c_car.img.get_height())
    point = [rect[0], rect[1]]
    return point


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (TRACK_BORDER, (0, 0))]
computer_car = ComputerCar(2.5, 2.5, PATH)
arrow = Arrow(2.8, 2.8, PATH)
reward = None
flag = False
game_info = GameInfo()
draw(WIN, images, computer_car, game_info, not run)
blit_text_center(WIN, MAIN_FONT, "Autonomous driving using HTN Planning!")
time.sleep(2)
draw(WIN, images, computer_car, game_info, not run)
blit_text_center(WIN, MAIN_FONT, "Generating HTN Plan")
time.sleep(1)
draw(WIN, images, computer_car, game_info, not run)
blit_text_center(WIN, MAIN_FONT, "Get!")
time.sleep(1)
draw(WIN, images, computer_car, game_info, not run)
blit_text_center(WIN, MAIN_FONT, "Set!")
time.sleep(1)
draw(WIN, images, computer_car, game_info, not run)
blit_text_center(WIN, MAIN_FONT, "Gooooo!")
time.sleep(1)
manual = False
game_info.start_level()
while run:
    clock.tick(FPS)
    draw(WIN, images, computer_car, game_info, run)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
    if run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            run = False
            manual = True
            reward = False
        computer_car.move()
        arrow.move()

        point = ccp(computer_car)
        # print(point)
        last = len(computer_car.path)
        # print(last)
        destination_ccp = computer_car.path[last - 1]
        last_point = tuple(point)
        if not manual:
            result1 = all(x < (y + 20) for x, y in zip(destination_ccp, last_point))
            result2 = all(x > (y - 20) for x, y in zip(destination_ccp, last_point))
            reached = result1 and result2
            if reached:
                game_info.stop_time()
                reward = True
                draw(WIN, images, computer_car, game_info, run)
                blit_text_center(WIN, MAIN_FONT, "Successfully reached the destination using HTN Planning!")
                time.sleep(1)


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = tuple(point)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


player_car = PlayerCar(3.5, 3.5)
if manual:
    blit_text_center(WIN, MAIN_FONT, "Unfortunately lost trust on autonomous driving!")
    pygame.display.update()
    time.sleep(2)
    draw(WIN, images, player_car, game_info, run)
    blit_text_center(WIN, MAIN_FONT, "Driver in control of the car!")
    pygame.display.update()
    time.sleep(2)
while manual:
    clock.tick(FPS)
    draw(WIN, images, player_car, game_info, run)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True
            manual = False
            break

    move_player(player_car)
    handle_collision(player_car, computer_car)
print(computer_car.path)
pygame.quit()

print(path)

print('Reward is: ' + str(reward))

file = open('Reward.txt', 'rt')
data = file.read()
file = open('Reward.txt', 'rt')
file_lines = file.readlines()
# route = ['School zone', 'Pedestrian crossing', 'Pedestrian crossing']
for r in route:
    r = r + ' = '
    for line in file_lines:
        line = line.strip()
        if r in line:
            route_reward = int(line.partition(r)[2])
            if reward:
                route_reward = route_reward + 1
            elif reward is None:
                route_reward = route_reward
            elif not reward:
                route_reward = route_reward - 1
            update = r + str(route_reward)
            data = data.replace(line, update)
file.close()
file = open('Reward.txt', 'wt')
file.write(data)
file.close()
