import RPi.GPIO as GPIO
import time

import socket
import threading

SERVO_MAX_DUTY    = 12
SERVO_MIN_DUTY    = 3

class SOCK:
    def __init__(self):
        self.keypad_out_port = [2, 3, 4, 17]
        self.keypad_in_port = [17, 27, 22]
        self.password = "0000"
        self.input_key = ""
        self.input_change = 0

        self.led_port = 18
        self.servo_port = 12
        
        self.is_detect = 0   

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Socket
        self.Host = 'SERVER_IP_ADDRESS'  # Server IP address
        self.Port = 9000  # Server Port number
	    self.init_port()

    def init_port():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_port, GPIO.OUT)
        GPIO.setup(self.servo_port, GPIO.OUT)
        self.servo = GPIO.PWM(self.servo_port, 50)
        self.servo.start(0)

        for i in range(4):
            GPIO.setup(self.keypad_in_port[i], GPIO.IN)
            GPIO.setup(self.keypad_out_port[i], GPIO.OUT)


    def Recv(self, conn, addr):
        while True:
            recv_data = conn.recv(1024).decode()  # Server -> Client data receiving
            print(recv_data)
            if recv_data == 'detect':
                self.LED('on')
                self.is_detect = 1
            elif recv_data == 'end':
                self.LED('off')
                self.is_detect = 0

    def Handle_sock(self):
        self.server_sock.bind((self.Host, self.Port))
        self.server_sock.listen(1)
        conn, addr = self.server_sock.accept()
        print('connect!!')
        # Thread for receiving server message
        t_recv = threading.Thread(target=self.Recv, args=(conn, addr, ))
        t_recv.start()
        t_doorlock = threading.Thread(target=self.Doorlock, args=())
        t_doorlock.start()

    def Doorlock(self):
        input_pw = keypad_input()
        if input_pw == self.password:
            self.MOTOR()
    
    def change_pw(self):
        new_pw = keypad_input()
        if len(new_pw) > 0:
            self.password = new_pw

    def keypad_input(is_change):
        while True:
            if self.is_detect == 0:
                for i in range(4):
                    GPIO.output(self.keypad_out_port[i], True)

                    for j in range(3):
                        while GPIO.input(self.keypad_in_port[j]) :
                            self.input_change = i * 3 + (j + 1)
                
                if 0 < self.input_change <= 9 :
                    self.input_key += str(self.input_change)
                elif self.input_change == 10:
                    return self.input_key
                elif self.input_change == 11:
                    self.input_key += '0'
                elif self.input_change == 12:
                    self.change_pw()

    def MOTOR(self):
        duty = SERVO_MIN_DUTY+(90*(9/180.0))
        self.servo.ChangeDutyCycle(duty)

        time.sleep(5)

        self.servo.ChangeDutyCycle(SERVO_MIN_DUTY)

    def LED(self, run_type):
        if run_type == 'on':
            GPIO.output(led_port, True)
        if run_type == 'off':
            GPIO.output(led_port, False)

#TCP Client
if __name__ == '__main__':
    sock = SOCK()
    sock.Handle_sock()
