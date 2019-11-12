import numpy as np
import cv2 as ocv
import imutils

"""
   written and completed by major-phyo-san on 12th November, 2019

   Python OpenCV version 3.4.2.16
   PyQt5 version 5.13.0
   Imutils version 0.5.3
   
   Image stiching and cropping logics are based on an article at 
   https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/
   Image resizing logic is based on a tutorial at
   https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
   Test images are used from
   https://github.com/kushalvyas/Python-Multiple-Image-Stitching/tree/master/images   
"""


class ImageStitcher:

    def __init__(self):
        self.images = []
        self.stitcher = None
        self.stitched = None
        self.cropped_stitched = None
        self.status = None

    def load_images(self, imagePaths):
        i = 1
        for imagePath in imagePaths:
            self.images.append(ocv.imread(imagePath))
            imgIndx = i - 1
            self.images[imgIndx] = self.width_height_corrector(self.images[imgIndx])
            ocv.imshow("image"+str(i), self.images[imgIndx])
            ocv.waitKey(0)
            ocv.destroyAllWindows()
            i = i + 1

    def width_height_corrector(self, image):
        widthLimit = 900
        heightLimit = 570
        if image.shape[1] > widthLimit and image.shape[0] < heightLimit: #shape 1 is width
            width = widthLimit
            height = image.shape[0]
            dim = (width, height)
            resized = ocv.resize(image, dim, interpolation=ocv.INTER_AREA)

        elif image.shape[1] < widthLimit and image.shape[0] > heightLimit: #shape 0 is height
            width = image.shape[1]
            height = heightLimit
            dim = (width, height)
            resized = ocv.resize(image, dim, interpolation=ocv.INTER_AREA)

        elif image.shape[1] > widthLimit and image.shape[0] > heightLimit:
            width = widthLimit
            height = heightLimit
            dim = (width, height)
            resized = ocv.resize(image, dim, interpolation=ocv.INTER_AREA)

        else:
            resized = image

        return resized

    def stitch_images(self):
        print("Stitching images, please wait....")
        self.stitcher = ocv.createStitcher(try_use_gpu=False)
        (self.status, self.stitched) = self.stitcher.stitch(self.images)
        self.images = []
        if self.status == 0:
            print("Image stitching completed")
            ocv.imshow("stitched image", self.stitched)
            ocv.waitKey(0)
            ocv.destroyAllWindows()
        else:
            print("Cannot stitch images. "+" Error code " + str(self.status))


    def smooth_stitched_image(self):
        print("Smoothing output image, please wait....")
        self.stitched = ocv.copyMakeBorder(self.stitched, 10,10,10,10, ocv.BORDER_CONSTANT, (0,0,0))
        gray = ocv.cvtColor(self.stitched, ocv.COLOR_BGR2GRAY)
        thresh = ocv.threshold(gray, 0, 255, ocv.THRESH_BINARY)[1]

        cnts = ocv.findContours(thresh.copy(), ocv.RETR_EXTERNAL, ocv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        c = max(cnts, key=ocv.contourArea)
        mask = np.zeros(thresh.shape, dtype="uint8")
        (x, y, w, h) = ocv.boundingRect(c)

        ocv.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        minRect = mask.copy()
        sub = mask.copy()

        while ocv.countNonZero(sub) > 0:
            minRect = ocv.erode(minRect, None)
            sub = ocv.subtract(minRect, thresh)

        cnts = ocv.findContours(minRect.copy(), ocv.RETR_EXTERNAL, ocv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        c = max(cnts, key=ocv.contourArea)
        (x, y, w, h) = ocv.boundingRect(c)
        self.cropped_stitched = self.stitched[y:y + h, x:x + w]
        self.stitched = None
        ocv.imshow("output image",self.cropped_stitched)
        ocv.waitKey(0)
        ocv.destroyAllWindows()

    def save_output_image(self,fileName,saveDir):       
       ocv.imwrite(saveDir+ "/" +fileName + "_output_stitched_image.jpg",self.cropped_stitched)
       print("Output image saved")
       self.cropped_stitched = None 

     