import cv2
import imutils
import pytesseract
import numpy as np

# Load the image
img = cv2.imread('C:/Users/Iftear/Desktop/Intelligence-traffic-monitoring-system-main/vehicle_number_by_its_plate/1.jpg', cv2.IMREAD_COLOR)

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 13, 15, 15)

# Detect edges
edged = cv2.Canny(gray, 30, 200)

# Find contours
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours1 = imutils.grab_contours(contours)
contours = sorted(contours1, key=cv2.contourArea, reverse=True)[:10]
screenCnt = None

# Iterate over contours
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
 
    if len(approx) == 4:
        screenCnt = approx
        break

# Check if contour detected
if screenCnt is None:
    detected = 0
    print("No contour detected")
else:
    detected = 1
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

# Mask the license plate region
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)

# Find the bounding box of the license plate
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx+1, topy:bottomy+1]

# Perform OCR on the cropped license plate
text = pytesseract.image_to_string(Cropped, config='--psm 11')
print("Detected license plate Number is:", text)

# Display the images
img = cv2.resize(img, (500, 300))
Cropped = cv2.resize(Cropped, (400, 200))
gray = cv2.resize(gray, (500, 300))
edged = cv2.resize(edged, (500, 300))
cv2.imshow('car', img)
cv2.imshow('Cropped', Cropped)
cv2.imshow('Image', gray)
cv2.imshow('thresholdImage', edged)

cv2.waitKey(0)
cv2.destroyAllWindows()
