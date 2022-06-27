import cv2
import numpy as np
from PIL import Image




def converter(reading_path, filename, saving_path):
  path = reading_path
  img = cv2.imread(path + filename)
  img = cv2.resize(img, (400,400))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  copy = img.copy()
  copy = cv2.cvtColor(copy, cv2.COLOR_RGB2GRAY)
  blurred = cv2.GaussianBlur(copy,(5,5), 0)
  thresh = cv2.threshold(blurred, 18, 255, cv2.THRESH_BINARY)[1]
  contour = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contour = contour[0][0]
  contour = contour[:,0,:]
  x1 = tuple(contour[contour[:,0].argmin()])[0]
  y1 = tuple(contour[contour[:,1].argmin()])[1]
  x2 = tuple(contour[contour[:,0].argmax()])[0]
  y2 = tuple(contour[contour[:,1].argmax()])[1]
  x = int(x2-x1)*4//100
  y = int(y2-y1)*5//100
  copy_2 = img.copy()
  if x2-x1 > 100 and y2-y1 > 100:
    copy_2 = copy_2[y1+y:y2-y, x1+x:x2-x]
    copy_2 = cv2.resize(copy_2, (400,400))
  lab = cv2.cvtColor(copy_2, cv2.COLOR_RGB2LAB)
  l, a, b = cv2.split(lab)
  clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=((8,8)))
  cl = clahe.apply(l)
  l_img = cv2.merge((cl, a, b))
  last = cv2.cvtColor(l_img, cv2.COLOR_LAB2RGB)
  med_last = cv2.medianBlur(last, 3)
  background = cv2.medianBlur(last, 37)
  mask = cv2.addWeighted(med_last,1, background,-1,255)
  final_img_for_img = cv2.bitwise_and(mask, med_last)
  im = Image.fromarray(final_img_for_img)
  im.save(saving_path + filename)
  final_img_for_pre = np.expand_dims(final_img_for_img, axis=0)
  return [final_img_for_img, final_img_for_pre, im]



