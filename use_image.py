import pyvirtualcam
import cv2

frame = cv2.imread("example.png")
cam = pyvirtualcam.Camera(width=width, height=height, fps=20)
while True:
    cam.send(frame)
    cam.sleep_until_next_frame()
    