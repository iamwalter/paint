import pygame, random, time, _thread
from pygame.locals import *


#Todo: COMMENT THE CODE

class Paint_Color(object):
    def __init__(self, name, r, g, b):
        self.name = name
        self.rgb = (r, g, b)

class PaintProgram(object):
    def __init__(self):
        pygame.init()

        self.init_colors()
        self.init_screen(1080, 720)

    def init_screen(self, x, y):
        self.screen = pygame.display.set_mode((x, y), HWSURFACE | DOUBLEBUF | RESIZABLE)

        self.draw_surface = pygame.Surface(self.screen.get_size())
        self.draw_surface.fill(self.white.rgb)

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.myfont = pygame.font.SysFont("monospace", 15)

        # render text

        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_caption('Paint Remastered')

    def init_colors(self):
        self.white = Paint_Color("White", 255, 255, 255)
        self.black = Paint_Color("Black", 0, 0, 0)
        self.red   = Paint_Color("Red",   255, 0, 0)
        self.blue  = Paint_Color("Blue",  0, 0, 255)
        self.yellow= Paint_Color("Yellow",255, 255, 0)
        self.green = Paint_Color("Green", 0, 255, 0)
        self.purple= Paint_Color("Purple",153, 0, 153)
        self.roze  = Paint_Color("Roze",  255, 0, 255)

        self.colors = [self.white, self.black, self.red, self.blue, self.yellow, self.green, self.purple, self.roze]
        self.color_index = 2
        self.current_draw_color = self.colors[self.color_index]

        self.brush_width = 5

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit the game
                self.exit_program(0)
            if event.type == pygame.VIDEORESIZE: # Resize
                self.resize(event.dict['size'][0], event.dict['size'][1])
            if pygame.mouse.get_pressed()[0]: #Left Mouse Button
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                self.draw(x, y, self.current_draw_color.rgb, self.brush_width)
            if pygame.mouse.get_pressed()[2]:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                self.draw(x, y, self.white.rgb, 20)
            if pygame.mouse.get_pressed()[1]:
                self.change_draw_color()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: self.change_brush_width(1)
                if event.button == 5: self.change_brush_width(-1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: # Clear the screen
                    self.clear()
                if event.key == pygame.K_r: # Change draw color
                    self.change_draw_color()
                if event.key == pygame.K_e:
                    self.change_brush_width(1)
                if event.key == pygame.K_q:
                    self.change_brush_width(-1)
                if event.key == pygame.K_s:
                    self.save()
                if event.key == pygame.K_ESCAPE:
                    self.exit_program(0)

    def save(self):
        save_str = "{}-{}-{} {}_{}_{}".format(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday,
                                              time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        try:
            pygame.image.save(self.draw_surface, "pictures/{}.png".format(save_str))
            print("Image saved as {}.png".format(save_str))
        except:
            print("Could not save image {}.png".format(save_str))

    def change_brush_width(self, change):
        self.brush_width += change

        if self.brush_width <= 0:
            self.brush_width = 1


    def change_draw_color(self):
        self.color_index += 1

        if self.color_index == len(self.colors):
            self.color_index = 0

        self.current_draw_color = self.colors[self.color_index]

        print('Changing color to {}'.format(self.current_draw_color.name))

    def clear(self):
        self.draw_surface.fill(self.white.rgb)

    def draw(self, x, y, color, width):
        pygame.draw.circle(self.draw_surface, color, (x, y), width)

    def resize(self, x, y):
        self.init_screen(x, y)

        print("Screen resized to X: {}, Y: {}...".format(x, y))

    def render(self):
        while self.running:
            self.clock.tick(120)

            self.screen.blit(self.draw_surface, (0, 0))

            current_color_label = self.myfont.render("Current Color: {}".format(self.current_draw_color.name), 1, self.black.rgb)
            brush_width_label = self.myfont.render("Brush Width: {}".format(self.brush_width), 1, self.black.rgb)

            self.screen.blit(current_color_label, (0, 0))
            self.screen.blit(brush_width_label, (0, 12))


            pygame.display.update()

    def logic(self):
        # Start render thread
        try:
            _thread.start_new_thread(self.render, ())
        except:
            print("Could not start render thread!")

        while self.running:
            self.get_input()

    def exit_program(self, state):
        self.running = False
        print("Quitting program with a state of {}.".format(state))
        pygame.quit()
        exit(0)

    def start(self):
        self.logic()

paint = PaintProgram()
paint.start()

