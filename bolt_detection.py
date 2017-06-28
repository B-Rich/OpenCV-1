import cv2

img = cv2.imread("bolt_1.jpg")
cv2.imshow("Image", img)
if cv2.waitKey() == 27:
    cv2.destroyAllWindows()
    exit(0)

