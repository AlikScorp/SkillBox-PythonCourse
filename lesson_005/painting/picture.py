from lesson_005.painting.snowfall import add_snowflake, draw_flake
from lesson_005.painting.wall import draw_wall
import simple_draw as sd
from lesson_005.painting.fractal import draw_branches_1
from lesson_005.painting.rainbow import draw_rainbow
# Не буду делать туду, но вы все-таки обратите внимание.
# Не нужно смешивать импорты в одну кучу.
# В первую очередь помещаются импорты из стандартной библиотеки python.
# После дополнительные модули, установленные как зависимости.
# И уже после них импортируем тот код, который написали вы.


def draw_house():
    draw_wall(sd.get_point(400, 100), area=(300, 300))
    sd.rectangle(sd.get_point(475, 200), sd.get_point(625, 350), color=sd.background_color, width=0)
    draw_man()
    sd.rectangle(sd.get_point(475, 200), sd.get_point(625, 350), color=sd.COLOR_DARK_CYAN, width=3)

    point_list = [sd.get_point(350, 400), sd.get_point(750, 400), sd.get_point(550, 500)]
    sd.polygon(point_list, color=sd.COLOR_DARK_RED, width=0)

    sd.line(sd.get_point(475, 300), sd.get_point(625, 300), color=sd.COLOR_DARK_CYAN, width=3)
    sd.line(sd.get_point(550, 200), sd.get_point(550, 300), color=sd.COLOR_DARK_CYAN, width=3)


def draw_cloud(point_x, point_y):
    cloud_color = (200, 200, 200)

    sd.circle(sd.get_point(point_x, point_y), radius=sd.random_number(20, 40), color=cloud_color, width=0)
    sd.circle(sd.get_point(point_x-40, point_y), radius=sd.random_number(20, 40), color=cloud_color, width=0)
    sd.circle(sd.get_point(point_x+35, point_y), radius=sd.random_number(20, 40), color=cloud_color, width=0)
    sd.circle(sd.get_point(point_x, point_y+40), radius=sd.random_number(20, 40), color=cloud_color, width=0)


def draw_sun(center_point, angle=90):
    sd.circle(center_position=center_point, radius=50, color=sd.COLOR_YELLOW, width=0)

    for i in range(10):
        ray = sd.get_vector(center_point, angle+i*360/10, width=5)
        ray.draw(color=sd.COLOR_YELLOW)


def clear_sun(center_point, angle=90):
    sd.circle(center_position=center_point, radius=50, color=sd.background_color, width=0)

    for i in range(10):
        ray = sd.get_vector(center_point, angle+i*360/10, width=5)
        ray.draw(color=sd.background_color)


def draw_tree(root=sd.get_point(900, 130), size=100):
    sd.line(sd.get_point(root.x, root.y - 30), root, color=(134, 127, 0), width=3)
    draw_branches_1(start_point=root, angle=90, length=size)


def snowdrift(n=50):
    snowflakes = []
    for i in range(n):
        snowflakes.append(add_snowflake(5, 10, area=(sd.get_point(50, 100), sd.get_point(300, 100))))
        draw_flake(snowflakes, i)


def draw_man():
    x, y = 515, 270

    sd.circle(sd.get_point(x, y), radius=20, color=sd.COLOR_WHITE, width=0)  # head

    sd.circle(sd.get_point(x-7, y+5), radius=4, color=sd.COLOR_BLACK, width=1)  # left ear
    sd.circle(sd.get_point(x-7, y+5), radius=2, color=sd.COLOR_BLACK, width=0)
    # sd.line(sd.get_point(x-9, y+5), sd.get_point(x-5, y+5), color=sd.COLOR_BLACK, width=1)

    sd.circle(sd.get_point(x+7, y+5), radius=4, color=sd.COLOR_BLACK, width=1)  # right ear
    sd.circle(sd.get_point(x+7, y+5), radius=2, color=sd.COLOR_BLACK, width=0)
    # sd.line(sd.get_point(x+5, y+5), sd.get_point(109, 305), color=sd.COLOR_BLACK, width=1)

    nose = sd.get_vector(sd.get_point(x, y-5), 90, 5, width=1)
    nose.draw(color=sd.COLOR_BLACK)
    nose = sd.get_vector(sd.get_point(x, y-5), 30, 3, width=1)
    nose.draw(color=sd.COLOR_BLACK)
    nose = sd.get_vector(sd.get_point(x, y-5), 150, 3, width=1)
    nose.draw(color=sd.COLOR_BLACK)
    mouth = [sd.get_point(x-10, y-8), sd.get_point(x-5, y-15), sd.get_point(x+5, y-15),
             sd.get_point(x+10, y-8), sd.get_point(x+5, y-10), sd.get_point(x-5, y-10)]

    # mouth = [sd.get_point(x-10, y-8), sd.get_point(x, y-15), sd.get_point(x+10, y-8)]

    sd.polygon(mouth, color=sd.COLOR_BLACK, width=1)
    sd.ellipse(sd.get_point(x-20, y-100), sd.get_point(x+20, y-20), color=sd.COLOR_WHITE, width=0)
    tie = [sd.get_point(x-2, y-20), sd.get_point(x-5, y-50), sd.get_point(x, y-55),
           sd.get_point(x+5, y-50), sd.get_point(x+2, y-20)]
    sd.polygon(tie, color=sd.COLOR_BLACK, width=0)

    sd.rectangle(sd.get_point(480, 170), sd.get_point(545, 200), color=sd.COLOR_DARK_CYAN, width=0)
    sd.rectangle(sd.get_point(555, 170), sd.get_point(620, 200), color=sd.COLOR_DARK_CYAN, width=0)


def draw_picture():
    sd.resolution = (1200, 800)
    sd.caption = 'Morning in a country'

    sd.start_drawing()

    draw_house()
    draw_tree()

    draw_sun(sd.get_point(100, 700), angle=30)
    draw_cloud(300, 730)
    draw_cloud(100, 670)
    draw_cloud(500, 650)
    draw_cloud(700, 710)

    sd.rectangle(sd.get_point(0, 0), sd.get_point(sd.resolution[0], 100), color=(180, 130, 31))

    snowdrift(300)
    draw_rainbow(sd.get_point(400, -100), 10, 1000)
    sd.finish_drawing()


def draw_picture_animated():
    angle = 0
    while True:
        sd.start_drawing()

        draw_sun(sd.get_point(100, 700), angle=angle)
        draw_house()
        draw_rainbow(sd.get_point(400, -100), 10, 1000)
        sd.finish_drawing()
        sd.sleep(0.1)
        clear_sun(sd.get_point(100, 700), angle=angle)

        if angle == 360:
            angle = 0
        else:
            angle += 1

        if sd.user_want_exit():
            break


if __name__ == '__main__':
    sd.resolution = (1200, 800)
    draw_picture_animated()
    sd.pause()
