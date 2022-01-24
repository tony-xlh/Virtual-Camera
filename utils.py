import cv2

def get_img_radio(img):
    width = img.shape[1]
    height = img.shape[0]
    if width>height:
        return width/height
    else:
        return height/width

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
    if get_img_radio(img) > ratio: #17/9 > 16/9 add padding to short side
        if width>height:
            desired_width = width
            desired_height = width / ratio
            top = int((desired_height - height)/2)
            bottom = top
        else:
            desired_width = height / ratio
            desired_height = height
            left = int((desired_width - width)/2)
            right = left
    else: # 4/3 < 16/9 add padding to long side
        if width>=height:
            desired_width = height * ratio
            desired_height = height
            left = int((desired_width - width)/2)
            right = left
        else:
            desired_width = width
            desired_height = width * ratio
            top = int((desired_height - height)/2)
            bottom = top

    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,value=[255,255,255])
    return img 