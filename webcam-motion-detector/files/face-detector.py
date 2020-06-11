# DETECTS FACE(S) IN A PHOTO

import cv2


def resize_img(image, scale):
	"""takes cv2 image as first parameter and resizes in ratio according to the 2nd parameter"""
	resized = cv2.resize(image, tuple(int(dimention * scale) for dimention in reversed(image.shape[:2])))
	return resized


def grayscale_img(image):
	"""takes cv2 image and returns it in grayscale"""
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	return gray


def show_img(image_path, image):
	"""shows cv2 image"""
	cv2.imshow(image_path, image)
	cv2.waitKey(0)  #milliseconds
	cv2.destroyAllWindows()


if __name__ == '__main__':
	img_path = "files/news.jpg"
	img = cv2.imread(img_path)
	face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	faces = face_cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=5)

	for x, y, width, height in faces:
		edited_img = img
		# edited_img = grayscale_img(edited_img)
		edited_img = cv2.rectangle(edited_img, (x, y), (x + width, y + height), (0, 255, 0), 3)

	edited_img = resize_img(edited_img, 0.7)
	show_img("edited", edited_img)

