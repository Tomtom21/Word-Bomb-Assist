import cv2
import easyocr
import numpy as np
import sys
import mss
import mss.tools
import time
import os
import nltk
from nltk.corpus import words
from wordfreq import zipf_frequency

# Loading the word list
word_list = words.words()

DEBUG = '--debug' in sys.argv
reader = easyocr.Reader(['en'])

def filter_boxed_letter_color(img):
    # Convert hex 8e95ac to BGR: (172, 149, 142)
    lower = np.array([162, 139, 132], dtype=np.uint8)
    upper = np.array([182, 159, 152], dtype=np.uint8)
    mask = cv2.inRange(img, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxed_imgs = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 20 and h > 20:
            boxed_imgs.append(img[y:y+h, x:x+w])
    return boxed_imgs

def preprocess_for_boxed_letters(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    upscaled = cv2.resize(gray, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)
    blur = cv2.blur(upscaled, (6, 6))
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(blur)
    _, thresh = cv2.threshold(enhanced, 120, 255, cv2.THRESH_BINARY)
    inverted = cv2.bitwise_not(thresh)
    return inverted

def main():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        print("Screen capture started. Press 'q' to quit.")
        while True:
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            if frame.shape[2] == 4:
                frame = frame[:, :, :3]
            boxed_imgs = filter_boxed_letter_color(frame)
            detected_letters = ''
            for boxed_img in boxed_imgs:
                preprocessed_box = preprocess_for_boxed_letters(boxed_img)
                box_result = reader.readtext(preprocessed_box, detail=0, text_threshold=0.3)
                detected_letters += ''.join([w.lower() for w in box_result if len(w) == 1 and (w.isalpha() or w == '0')])
                detected_letters = detected_letters.replace('0', 'o')

            os.system('cls || clear')
            if detected_letters:
                # print(f"Detected boxed letters: {detected_letters[::-1]}")
                # print(detected_letters)
                seq = detected_letters[::-1]
                result = [w for w in word_list if seq in w and 4 <= len(w) <= 7]
                filtered = [
                    w for w in result
                    if seq in w and zipf_frequency(w, "en") >= 3.0
                ]
                # for w in result[:50]:
                #     print(w)
                print(filtered[:50])
            if DEBUG:
                for i, boxed_img in enumerate(boxed_imgs):
                    preprocessed_box = preprocess_for_boxed_letters(boxed_img)
                    cv2.imshow(f'Debug - Boxed Region {i}', preprocessed_box)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.3)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

