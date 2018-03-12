from pyglet.gl import *


class Window(pyglet.window.Window):

    def __init__(self, width, height, title='', resizable=False):
        super(Window, self).__init__(width, height, title, resizable)


if __name__ == '__main__':
    window = Window(400, 400, 'Hello World!', True)

    pyglet.app.run()
