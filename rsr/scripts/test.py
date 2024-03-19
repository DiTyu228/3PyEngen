import m_math as maths


class test():
    def start(self):
        self.vect = maths.vectors()
        self.i = 1
        print("scripst start")

    def update(self):
        print("scripst update " + str(self.i))
        self.i = self.i + 1