import m_math as maths
import MainFrame.ObjectCore as Behaver


class test(Behaver.GameObject):

    def start(self):

        self.mode = 0
        print("scripst start")

    def update(self):
        self.transform.scale.z = 5



