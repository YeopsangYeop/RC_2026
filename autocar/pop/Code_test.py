import time
from pop import Pilot
from pop import Util
import cv2

car = Pilot.AutoCar()

car.steering = 0 #바퀴 회전
car.forward() #전지
car.backward() #후진
car.setSpeed(50) #스피드?
car.joystick() #조이스틱
car.camPan(10) #좌우
car.camTilt(100) #상하
value = car.getGyro() #각속도를 읽어옴
value2 = car.getAccel() #가속도를 읽어옴
Util.enable_imshow()
Util.createIMG()

#----------------------------------------------------------------------------


