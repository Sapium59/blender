import os

import cv2
from tqdm import tqdm

class VideoSaver:
    def __init__(self, save_path, FPS=30, frameSize=(1920, 1080), isSave=True, isColor=True):
        self.isSave = isSave
        if self.isSave:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.out = cv2.VideoWriter(save_path, fourcc, FPS, frameSize, isColor=isColor)
 
    def write(self, frame):
        if self.isSave: 
            self.out.write(frame)
 
    def __del__(self):
        print("killed VideoSaver")
        if self.isSave: 
            self.out.release()

def make_video(img_dir, FPS=24):
    save_path=img_dir + ".mp4"
    print(f"Saving video: {save_path}")
    vs = VideoSaver(save_path=save_path, FPS=FPS)
    
    img_files = sorted(os.listdir(img_dir))
    for img_file in tqdm(img_files):
        img = cv2.imread(os.path.join(img_dir, img_file))
        vs.write(img)

if __name__ =="__main__":
    make_video(img_dir=r"F:\MyPython\blender\rendered\animate01-Dec 17 13-50-41")
