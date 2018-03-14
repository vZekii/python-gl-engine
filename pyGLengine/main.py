from pyglet.gl import *
from pyglet.window import key
import math

import model


class Player:
    def __init__(self):
        self.position = [0, 0, 2]  # Start the player 2 spaces back from origin
        self.rotation = [0, 0]

    def update(self, dt, keys):
        s = dt * 5
        rotation_y = -self.rotation[1] / 180 * math.pi
        dx, dz = math.sin(rotation_y), math.cos(rotation_y)
        dx /= 12; dz /= 12

        if keys[key.W]:
            self.position[0] += dx
            self.position[2] -= dz
        if keys[key.S]:
            self.position[0] -= dx
            self.position[2] += dz
        if keys[key.A]:
            self.position[0] -= dz
            self.position[2] -= dx
        if keys[key.D]:
            self.position[0] += dz
            self.position[2] += dx

        if keys[key.SPACE]:
            self.position[1] += s
        if keys[key.LSHIFT]:
            self.position[1] -= s

    def mouse_motion(self, dx, dy):
        dx /= 8
        dy /= 8
        self.rotation[0] += dy
        self.rotation[1] -= dx

        if self.rotation[0] > 90:
            self.rotation[0] = 90
        elif self.rotation[0] < -90:
            self.rotation[0] = -90


class Window(pyglet.window.Window):
    def __init__(self, width, height, title='', resizable=False):
        """
        An extension of the pyglet window
        :param width: width of window
        :param height: height of window
        :param title: name of window
        :param resizable: if the window is resizeable or not
        """
        super(Window, self).__init__(width, height, title, resizable)
        self.exclusive = True

        self.player = Player()
        self.model = model.Obj('test_models/ak.obj', 'test_models/ak.mtl')

        # For the player class
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)  # Setup key handling
        pyglet.clock.schedule(self.update)  # Schedule the update function

    @staticmethod
    def set_projection():
        """
        Small function to set projection mode in opengl
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    @staticmethod
    def set_model():
        """
        Small function to set model mode in opengl
        """
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        """
        A function which converts the OpenGL scene into a 3D space
        """
        self.set_projection()
        fov, min_render_dist, max_render_dist = 70, 0.5, 10000
        aspect_ratio = self.width / self.height
        gluPerspective(fov, aspect_ratio, min_render_dist, max_render_dist)
        self.set_model()

    def set2d(self):
        pass  # Not needed quite yet

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_mouse_motion(self, _, __, dx, dy):
        self.player.mouse_motion(dx, dy)

    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def on_mouse_press(self, x, y, button, modifiers):
        if self.exclusive: self.set_exclusive_mouse(False)
        else: self.set_exclusive_mouse(True)

    def on_draw(self):
        """
        Called on every update along with scheduled functions
        """
        self.clear()
        self.set3d()

        glRotatef(-self.player.rotation[0], 1, 0, 0)  # Rotate the players view on the x axis
        glRotatef(-self.player.rotation[1], 0, 1, 0)  # And again on the y axis
        x, y, z = self.player.position
        glTranslatef(-x, -y, -z)  # Factor in player's position

        glTranslatef(0, 0, -10)  # Move the camera back to see the model
        self.model.rotation[1] += 2  # Rotate the model by 2 degrees on the y axis per update
        self.model.draw()


if __name__ == '__main__':
    window = Window(400, 400, 'Hello World!', True)
    glClearColor(0.2, 0.5, 0.8, 1)
    pyglet.app.run()
