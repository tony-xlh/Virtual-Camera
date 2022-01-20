import cv2

def add_padding(img):
    width = img.shape[1]
    height = img.shape[0]
    ratio = 16/9
    
    desired_height = height
    desired_width = width
    top = 0
    bottom = 0
    left = 0
    right = 0
    if height/width != ratio:
        if width>=height:
            desired_width = height * ratio
            desired_height = height
            left = int((desired_width - width)/2)
            right = left
        else:
            desired_width = width
            desired_height = width * ratio
            top = int((desired_height - height)/2)
            right = top

    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,value=[255,255,255])
    return img 