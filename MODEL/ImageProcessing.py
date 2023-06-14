import cv2


class imageProcessing:

    def  __init__(image):
        cv2.resize(image, (256, 256))
        gray_face, colored_face, marker = imageProcessing.faceSegmentor(image)
        if marker == 1:
            eye_color_rank = 0
            face_color_rank = imageProcessing.faceColorRank(imageProcessing.faceColorExtractor(image))
        else :
            eye_segmented , eye_marker= imageProcessing.eyeSegmentor(gray_face, colored_face)
            if eye_marker == 1 :
                eye_color_rank = 0
                face_color_rank = imageProcessing.faceColorRank(imageProcessing.faceColorExtractor(colored_face)) 
            else :   
                eye_colored = imageProcessing.eyeColorExtractor(eye_segmented)
                eye_color_rank = imageProcessing.eyeColorRank(eye_colored)
                remover_eye_image = imageProcessing.faceEyeRemoval(colored_face)
                face_color_rank = imageProcessing.faceColorRank(imageProcessing.faceColorExtractor(remover_eye_image))
        return (eye_color_rank, face_color_rank)

    def eyeCaller():
        c_eye = cv2.CascadeClassifier('Data/Classifiers/cascade_eye.xml')
        return (c_eye)

    def faceCaller():
        c_face = cv2.CascadeClassifier('Data/Classifiers/cascade_frontalface_d.xml')
        return (c_face)

    def faceSegmentor(image):
        """
        :param image:
        """
        classifier_face = imageProcessing.faceCaller()
        y = 0
        h = 0
        while True:
            gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rec_face = classifier_face.detectMultiScale(gray_im)
            for (x, y, w, h) in rec_face:
                face_g = gray_im[y:y + h, x:x + w]
                face_c = image[y:y + h, x:x + w]
            break
        mark = 0
        if y & h == 0: 
            face_g = [0]
            face_c = [0]
            mark = 1
        return (face_g, face_c, mark)    

    def faceEyeRemoval(face_image):
        classifier_eye = imageProcessing.eyeCaller()
        rec_eye = classifier_eye.detectMultiScale(face_image)
        for (ex, ey, ew, eh) in rec_eye:
            face_Min_eye = cv2.rectangle(face_image, (ex, ey), (ex + ew, ey + eh), (0, 0, 0), -1)
        return (face_Min_eye)

    def eyeSegmentor(face_gray, face_c):
        classifier_eye = imageProcessing.eyeCaller()
        rec_eye = classifier_eye.detectMultiScale(face_gray)
        ey = 0
        eh = 0
        for (ex, ey, ew, eh) in rec_eye:
                eye = face_c[ey:ey + eh, ex:ex + ew]
        mark = 0        
        if ey & eh == 0:
            eye = [0]
            mark = 1
        return (eye, mark)

    def faceColorExtractor(im_f):
        gray_im_f = cv2.cvtColor(im_f, cv2.COLOR_BGR2GRAY)
        th3 = cv2.adaptiveThreshold(gray_im_f, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
        ret, face_m1 = cv2.threshold(gray_im_f, 170, 255, cv2.THRESH_BINARY)
        ret, face_m2 = cv2.threshold(gray_im_f, 120, 255, cv2.THRESH_BINARY)
        face_m3 = cv2.bitwise_and(th3, face_m1)
        face_mask = cv2.bitwise_xor(face_m2, face_m3)
        face_co = cv2.bitwise_and(im_f, im_f, mask=face_mask)
        return (face_co)

    def eyeColorExtractor(im_e):
        gray_im_e = cv2.cvtColor(im_e, cv2.COLOR_BGR2GRAY)
        th3 = cv2.adaptiveThreshold(gray_im_e, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, -8)
        eye_co = cv2.bitwise_and(im_e, im_e, mask=th3)
        return (eye_co)

    def faceColorRank(face_image):
        sum = 0
        counter = 0
        for i in range(face_image.shape[0]):
            for j in range(face_image.shape[1]):
                greenpixel = face_image.item(i, j, 1)
                redpixel = face_image.item(i, j, 2)
                if greenpixel > 100:
                    if redpixel > 100:
                        sum = sum + greenpixel + redpixel
                        counter = counter + 1
        if counter != 0:                
            color_rank = sum / counter
            return (color_rank)
        else : return(0)

    def eyeColorRank(eye_image):
        sum = 0
        counter = 0
        for i in range(eye_image.shape[0]):
            for j in range(eye_image.shape[1]):
                greenpixel = eye_image.item(i, j, 1)
                redpixel = eye_image.item(i, j, 2)
                if greenpixel > 150 :
                    if redpixel > 150 :
                        sum = sum + greenpixel + redpixel
                        counter = counter + 1
        if counter != 0:                
            color_rank = sum / counter
            return (color_rank)
        else : return(0)