import qrcode
import random
import string
import sqlite3
import datetime

def create():
    # DB에 테이블명으로 쓰기 위해 오늘 날짜를 불러옴
    now = datetime.datetime.now()

    # 현재 날짜와 그 다음 날짜를 지정
    nowDate = now.strftime("Y%Y%m%d")
    one = datetime.timedelta(days=1)
    nextDate = now + one
    nextDate_str = nextDate.strftime("Y%Y%m%d")
    nextDate_Hour_str = nextDate.strftime("Y%Y%m%d %H시:%M분")

    # 체크인 시간과 체크아웃 시간 결정
    nowTime = now.strftime(nowDate + " %H시:%M분")
    endTime = nextDate.strftime(nextDate_str + " 12시:00분")

    # 난수 생성
    randNum = str(random.randrange(111111111111111, 999999999999999))
    # 랜덤 알파벳 생성
    randomAlphabet = str(random.choice(string.ascii_letters)).upper()

    # 랜덤 알파벳 + 난수
    QR_str = randomAlphabet + randNum

    # 생성된 랜덤 문자열
    print(QR_str)

    # 문자열로 QR 코드 생성
    img = qrcode.make(QR_str)

    conn = sqlite3.connect('../Database/QRcode.sqlite3')  # DB 생성 or 이미 있으면 연걸
    cur = conn.cursor()  # 커서 생성

    # 생성된 이미지를 QRimage.png 로 저장
    img.save('../QR_Image/QRimage.png')

    conn.execute('CREATE TABLE IF NOT EXISTS ' + nowDate + '(check_in TEXT, check_out TEXT, code TEXT)')


    cur.executemany('INSERT INTO ' + nowDate + ' VALUES (?, ?, ?)', [(nowTime, endTime, QR_str)])

    # 테이블 내 데이터 갯수를 저장
    # conn.execute('CREATE INDEX idxName ON ' + nowDate + '(number DESC)')

    conn.commit()
    conn.close()