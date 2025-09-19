import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('12.png')
k=5
blur = cv2.GaussianBlur(img,(k,k),0)
median = cv2.medianBlur(img,k)

plt.subplot(121),plt.imshow(median),plt.title('3x3')
plt.xticks([]),plt.yticks([])
plt.subplot(122),plt.imshow(blur),plt.title('5x5')
plt.xticks([]),plt.yticks([])
plt.show()