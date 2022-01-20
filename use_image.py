import pyvirtualcam
import cv2

frame = cv2.imread("example.jpg")
width = frame.shape[1]
height = frame.shape[0]
cam = pyvirtualcam.Camera(width=width, height=height, fps=20)
while True:
    cam.send(frame)
    cam.sleep_until_next_frame()
    