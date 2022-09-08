import cv2
import matplotlib.pyplot as pic

'''py
    Original Image Setup
'''

# seaborn matplotlib styling
pic.style.use('seaborn-darkgrid')

# read image from cv2
img = cv2.imread("girl.png")

# Set the image to default RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# image resizing
pic.figure(figsize=(5, 5))
pic.imshow(img)

# skip the graph axis hover in image
pic.axis("off")

# image title
pic.title("Original Image")
pic.show()

'''
    Converting Image to GrayScale to decrease the image complexity
'''

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pic.figure(figsize=(5, 5))
pic.imshow(gray_img, cmap="gray")
pic.axis("off")
pic.title("GrayScale Image")
pic.show()

'''
    Inverting the image to study image precision
'''

img_invert = cv2.bitwise_not(gray_img)
pic.figure(figsize=(5, 5))
pic.imshow(img_invert, cmap="gray")
pic.axis("off")
pic.title("Inverted Image")
pic.show()

'''
    Image smoothing
'''

img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
pic.figure(figsize=(5, 5))
pic.imshow(img_smoothing, cmap="gray")
pic.axis("off")
pic.title("Smoothen Image")
pic.show()

'''
    Image Finalization
'''

final_image = cv2.divide(gray_img, 255 - img_smoothing, scale=255)
pic.figure(figsize=(8, 8))
pic.imshow(final_image, cmap="gray")
pic.axis("off")
pic.title("Final Sketch Image")
pic.show()

pic.figure(figsize=(20, 20))
pic.figure('Py-Sketch')
pic.subplot(1, 5, 1)
pic.imshow(img)
pic.axis("off")
pic.title("Original Image")
pic.subplot(1, 5, 2)
pic.imshow(gray_img, cmap="gray")
pic.axis("off")
pic.title("GrayScale Image")
pic.subplot(1, 5, 3)
pic.imshow(img_invert, cmap="gray")
pic.axis("off")
pic.title("Inverted Image")
pic.subplot(1, 5, 4)
pic.imshow(img_smoothing, cmap="gray")
pic.axis("off")
pic.title("Smoothen Image")
pic.subplot(1, 5, 5)
pic.imshow(final_image, cmap="gray")
pic.axis("off")
pic.title("Final Sketch Image")

mng = pic.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
pic.show()


