import m_math
import keyboard

class Physc():
 def __init__(self, cx, cy, cz, vertices, grspeed):
    self.x = cx
    self.y = cy
    self.z = cz
    self.grspeed = grspeed
    self.vertices = vertices
 def pyhogorsm(self,s):
    return math.sqrt(math.pow(abs(self.x - s.x), 2) + math.pow(abs(self.y - s.y)) + math.pow(abs(self.z - s.z), 2))

 def move(self, x, y, z):
     # Change the x y and z values
     self.x += x
     self.y += y
     self.z += z

     # Move each of the vertices
     for i in range(len(self.vertices)):
         self.vertices[i] = (self.vertices[i][0] + x, self.vertices[i][1] + y, self.vertices[i][2] + z)
 def Collideres(self,s):
    col_x = abs(self.x - s.x) < (self.width / 2) + (s.width / 2)
    col_y = abs(self.y - s.y) < (self.height / 2) + (s.height / 2)
    col_z = abs(self.z - s.z) < (self.depth / 2) + (s.depth / 2)


    return (col_x and col_y and col_z)
class PhyscRan(Physc):

 def __init__(self):
     ph =Physc()
     ph.__init__()
 def phys(self):
     None
 def plyerphys(self, ground):
     jumpspeed = 9
     ph = Physc()
     plyspeed = 0
     fallspeed = self.grspeed / 2
     gravity = self.grspeed
     # Gravity
     if plyspeed > -fallspeed:
         plyspeed -= self.grspeed

     # Check if the player has collided with the ground
     if ph.colliders(ground):
         # Set jumping to false and yspeed to 0
         jumped = False
         p1yspeed = 0
         # Move the player out of the ground
         while ph.collide(ground):
             ph.move(0, gravity, 0)

     # Check if the space key is pressed and the player isn't currently jumping
     if keyboard.is_pressed('j') and not jumped:
         p1yspeed = jumpspeed
         jumped = True
