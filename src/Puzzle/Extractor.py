from cv2 import cv2
import sys
import numpy as np
from Img.filters import *

def show_image(img, ind=None, name='image', show=True):
    plt.axis("off")
    plt.imshow(img)
    if show:
        plt.show()

def show_multiple_images(imgs):
    fig = plt.figure("Images")
    for i, img in enumerate(imgs):
        ax = fig.add_subplot(len(imgs), 1, i + 1)
        ax.set_title(str(i))
        show_image(img, show=False)
    plt.show()


class Extractor():
    def __init__(self, path, pixmapWidget=None):
        self.path = path
        self.img = cv2.imread(self.path, cv2.IMREAD_COLOR)
        self.img_bw = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        self.pixmapWidget = pixmapWidget

    def extract(self):
        kernel = np.ones((3, 3), np.uint8)
        # img = cv2.resize(initial_img, None, fx=0.5, fy=0.5)

        cv2.imwrite("/tmp/binarized.png", self.img_bw)
        if self.pixmapWidget is not None:
            self.pixmapWidget.add_image_widget("/tmp/binarized.png", 0, 0)

        # show_image(self.img_bw)
        # self.img_bw = cv2.cvtColor(self.img_bw, cv2.COLOR_RGB2GRAY)
        show_image(self.img_bw)

        def test_otsus():
            tmp = [100, 150, 200, 240, 255]
            imgs = []
            for i in tmp:
                ret, img_tmp = cv2.threshold(self.img_bw, 0, i, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                imgs.append(img_tmp)
            show_multiple_images(imgs)
            # ret, self.img_bw = cv2.threshold(self.img_bw, 240, 255, cv2.THRESH_BINARY_INV)
            cv2.imwrite("/tmp/binarized_treshold.png", self.img_bw)

        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
        # fgmask = fgbg.apply(self.img_bw)
        # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        def test_adapt_mog2():
            th3 = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                        cv2.THRESH_BINARY, 11, 2)

            ret, self.img_bw = cv2.threshold(self.img_bw, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            # ret, self.img_bw = cv2.threshold(self.img_bw, 240, 255, cv2.THRESH_BINARY_INV)

            fgbg = cv2.createBackgroundSubtractorMOG2()
            fgmask = fgbg.apply(self.img_bw)
            show_multiple_images([self.img_bw, fgmask, th3])

        def test_histogram():
            fig = plt.figure()

            # plot a 2D color histogram for green and blue
            ax = fig.add_subplot(131)
            hist = cv2.calcHist([self.img[:, :, 1], self.img[:, :, 0]], [0, 1], None,
                                [32, 32], [0, 256, 0, 256])
            p = ax.imshow(hist, interpolation="nearest")
            ax.set_title("2D Color Histogram for Green and Blue")
            plt.colorbar(p)

            # plot a 2D color histogram for green and red
            ax = fig.add_subplot(132)
            hist = cv2.calcHist([self.img[:, :, 1], self.img[:, :, 2]], [0, 1], None,
                                [32, 32], [0, 256, 0, 256])
            p = ax.imshow(hist, interpolation="nearest")
            ax.set_title("2D Color Histogram for Green and Red")
            plt.colorbar(p)

            # plot a 2D color histogram for blue and red
            ax = fig.add_subplot(133)
            hist = cv2.calcHist([self.img[:, :, 0], self.img[:, :, 2]], [0, 1], None,
                                [32, 32], [0, 256, 0, 256])
            p = ax.imshow(hist, interpolation="nearest")
            ax.set_title("2D Color Histogram for Blue and Red")
            plt.colorbar(p)
            plt.show()

        from skimage.filters import (threshold_otsu, threshold_niblack,
                                     threshold_sauvola)

        # window_size = 101
        # thresh_sauvola = threshold_sauvola(self.img, window_size=window_size)
        # binary_sauvola = self.img > thresh_sauvola
        # plt.subplot(2, 2, 4)
        # plt.imshow(binary_sauvola, cmap=plt.cm.gray)
        # plt.title('Sauvola Threshold')
        # plt.axis('off')
        # plt.show()

        # test_adapt_mog2()

        def test_adaptives():
            tmp1 = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                cv2.THRESH_BINARY, 25, 2)
            tmp2 = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                cv2.THRESH_BINARY, 25, 7)
            tmp3 = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                cv2.THRESH_BINARY, 25, 12)
            tmp4 = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                cv2.THRESH_BINARY, 51, 2)
            tmp5 = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                cv2.THRESH_BINARY, 51, 7)
            tmp6 = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                cv2.THRESH_BINARY, 51, 12)
            show_multiple_images([tmp1, tmp2, tmp3, tmp4, tmp5, tmp6])

        def apply_close():
            # Inversing colors : start of filling pieces
            self.img_bw = cv2.bitwise_not(self.img_bw)
            # filling holes in the pieces 2
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
            self.img_bw = cv2.morphologyEx(self.img_bw, cv2.MORPH_CLOSE, kernel)
            # Inversing colors back : end of filling pieces
            self.img_bw = cv2.bitwise_not(self.img_bw)

        def apply_small_close():
            # Inversing colors : start of filling pieces
            self.img_bw = cv2.bitwise_not(self.img_bw)
            # filling holes in the pieces 2
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            self.img_bw = cv2.morphologyEx(self.img_bw, cv2.MORPH_CLOSE, kernel)
            # Inversing colors back : end of filling pieces
            self.img_bw = cv2.bitwise_not(self.img_bw)

        def apply_open():
            # Inversing colors : start of filling pieces
            self.img_bw = cv2.bitwise_not(self.img_bw)
            # filling holes in the pieces 2
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            self.img_bw = cv2.morphologyEx(self.img_bw, cv2.MORPH_OPEN, kernel)
            # Inversing colors back : end of filling pieces
            self.img_bw = cv2.bitwise_not(self.img_bw)

        def fill_holes():
            # filling contours found (and thus potentially holes in pieces)
            _, contour, _ = cv2.findContours(self.img_bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contour:
                cv2.drawContours(self.img_bw, [cnt], 0, 255, -1)

        def fill_and_open():
            fill_holes()
            apply_close()

        # ret, self.img_bw = cv2.threshold(self.img_bw, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # ret, self.img_bw = cv2.threshold(self.img_bw, 240, 255, cv2.THRESH_BINARY_INV)
        # show_image(self.img_bw)

        def test_noise_otsu(splitOtsu=True, replace=False):
            morph = self.img.copy()
            for r in range(4):
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
                morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
                morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
            show_image(morph)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            mgrad = cv2.morphologyEx(morph, cv2.MORPH_GRADIENT, kernel)
            print('Morphology gradient')
            show_image(mgrad)
            self.img_bw = np.max(mgrad, axis=2)  # BGR 2 GRAY

            def f(x):
                if x < 5:
                    return 0
                else:
                    return 255

            f = np.vectorize(f)

            # self.img_bw = f(self.img_bw)
            # TODO: numperize this
            for i, tab in enumerate(self.img_bw):
                self.img_bw[i] = f(self.img_bw[i])
            #     for j, elt in enumerate(tab):
            #         if self.img_bw[i, j] < 5:
            #             self.img_bw[i, j] = 0
            #         else:
            #             self.img_bw[i, j] = 255

            # self.img_bw = np.apply_along_axis(lambda x: 255 if x > 0 else 0, 0, self.img_bw)
            show_image(self.img_bw)
            return
            if splitOtsu == True:
                ch = cv2.split(mgrad)
                _, ch[0] = cv2.threshold(ch[0], 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # COULD BE BETTER
                _, ch[1] = cv2.threshold(ch[1], 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                _, ch[2] = cv2.threshold(ch[2], 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                merged = cv2.merge(ch, 3)
                show_image(merged)
            else:
                mgrad = cv2.cvtColor(mgrad, cv2.COLOR_BGR2GRAY)
                _, mgrad = cv2.threshold(mgrad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                show_image(mgrad)
            if replace == True:
                # self.img_bw = cv2.bitwise_not(self.img_bw)
                # ret, tmp = cv2.threshold(mgrad, 240, 255, cv2.THRESH_BINARY_INV)
                # show_image(tmp)
                # self.img_bw = cv2.cvtColor(mgrad, cv2.COLOR_BGR2GRAY)
                mgrad = np.max(mgrad, axis=2) # BGR 2 GRAY
                self.img_bw = mgrad
                # self.img_bw = cv2.bitwise_not(self.img_bw)
                print('Finished noise otsu')


        test_noise_otsu(splitOtsu=True, replace=True)

        # self.img_bw = cv2.adaptiveThreshold(self.img_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
        #                              cv2.THRESH_BINARY, 11, 2)

        # FIXME: IS THIS OTSU USELESS?
        # _, self.img_bw = cv2.threshold(self.img_bw, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # self.img_bw = cv2.bitwise_not(self.img_bw)
        show_image(self.img_bw)
        fill_holes()
        show_image(self.img_bw)

        # apply_small_close()
        # show_image(self.img_bw)
        # apply_small_close()
        # show_image(self.img_bw)
        # apply_small_close()
        # show_image(self.img_bw)
        # apply_small_close()
        # show_image(self.img_bw)

        cv2.imwrite("/tmp/binarized_treshold_filled.png", self.img_bw)
        if self.pixmapWidget is not None:
            self.pixmapWidget.add_image_widget("/tmp/binarized_treshold.png", 1, 1)

        def cmp(a, b):
            return (a > b) - (a < b)
        # In case with fail to find the pieces, we fill some holes and then try again
        nb_error_max = 42
        # while True: # TODO Add this at the end of the project
        #     try:
        self.img_bw, contours, hier = cv2.findContours(self.img_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print('Found nb pieces: ' + str(len(contours)))

        nb_pieces = None
        if len(sys.argv) > 2:
            # Number of pieces specified by user
            nb_pieces = int(sys.argv[2])
            contours = sorted(np.array(contours), key=lambda x: x.shape[0], reverse=True)[:nb_pieces]
            print('Found nb pieces: ' + str(len(contours)))
        else:
            # Try to remove useless contours
            contours = sorted(np.array(contours), key=lambda x: x.shape[0], reverse=True)
            max = contours[1].shape[0]
            contours = np.array([elt for elt in contours if elt.shape[0] > max / 2])
            print('Found nb pieces: ' + str(len(contours)))

        whiteImg = np.zeros(self.img_bw.shape)
        cv2.drawContours(whiteImg, contours, -1, (255, 0, 0), 1, maxLevel=1)
        show_image(whiteImg)

        puzzle_pieces = export_contours(self.img, self.img_bw, contours, "/tmp/contours.png", 5)
        # break
        # except (IndexError):
        #     fill_holes()
        #     nb_error_max -= 1
        #     if nb_error_max <= 0:
        #         print('Could not find the pieces, exiting the app')
        #         sys.exit(1)
        #     print('Error while trying to find the pieces, trying again after filling some holes')
        if self.pixmapWidget is not None:
            self.pixmapWidget.add_image_widget("/tmp/contours.png", 0, 1)

        fshift, magnitude = get_fourier(self.img_bw)
        cv2.imwrite("/tmp/yolo.png", magnitude)
        if self.pixmapWidget is not None:
            self.pixmapWidget.add_image_widget("/tmp/yolo.png", 1, 0)

        rows, cols = self.img_bw.shape
        crow, ccol = int(rows / 2), int(cols / 2)
        fshift[crow - 30:crow + 30, ccol - 30:ccol + 30] = 0
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)

        cv2.imwrite("/tmp/yolo.png", img_back)
        return puzzle_pieces
