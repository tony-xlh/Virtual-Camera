import av
import pyvirtualcam
import sys

def main(path):
    container = av.open(path)
    height = container.streams[0].codec_context.coded_height
    width = container.streams[0].codec_context.coded_width

    cam = pyvirtualcam.Camera(width=width, height=height, fps=20)

    while True:
        container = av.open("example.mp4")
        stream = container.streams.video[0]
        for frame in container.decode(stream):
            frame = frame.to_ndarray(format='bgr24')
            cam.send(frame)
            cam.sleep_until_next_frame()
        
if __name__ == "__main__":
    path = "example.mp4"
    if len(sys.argv) == 2 :
        path = sys.argv[1]
    print(path)
    main(path)
    