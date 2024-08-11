import RPi.GPIO as GPIO
import time

import socket
import threading

buzzer_port = 15
led_port = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_port, GPIO.OUT)
GPIO.setup(led_port, GPIO.OUT)

class SOCK:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Socket
        self.Host = 'SERVER_IP_ADDRESS'  # 서버의 IP 주소
        self.Port = 9000  # 서버의 Port 주소

    def Recv(self, conn, addr):
        while True:
            recv_data = conn.recv(1024).decode()  # Server -> Client 데이터 수신
            print(recv_data)
            if recv_data == 'detect':
                self.BUZZER()
                self.LED('on')
            elif recv_data == 'end':
                self.LED('off')

    def Handle_sock(self):
        self.server_sock.bind((self.Host, self.Port))
        self.server_sock.listen(1)
        conn, addr = self.server_sock.accept()
        print('connect!!')
        # Thread for receiving server message
        t = threading.Thread(target=self.Recv, args=(conn, addr, ))
        t.start()

    def BUZZER(self):
        pwm = GPIO.PWM(buzzer_port, 1.0)
        pwm.start(50.0)

        for _ in range(5):
            pwm.ChangeFrequency(440) # Repeating 'la'
            time.sleep(1.0)
        pwm.stop()

    def LED(self, run_type):
        if run_type == 'on':
            GPIO.output(led_port, True)
        if run_type == 'off':
            GPIO.output(led_port, False)

#TCP Client
if __name__ == '__main__':
    sock = SOCK()
    sock.Handle_sock()
