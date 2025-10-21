#Importing all the needed files
import cv2 as cv   #OpenCV2
from mediapipe.python.solutions import drawing_utils, holistic   #MediaPipe
from pynput.keyboard import Controller, Key   #Keyboard controler and keys

cam = cv.VideoCapture(0)   #Reading the webcam
draw = drawing_utils   #Hỗ trợ vẽ các tọa độ được xác định bởi mediapipe 
keyboard = Controller()   #Keyboard controller

#Our program engine starts here
with holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5) as holi:   # Tạo một mô hình Holistic của MediaPipe để phát hiện và theo dõi tay, mặt, cơ thể
    while True:
        ret,frame = cam.read()   #đọc hình ảnh từ webcam

        img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)   #Chuyển đổi định dạng màu từ BGR sang RGB
        results = holi.process(img)   #Gửi hình ảnh cho mediapipe xử lý

        #Vẽ các tọa độ của bàn tay phải và bàn tay trái
        draw.draw_landmarks(img,results.right_hand_landmarks,holistic.HAND_CONNECTIONS)
        draw.draw_landmarks(img,results.left_hand_landmarks,holistic.HAND_CONNECTIONS)

        #Nếu bàn tay không xuất hiện trong khung hình, khả năng lỗi
        try:

            #Lấy tất cả các điểm tọa độ từ cả hai bàn tay
            RightLandmarks = results.right_hand_landmarks.landmark
            LeftLandmarks = results.left_hand_landmarks.landmark

            #Kiếm tra bàn tay phải đang nắm hay không
            if RightLandmarks[8].y > RightLandmarks[7].y and RightLandmarks[12].y > RightLandmarks[11].y and RightLandmarks[16].y > RightLandmarks[15].y and RightLandmarks[20].y > RightLandmarks[19].y:
                
                #Writting text on the screen
                cv.putText(img,'Right',(10,400), cv.FONT_HERSHEY_COMPLEX, 1,(255,0,127),2)
                
                #Nhấn phím mũi tên phải
                keyboard.release(Key.left)
                keyboard.press(Key.right)
                
            #Kiếm tra bàn tay trái đang nắm hay không
            elif LeftLandmarks[8].y > LeftLandmarks[7].y and LeftLandmarks[12].y > LeftLandmarks[11].y and LeftLandmarks[16].y > LeftLandmarks[15].y and LeftLandmarks[20].y > RightLandmarks[19].y:
                
                #Writting text on the screen
                cv.putText(img,'Left',(550,400), cv.FONT_HERSHEY_COMPLEX, 1,(255,0,127),2)

                #Nhấn phím mũi tên trái
                keyboard.release(Key.right)
                keyboard.press(Key.left)

            else:
                #Thả cả hai phím nếu không nắm tay
                keyboard.release(Key.right)
                keyboard.release(Key.left)
                
        except:

            #Nếu không phát hiện bàn tay, thả cả hai phím
            keyboard.release(Key.right)
            keyboard.release(Key.left)

        #Chuyển đổi định dạng màu trở lại BGR để hiển thị đúng với OpenCV
        img = cv.cvtColor(img,cv.COLOR_RGB2BGR)

        #Hiển thị hình ảnh
        cv.imshow('CountFingure',img)

        #Wait for 1ms 
        key = cv.waitKey(1)

        #Kiểm tra nếu phím q được nhấn để thoát khỏi vòng lặp
        if key == ord('q'):
            break


cam.release()   #Tắt webcam
cv.destroyAllWindows()  #Đóng tất cả cửa sổ OpenCV