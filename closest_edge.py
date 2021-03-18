import cv2
import numpy as np
import math
import sys
from urllib.request import urlopen
from distances import *

req = urlopen('https://datacarpentry.org/image-processing/fig/07-junk.jpg')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img_rgb = cv2.imdecode(arr, -1)  # 'Load it as it is'
img = cv2.cvtColor(img_rgb.copy(), cv2.COLOR_BGR2GRAY)

edged = cv2.Canny(img.copy(), 110, 200)
edged = cv2.dilate(edged, None, iterations=2)
edged = cv2.erode(edged, None, iterations=2)
cv2.imwrite('edge_detected.png', edged)

contours, _ = cv2.findContours(edged, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
contours = [cnt for cnt in contours if cnt.shape[0] > 100]


def dist_old(p1, p2, p3):
    return (np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1))


rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 50  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on


lines = cv2.HoughLinesP(edged, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)


pixel = (1500, 1000)
min_dist = sys.maxsize + 1

img_point = cv2.circle(img_rgb.copy(), pixel, radius=5,
                       color=(0, 0, 255), thickness=-8)
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(img_point, (x1, y1), (x2, y2), (255, 0, 0), 5)
        p1 = np.asarray((x1, y1))
        p2 = np.asarray((x2, y2))
        p3 = np.asarray(pixel)
        d2 = dist_old(p1, p2, p3)
        d = pnt2line(pixel, p1, p2)
        if d < min_dist:
            min_dist = d
            reqd_line = [x1, y1, x2, y2]

        elif d == min_dist:
            curr_len = (x1-x2)**2 + (y1-y2)**2
            min_len = (reqd_line[0] - reqd_line[2])**2+(reqd_line[1] - reqd_line[3])**2
            if curr_len >= min_len:
                reqd_line = [x1, y1, x2, y2]
cv2.imwrite('line_image.jpg', img_point)


img_point = cv2.circle(img_rgb.copy(), pixel, radius=5,
                       color=(0, 0, 255), thickness=-8)

cv2.line(img_point, (reqd_line[0], reqd_line[1]),
         (reqd_line[2], reqd_line[3]), (255, 0, 0), 5)

cv2.imwrite('final.jpg', img_point)
