import MainFrame.WinMeneger as mg
import m_math
import m_math as maths
import MainFrame.ObjectCore as Behaver

TextEngen = Behaver.UIText(m_math.Vector3(255, 255, 255), m_math.Vector2(20, 20))


class TextRenderTest(Behaver.GameObject):

    def start(self):
        global TextEngen
        #TextEngen.Render_text("Hello woreld!")

    def update(self):
        pass
