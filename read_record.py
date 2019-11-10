import cv2
import numpy as np
from PIL import Image
import io

ann_raw = open("23.txt").read().split("T")
ann = []
for a in ann_raw:
    a = a.split()
    if len(a)>2:
        ann_tmp = np.array(a[2:], dtype=float).reshape(-1, 5)
        ann_tmp[..., 4] *= 100
        ann.append((int(a[0]), int(a[1]), np.array(np.uint16(ann_tmp))))
    elif a:
        ann.append((int(a[0]), int(a[1]), []))

f = open("23.mjpeg", "rb")

for i in range(len(ann) - 1):
    time, p, dets = ann[i]
    f.seek(p)
    im_b = f.read(ann[i+1][1]-p+4)
    im = cv2.imdecode(np.asarray(bytearray(im_b), dtype="uint8"), cv2.IMREAD_COLOR)
    cv2.putText(im, f"{(time//60000)%60}:{(time//1000)%60}", (20, 20), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.6, (0,255,0))
    for det in dets:
        x_min, y_min, x_max, y_max = np.int32(det[:-1])
        cv2.rectangle(im, (x_min, y_min), (x_max, y_max), (255, 0, 0))
    cv2.imshow("im", im)
    cv2.waitKey(1)
