from threading import Thread
import pyvirtualcam
import sys
import cv2
import time
import numpy as np
import utils
from PIL import Image


class VirtualCamera():
    def __init__(self):
        self.cam = None
        self.running = True
      
    def terminate(self):
        self.running = False
          
    def run(self, frame):
        width = frame.shape[1]
        height = frame.shape[0]
        cam = pyvirtualcam.Camera(width=width, height=height, fps=20)
        while self.running==True:
            cam.send(frame)
            cam.sleep_until_next_frame()

ix,iy = -1,-1
previous_tx = 0
previous_ty = 0
current_tx = 0
current_ty = 0
is_mouse_down = False
angle = 0

def move_image(image, tx,ty):
    global current_tx, current_ty
    tx = previous_tx + tx
    ty = previous_ty + ty
    current_tx = tx
    current_ty = ty
    rows, cols=image.shape[:2]
    moving_matrix=np.float64([[1,0,tx],[0,1,ty]])
    return cv2.warpAffine(image, moving_matrix,(cols,rows))

def handle_mouse_events(event,x,y,flags,param):
    global ix,iy, is_mouse_down, vis, img, cam
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y
        is_mouse_down = True
        stop_cam(cam)

    elif event == cv2.EVENT_MOUSEMOVE:
        tx = ix - x
        ty = iy - y
        if is_mouse_down:
            img = move_image(vis, -tx, -ty)

    elif event == cv2.EVENT_LBUTTONUP:
        is_mouse_down = False
        previous_tx = current_tx
        previous_ty = current_ty
        cam = start_cam(img)

def start_cam(img):
    c = VirtualCamera()
    t = Thread(target = c.run, args =(img, ))
    t.start()
    return c
    
def stop_cam(c):
    c.terminate()
          
def rotated(image):
    global angle
    print(angle)
    img_pil = Image.fromarray(image)
    img_pil = img_pil.rotate(angle)
    return np.asarray(img_pil)

def on_rotate(degree):
    global angle
    angle = degree
    print("angle update: "+str(angle))
    
    
def main():
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Rotate','image',0,360, on_rotate)
    cv2.setMouseCallback('image', handle_mouse_events)

    while True:
        time.sleep(0.05)        
        cv2.imshow('image',rotated(img))
        k = cv2.waitKey(1) & 0xFF
        if k == 27: #esc
            cam.terminate()
            break
    
    
if __name__ == "__main__":
    path = "example.png"
    if len(sys.argv) == 2 :
        path = sys.argv[1]
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = utils.add_padding(img)
    vis = img.copy()
    cam = start_cam(img)
    main()