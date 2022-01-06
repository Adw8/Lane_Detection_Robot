import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def canny_edge_detector(image):
    # Convert the image color to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Reduce noise from the image
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def region_of_interest(image):
    height = image.shape[0]
    #polygons = np.array([[
        #(355, height),
        #(355,  height/2),
        #(1100 , height/2),
        #(1100, height),
    #]], np.int32)
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)

    # Fill poly-function deals with multiple polygon
    cv2.fillPoly(mask, polygons, 255)

    # Bitwise operation between canny image and mask image
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image
def create_coordinates(image, line_parameters):
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope,intercept=0.1,0
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        # It will fit the polynomial and the intercept and slope
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = create_coordinates(image, left_fit_average)
    right_line = create_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])
def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
        return line_image
def steering_angle2(image):
    lane_lines =[[[ 325 ,720 ,500, 432]],[[1010 , 720 , 660,  432]]]
    #lane_lines = [[[165, 480, 254, 240]], [[485, 480, 316, 240]]]
    height, width, _ = image.shape
    _, _, left_x2, _ = lane_lines[0][0]
    _, _, right_x2, _ = lane_lines[1][0]
    top = int((left_x2 + right_x2) / 2)
    mid = int(width/2)
    x_offset = top - mid
    y_offset = int(height/2)
    angle_radian = math.atan(x_offset / y_offset)
    angle_deg = int(angle_radian * 180.0 / math.pi)
    steering_angle = angle_deg + 90
    cv2.line(image, (mid, height), (int(top), y_offset), (0,0,255), 5)
    return image



# Path of dataset directory
cap = cv2.VideoCapture(r"C:\Users\Shlok\OneDrive\Desktop\lane detection\LaneD1.mp4")
while (cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny_edge_detector(frame)
    cropped_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100,
                            np.array([]), minLineLength=40,
                            maxLineGap=5)

    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    print(averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    #cv2.imshow("results", combo_image)
    steeringangle= steering_angle2( combo_image)
    cv2.imshow("Steering angle", steeringangle)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()


cv2.destroyAllWindows()



