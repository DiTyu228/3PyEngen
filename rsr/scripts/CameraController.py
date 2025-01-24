import m_math as maths
import MainFrame.ObjectCore as Behaver

import keyboard
import MainFrame.WinMeneger as mg

x, y = mg.GetScreenZise()
mouse = mg.mouse()
mx, my = mouse.get_position()

class CameraController(Behaver.GameObject):

    def start(self):
        print("camera start")


    def update(self):
        global x
        global y
        speed = 1
        print(mx, my)
        if keyboard.is_pressed('esc'):
            quit()
        if keyboard.is_pressed('w'):
            self.transform.position.x += (x / mouse.get_position()[1]) * speed
            self.transform.position.y += (y / mouse.get_position()[0]) * speed
        if keyboard.is_pressed('s'):
            self.transform.position.x -= (x / mouse.get_position()[1]) * speed
            self.transform.position.y -= (y / mouse.get_position()[0]) * speed
        if keyboard.is_pressed('a'):
            self.transform.position.x -= (x / mouse.get_position()[1]) * speed
            self.transform.position.y += (y / mouse.get_position()[0]) * speed
        if keyboard.is_pressed('d'):
            self.transform.position.x += (x / mouse.get_position()[1]) * speed
            self.transform.position.y -= (y / mouse.get_position()[0]) * speed
        if keyboard.is_pressed('ctrl'):
            self.transform.position.z += speed
        if keyboard.is_pressed('space'):
            self.transform.position.z -= speed

        self.speed = speed
