import simple_draw as sd


def draw_rainbow(center=sd.get_point(-400, -400), width=30, radius=1000):
    """
        Функция рисует радугу с центром center, толщиной полос width, и радиусом radius
    """
    rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                      sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)
    for i, color in enumerate(rainbow_colors):
        sd.circle(center, radius+i*width, color, width)


if __name__ == '__main__':
    sd.start_drawing()
    draw_rainbow(sd.get_point(-400, -400), 30, 1000)
    sd.finish_drawing()
    sd.pause()
