import cv2
import numpy as np

def nothing(x):
    pass

img = cv2.imread('1234.jpg')
img_backup = img.copy()

drawing = False
mode = True
ix, iy = -1, -1

mouse_x, mouse_y = 0, 0  # 마우스 좌표 저장용

# 도형 리스트: (mode, pt1, pt2)
shapes = []

def draw_all_shapes(image, shapes, alpha=0.4):
    overlay = image.copy()
    for m, pt1, pt2 in shapes:
        if m:
            cv2.rectangle(overlay, pt1, pt2, (0, 255, 0), -1)
        else:
            cv2.circle(overlay, pt2, 5, (0, 0, 255), -1)
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, mouse_x, mouse_y

    mouse_x, mouse_y = x, y  # 마우스 좌표 저장

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = img_backup.copy()
            overlay = temp_img.copy()

            if mode:
                cv2.rectangle(overlay, (ix, iy), (x, y), (0, 255, 0), -1)
            else:
                cv2.circle(overlay, (x, y), 5, (0, 0, 255), -1)

            alpha = 0.4
            cv2.addWeighted(overlay, alpha, temp_img, 1 - alpha, 0, temp_img)

            draw_all_shapes(temp_img, shapes, alpha)

            r = cv2.getTrackbarPos('R', 'image')

            # 픽셀 색상 가져오기
            if 0 <= mouse_y < img_backup.shape[0] and 0 <= mouse_x < img_backup.shape[1]:
                b, g, r_val = img_backup[mouse_y, mouse_x]
                color_str = f"({r_val},{g},{b})"
            else:
                color_str = "(0,0,0)"

            text = f"mouse position ({mouse_x},{mouse_y}) - {color_str} - {int(mode)} - {r}"
            cv2.putText(temp_img, text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow('image', temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            shapes.append((True, (ix, iy), (x, y)))
        else:
            shapes.append((False, (ix, iy), (x, y)))

cv2.namedWindow('image')
cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.setMouseCallback('image', draw_circle)

while True:
    temp_img = img_backup.copy()
    draw_all_shapes(temp_img, shapes, alpha=0.4)

    r = cv2.getTrackbarPos('R', 'image')

    if 0 <= mouse_y < img_backup.shape[0] and 0 <= mouse_x < img_backup.shape[1]:
        b, g, r_val = img_backup[mouse_y, mouse_x]
        color_str = f"({r_val},{g},{b})"
    else:
        color_str = "(0,0,0)"

    text = f"mouse position ({mouse_x},{mouse_y}) - {color_str} - {int(mode)} - {r}"
    cv2.putText(temp_img, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('image', temp_img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('m'):
        mode = not mode
    elif key == 27:
        break

cv2.destroyAllWindows()