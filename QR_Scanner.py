import RPi.GPIO as GPIO
import cv2
import Compare_QRcode
import Door_Mortor
import LED
import time
import QR_Create
import Send_QR


def start():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(19, GPIO.IN)

    #DB에 저장된 코드를 불러옴
    code, date = Compare_QRcode.get_code_and_date()

    # 카메라 객체
    cap = cv2.VideoCapture(0)

    LED.compare_start()

    # QR코드 인식 객체
    detector = cv2.QRCodeDetector()

    end = False

    while True:
        # 카메라의 이미지를 읽음
        _, img = cap.read()
        # 박스 영역의 좌표 및 데이터 가져오기
        data, bbox, _ = detector.detectAndDecode(img)

        # 박스 영역이 있다면 데이터가 속한 박스 영역을 그림
        if (bbox is not None):
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255,
                                                                                             0, 255), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)


            if data:
                if Compare_QRcode.judge_admin(data) == 1:
                    QR_Create.create()
                    Send_QR.send(data)
                    LED.compare_true()
                    end = True

                else:
                    if code == data and Compare_QRcode.judge_today(date) == 0:
                        print("만료된 코드입니다:", data)
                        LED.compare_false()
                        end = True

                    elif code == data:
                        print("코드가 같습니다:", data)
                        LED.compare_true()
                        Door_Mortor.mortor()
                        end = True

                    else:
                        print("다른 코드입니다:", data)
                        LED.compare_false()
                        end = True

        # 영상 미리보기를 표시
        cv2.imshow("code detector", img)

        if GPIO.input(19) == 0:
            LED.compare_end()
            end = True
            time.sleep(1)

        if (cv2.waitKey(1) == ord("q") or end == True):
            break
    # 카메라 객체를 해제하고 종료
    cap.release()
    cv2.destroyAllWindows()