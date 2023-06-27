from matplotlib import pyplot as plt
import cv2
import os 
path="{}/verify.jpg".format(os.getcwd())

def get_offset():
    image=cv2.imread(path)
    image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Converting BGR to RGB
    # plt.imshow(image)
    # plt.show()

    canny=cv2.Canny(image,300,300)
    # plt.imshow(canny)
    # plt.show()

    contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  
    dx, dy = 0, 0
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if (100 > w > 45) and (100 >  h > 45):
            dx = x
            dy = y
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
    # plt.imshow(image)
    # plt.show()
    print(dx,dy)
    
    return dx

if __name__ == "__main__":
    get_offset()
