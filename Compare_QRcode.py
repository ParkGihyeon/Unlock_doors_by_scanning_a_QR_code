import sqlite3
import datetime

def compare(code):
    conn = sqlite3.connect('../Database/QRcode.sqlite3')
    cur = conn.cursor()  # 커서 생성
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    past_db_table = cur.fetchall()
    past_db_table_name = [x[0] for x in past_db_table]


    cur.execute("SELECT * FROM " + past_db_table_name[-1])
    past_db_table_contents = cur.fetchall()

    if code == past_db_table_contents[-1][2]:
        return 1 #이 경우에 문을 열어주면 된다.
    else:
        return 0 #문을 열지 않음


def get_code_and_date():
    conn = sqlite3.connect('../Database/QRcode.sqlite3')
    cur = conn.cursor()  # 커서 생성
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    past_db_table = cur.fetchall()
    past_db_table_name = [x[0] for x in past_db_table]

    cur.execute("SELECT * FROM " + past_db_table_name[-1])
    past_db_table_contents = cur.fetchall()

    return past_db_table_contents[-1][2], past_db_table_contents[-1][1]  # 마지막 QR코드와 생성날짜 반환


def judge_today(date):
    #전달받는 date의 형식은 Y20210603 12시:00분

    #print(Mystr[0:9])  # Y날짜
    #print(Mystr[10:12]) # 시간

    now = datetime.datetime.now()
    nowHour = now.strftime("%H")
    today_str = now.strftime("Y%Y%m%d")


    if date[0:9] == today_str:  # 마감날짜 == 현재날짜
        if date[10:12] >= nowHour:
            return 1  # 퇴실시간 이전
        else:
            return 0  # 퇴실시간 이후

    elif date[1:9] > today_str[1:]:  # 퇴실날짜 전날일 경우
        return 1

    else:
        return 0


def judge_admin(code):
    if '@' in code:
        print("어드민 QR코드입니다.")
        return 1
    else:
        return 0
