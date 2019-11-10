import cv2
import numpy as np
from PIL import Image
import io

class Record:
    def __init__(self, ann_filename):
        ann_filename = ann_filename.replace(".mjpeg", ".txt")
        ann_raw = open(ann_filename).read().split("T")
        self.ann = []
        self.p = []
        self.dets = {}
        for i in range(len(ann_raw)-1):
            a = ann_raw[i].split()
            if len(a)>2:
                ann_tmp = np.array(a[2:], dtype=float).reshape(-1, 5)
                ann_tmp[..., 4] *= 100
                self.ann.append((int(a[0]), int(a[1]), int(ann_raw[i+1].split()[1]), np.array(np.uint16(ann_tmp))))
            elif a:
                self.ann.append((int(a[0]), int(a[1]), int(ann_raw[i+1].split()[1]), []))
        self.frame_count = len(self.ann)
        self.vid_file = open(ann_filename[:-4]+".mjpeg", "rb")

        self.cur_pos = 0

    def get_frame(self, index=None):
        if index is None:
            index = self.cur_pos
            self.cur_pos += 1
        time, p, pend, dets = self.ann[index]
        self.vid_file.seek(p)
        im_b = self.vid_file.read(pend-p+4)
        im = cv2.imdecode(np.asarray(bytearray(im_b), dtype="uint8"), cv2.IMREAD_COLOR)
        return im
    
    def get_dets(self, index):
        time, p, pend, dets = self.ann[index]
        return dets
    
    def get_time(self, index):
        time, p, pend, dets = self.ann[index]
        return time
        

if __name__ == "__main__":
    rec = Record("25.txt")
    ann = rec.ann
    for i in range(rec.frame_count):
        im = rec.get_frame(i)
        dets = rec.get_dets(i)
        time = rec.get_time(i)
        
        cv2.putText(im, f"{(time//60000)%60}:{(time//1000)%60}", (20, 20), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.6, (0,255,0))
        for det in dets:
            x_min, y_min, x_max, y_max = np.int32(det[:-1])
            cv2.rectangle(im, (x_min, y_min), (x_max, y_max), (255, 0, 0))
        cv2.imshow("im", im)
        cv2.waitKey(1)
