import cv2
import numpy as np

video = cv2.VideoCapture("video.mp4")

def region(image):
    height, width = image.shape
    triangle = np.array([[(50, height), (150, 300), (width - 150, 300), (width, height)]])
    mask = np.zeros_like(image)
    mask = cv2.fillPoly(mask, triangle, 255)
    mask = cv2.bitwise_and(image, mask)
    return mask

while True:
    ret, frame = video.read()
    if not ret:
        break
    scale_percent = 60  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    output = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    mask = region(edges)

    lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 30, minLineLength=50, maxLineGap=50)
    x_coords = []
    neg_slope_x = []
    pos_slope_x = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)
        if slope < 0:
            neg_slope_x.append(x1)
            neg_slope_x.append(x2)
        else:
            pos_slope_x.append(x1)
            pos_slope_x.append(x2)

    if len(neg_slope_x) > 0:
        avg_neg_slope_x = sum(neg_slope_x) / len(neg_slope_x)
        print("\nAverage x-coordinate of lines with negative slope:", avg_neg_slope_x)
    if len(pos_slope_x) > 0:
        avg_pos_slope_x = sum(pos_slope_x) / len(pos_slope_x)
        print("Average x-coordinate of lines with positive slope:", avg_pos_slope_x)
    if len(neg_slope_x) > 0 and len(pos_slope_x) > 0:
        avg_x = (avg_neg_slope_x + avg_pos_slope_x) / 2
        print("Average x-coordinate of both lanes:", avg_x)
        cv2.line(output, (int(avg_neg_slope_x), 480), (int(avg_neg_slope_x), 325), (0, 0, 255), thickness=5)
        cv2.line(output, (int(avg_pos_slope_x), 480), (int(avg_pos_slope_x), 325), (0, 0, 255), thickness=5)
        cv2.line(output, (int(avg_x), 480), (int(avg_x), 325), (0, 255, 0), thickness=5)

    cv2.imshow("Lanes", output)

    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
