import numpy as np
import cv2 as ocv
import imutils


class ImageStitcher:

    def __init__(self):
        self.images = []
        self.stitcher = None
        self.stitched = None
        self.status = None

    def load_images(self, imagePaths):
        for imagePath in imagePaths:
            self.images.append(ocv.imread(imagePath))

    def stitch_images(self):
        self.stitcher = ocv.createStitcher(try_use_gpu=False)
        (self.status, self.stitched) = self.stitcher.stitch(self.images)
        return self.status

    def smooth_stitched_image(self):
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
        self.stitched = self.stitched[y:y + h, x:x + w]

