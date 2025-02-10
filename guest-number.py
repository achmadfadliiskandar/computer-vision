import cv2
import random

vidio = cv2.VideoCapture(0)

data_gambar = ['images/satu.jpeg','images/dua.jpeg','images/tiga.jpeg','images/empat.jpeg','images/lima.jpeg']
# data = [5,2,10,4,1]
gambar_random = cv2.imread(random.choice(data_gambar))

while True:
    ret,frame = vidio.read()
    if not ret:
        break

    frame = cv2.flip(frame , 1)
    ukuran_gambar = cv2.resize(gambar_random,(200,100))
    tinggi,lebar,_ = gambar_random.shape

    y_offset,x_offset = 10,frame.shape[1] -210
    frame[y_offset:y_offset + 100,x_offset:x_offset + 200] = ukuran_gambar

    cv2.imshow("Tebak Angka 1-10",frame)
    if cv2.waitKey(1) ==  ord('x'):
        break

vidio.release()
cv2.destroyAllWindows()