# send_attachment.py
import os
import smtplib

from email import encoders
from email.utils import formataddr
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send(address):
    from_addr = formataddr(('QR코드 발신', '발신자 입력'))
    to_addr = formataddr(('QR코드 수신', address))

    session = None

    # SMTP 세션 생성
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.set_debuglevel(True)

    # SMTP 계정 인증 설정
    session.ehlo()
    session.starttls()
    session.login('로그인 이메일 입력', '로그인 비밀번호 입력')

    # 메일 콘텐츠 설정
    message = MIMEMultipart("mixed")

    # 메일 송/수신 옵션 설정

    message.set_charset('utf-8')
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = '[QR code]출입을 위한 QR코드입니다.'
    # 메일 콘텐츠 - 내용
    body = '''
    <h4>첨부된 QR코드를 카메라에 인식시켜 주십시오.</h4>
    '''
    bodyPart = MIMEText(body, 'html', 'utf-8')
    message.attach(bodyPart)

    # 메일 콘텐츠 - 첨부파일
    attachments = [
        os.path.join(os.getcwd(), '../QR_Image', 'QRimage.png')
    ]

    for attachment in attachments:
        attach_binary = MIMEBase("application", "octect-stream")

        binary = open(attachment, "rb").read()  # read file to bytes

        attach_binary.set_payload(binary)
        encoders.encode_base64(attach_binary)  # Content-Transfer-Encoding: base64

        filename = os.path.basename(attachment)
        attach_binary.add_header("Content-Disposition", 'attachment', filename=('utf-8', '', filename))

        message.attach(attach_binary)
    # 메일 발송
    session.sendmail(from_addr, to_addr, message.as_string())