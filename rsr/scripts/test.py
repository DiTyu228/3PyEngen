import m_math as maths
import MainFrame.ObjectCore as Behaver


class test(Behaver.GameObject):
    def start(self):
        print("scripst start")

    def update(self):
        self.transform.position.x = self.transform.position.x + 1
        if self.transform.position.x == 20:
            self.transform.position.x = 0

