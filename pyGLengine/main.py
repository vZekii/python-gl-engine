from pyglet.gl import *

import pyGLengine.model as model


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
        self.model = model.Obj('test_models/ak.obj', 'test_models/ak.mtl')

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
        pass

    def on_draw(self):
        """
        Called on every update along with scheduled functions
        """
        self.clear()
        self.set3d()

        glTranslatef(0, 0, -10)  # Move the camera back to see the model
        self.model.rotation[1] += 2  # Rotate the model by 2 degrees on the y axis per update
        self.model.draw()


if __name__ == '__main__':
    window = Window(400, 400, 'Hello World!', True)
    glClearColor(0.2, 0.5, 0.8, 1)
    pyglet.app.run()
