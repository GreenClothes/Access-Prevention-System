import threading

import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *

# from face_detection_pyqt5 import run
import face_detection_pyqt5
from person_db import PersonDB

import socket
from _thread import *

from queue import Queue
import numpy as np

import time

PORT = 9000  # the port number for socket communication

class FRAME(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # update frame on PyQt GUI
        # print('i am frame thread')
        while 1:
            try:
                for i in range(6):
                    if self.parent.cctv_ip_num > i:
                        ret, self.parent.frame[i] = self.parent.video_capture[i].read()
                        self.parent.detect.get_frame(self.parent.frame)
                        if ret:
                            frame_rgb = cv2.cvtColor(self.parent.frame[i], cv2.COLOR_BGR2RGB)
                            image = QImage(
                                frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888
                            )
                            pixmap = QPixmap.fromImage(image)

                            self.parent.image[i].setPixmap(pixmap.scaled(
                                self.parent.image[i].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                            ))
                        else:
                            # Once the connection is disconnected, reassign and checking that the frame is read
                            self.video_capture = [cv2.VideoCapture(self.parent.cctv_ip_addresses[0])]
                            ret, self.parent.frame[i] = self.parent.video_capture[0].read()
                            if not ret:
                                self.parent.cctv_ip_num -= 1
                                self.parent.cctv_flg[i] = 1
                    elif self.parent.cctv_flg[i]:
                        pixmap = QPixmap('image/none.png')

                        self.parent.image[i].resize(500, 500)

                        self.parent.image[i].setPixmap(pixmap.scaled(
                            self.parent.image[i].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                        ))
                        self.parent.cctv_flg[i] = 0
                time.sleep(0.03)
            except Exception as e:
                print("ERROR OCCUR", e)

    def get_info(self, parent):
        # 수정
        self.parent = parent

class DETECTION(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.frame = []
        self.pdb = PersonDB()
        self.pdb.load_db('students')
        self.cctv_ip_num = 0
        self.running = False

    def run(self):
        while self.running:
            try:
                for i in range(6):
                    if self.cctv_ip_num > i:
                        # face detection
                        frame, names, faces = face_detection_pyqt5.run(self.frame[i], self.pdb)
                        # Saving detected names and faces
                        SOCK.get_detection(names, faces, i)
                time.sleep(1)
            except Exception as e:
                print("ERROR", e)

    def get_ip(self, ip_num):
        self.cctv_ip_num = ip_num

    def get_frame(self, fr):
        self.frame = fr.copy()

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

class IPInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Access prevention system")
        Background_layout = QVBoxLayout()

        Top_layout = QHBoxLayout()

        # Table outputting connected devices
        self.cctv_connection_table = QTableWidget()
        self.cctv_connection_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cctv_connection_table.resize(50, 50)
        self.cctv_connection_table.setColumnCount(1)
        self.cctv_connection_table.setRowCount(6)
        self.cctv_connection_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cctv_connection_table.setHorizontalHeaderLabels(['cctv'])

        self.door_connection_table = QTableWidget()
        self.door_connection_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.door_connection_table.resize(50, 50)
        self.door_connection_table.setColumnCount(1)
        self.door_connection_table.setRowCount(6)
        self.door_connection_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.door_connection_table.setHorizontalHeaderLabels(['door lock'])

        table_layout = QHBoxLayout()
        table_layout.addWidget(self.cctv_connection_table)
        table_layout.addWidget(self.door_connection_table)

        Connection_layout = QVBoxLayout()

        # Window and button for entering device ip addresses to connect
        self.ip_input = QLineEdit()
        Connection_layout.addWidget(self.ip_input)

        btn_layout = QHBoxLayout()
        self.input_button = QPushButton("Connect")
        self.input_button.clicked.connect(self.add_input)
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect_sock)
        btn_layout.addWidget(self.input_button)
        btn_layout.addWidget(self.disconnect_button)
        Connection_layout.addLayout(btn_layout)

        # Window for outputting videos
        self.img_vlayout = QVBoxLayout()
        self.img_hlayout1 = QHBoxLayout()
        self.img_hlayout2 = QHBoxLayout()

        self.image = {}
        for i in range(3):
            self.image[i] = QLabel()
            self.img_hlayout1.addWidget(self.image[i])
        for i in range(3):
            self.image[i + 3] = QLabel()
            self.img_hlayout2.addWidget(self.image[i + 3])
        self.img_vlayout.addLayout(self.img_hlayout1)
        self.img_vlayout.addLayout(self.img_hlayout2)

        Top_layout.addLayout(table_layout)
        Top_layout.addLayout(Connection_layout)

        Background_layout.addLayout(Top_layout)
        Background_layout.addLayout(self.img_vlayout)

        # Setting face detecting time
        self.start_h_spinbox = QSpinBox(self)
        self.start_h_spinbox.setRange(0, 24)
        self.start_m_spinbox = QSpinBox(self)
        self.start_m_spinbox.setRange(0, 59)
        self.end_h_spinbox = QSpinBox(self)
        self.end_h_spinbox.setRange(0, 24)
        self.end_m_spinbox = QSpinBox(self)
        self.end_m_spinbox.setRange(0, 59)

        self.start_h_label = QLabel('시', self)
        self.start_m_label = QLabel('분', self)
        self.end_h_label = QLabel('시', self)
        self.end_m_label = QLabel('분', self)

        self.add_btn = QPushButton('추가', self)
        self.add_btn.clicked.connect(self.add_btn_clicked)
        self.delete_btn = QPushButton('제거', self)
        self.delete_btn.clicked.connect(self.delete_btn_clicked)

        self.time_input_layout = QHBoxLayout()
        self.time_input_layout.addWidget(self.start_h_spinbox)
        self.time_input_layout.addWidget(self.start_h_label)
        self.time_input_layout.addWidget(self.start_m_spinbox)
        self.time_input_layout.addWidget(self.start_m_label)
        self.time_input_layout.addWidget(self.end_h_spinbox)
        self.time_input_layout.addWidget(self.end_h_label)
        self.time_input_layout.addWidget(self.end_m_spinbox)
        self.time_input_layout.addWidget(self.end_m_label)
        self.time_input_layout.addWidget(self.add_btn)

        self.time_table_name = QLabel('Time Table')
        self.time_table_name.setAlignment(Qt.AlignHCenter)
        self.time_table = QTableWidget()
        self.time_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.time_table.setColumnCount(2)
        self.time_table.setRowCount(15)
        self.time_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.time_table.setHorizontalHeaderLabels(['시작', '종료'])

        self.time_table_name_layout = QHBoxLayout()
        self.time_table_name_layout.addWidget(self.time_table_name)
        self.time_table_name_layout.addWidget(self.delete_btn)
        self.time_table_layout = QVBoxLayout()
        self.time_table_layout.addLayout(self.time_input_layout)
        self.time_table_layout.stretch(1)
        self.time_table_layout.addLayout(self.time_table_name_layout)
        self.time_table_layout.addWidget(self.time_table)

        self.total_layout = QHBoxLayout()
        self.total_layout.addLayout(Background_layout)
        self.total_layout.addLayout(self.time_table_layout)
        self.setLayout(self.total_layout)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_frames)
        self.timer_time_table_check = QTimer()
        self.timer_time_table_check.timeout.connect(self.check_time_table)

        self.cctv_ip_addresses = []  # entered cctv ip addresses
        self.door_ip_addresses = []  # entered door lock ip addresses

        self.video_capture = []  # read videos from ip addresses
        self.cctv_ip_num = 0  # the number of entered cctv ip addresses
        self.door_ip_num = 0  # the number of entered door lock ip addresses

        self.cctv_flg = {i: 1 for i in range(6)}  # Whether reading video from the web where cctv is streaming

        self.frame = [[] for _ in range(6)]

        self.start_time_set = []
        self.end_time_set = []
        self.running_flg = 0

        self.detect = DETECTION(self)
        self.detect.start()
        self.frame_thread = FRAME(self)
        self.frame_thread.start()
        self.start()



    def start(self):
        # self.timer.start(30)  # frame interval (milliseconds)
        self.timer_time_table_check.start(1000)

    # Setting Table using connected client ip addresses
    def set_Table(self, obj, s):
        if s == 'cctv':
            idx = self.cctv_ip_num - 1
            self.cctv_connection_table.setItem(idx, 0, QTableWidgetItem(self.cctv_ip_addresses[idx]))
        if s == 'door':
            idx = self.door_ip_num - 1
            self.door_connection_table.setItem(idx, 0, QTableWidgetItem(self.door_ip_addresses[idx]))

    # Connecting with devices via entered ip addresses
    def add_input(self):
        ip_address = self.ip_input.text()
        if ip_address:
            # (test) If ip address is not entered normally, videos will be printed.
            # self.cctv_ip_num += 1
            # If entered ip is web streaming ip of cctv(raspi)
            if ip_address.endswith('8081'):
                # if self.cctv_ip_num == 0:
                if ip_address[:5] not in self.cctv_ip_addresses and self.cctv_ip_num < 6:
                    video_ip = 'http://' + ip_address
                    src = cv2.VideoCapture(video_ip)
                    # src = cv2.VideoCapture(0)
                    ret, frame = src.read()
                    self.frame.append(frame)
                    if ret:
                        # checking connection with cctv
                        ip = ip_address[:-5]
                        # print(ip)
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.settimeout(1)
                        try:
                            connection = client_socket.connect_ex((ip, PORT))
                            # print(connection)
                            if connection == 0:
                                # Add cctv client
                                SOCK.cctv_clients.append(client_socket)
                                # start_new_thread(SOCK.detect_student, (0, ))

                                self.video_capture.append(src)
                                # save ip excluding port number
                                self.cctv_ip_addresses.append(ip_address[:-5])
                                self.cctv_ip_num += 1
                                self.detect.get_ip(self.cctv_ip_num)
                                self.set_Table(self, s='cctv')
                                QMessageBox.information(self, f"Success", f"Connected with '{ip_address}'")
                            else:
                                QMessageBox.critical(self, "Fail", f"Cannot connect with '{ip_address}'")
                        except:
                            client_socket.close()
                            QMessageBox.critical(self, "Fail", f"'{ip_address}' is not ip address format")
                    else:
                        del self.frame[self.cctv_ip_num]
                        QMessageBox.warning(self, "CAUTION", f"Cannot read video from '{ip_address}'.")
                else:
                    QMessageBox.warning(self, "CAUTION", "The CCTV is already connected.")
            # If entered ip is door lock(raspi) ip
            else:
                # if self.door_ip_num == 0:
                if ip_address not in self.door_ip_addresses:
                    # Checking connection with door lock
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.settimeout(1)
                    try:
                        connection = client_socket.connect_ex((ip_address, PORT))
                        # print(connection)
                        if connection == 0:
                            # Add door lock client
                            SOCK.doorlock_clients.append(client_socket)

                            self.door_ip_addresses.append(ip_address)
                            self.door_ip_num += 1
                            self.set_Table(self, s='door')
                            QMessageBox.information(self, f"Success", f"Connected with '{ip_address}'")
                        else:
                            client_socket.close()
                            QMessageBox.critical(self, "Fail", f"Cannot connect with '{ip_address}'")
                    except:
                        QMessageBox.critical(self, "Fail", f"'{ip_address}' is not ip address format")
                else:
                    QMessageBox.warning(self, "CAUTION", "The door lock is already connected.")
            self.ip_input.clear()

    # Disconnect socket communication with cctv or door lock
    def disconnect_sock(self):
        cell_cctv = self.cctv_connection_table.selectedItems()
        cell_door = self.door_connection_table.selectedItems()
        selected_cctv_row = sorted([cc.row() for cc in cell_cctv], reverse=True)
        selected_door_row = sorted([cd.row() for cd in cell_door], reverse=True)
        selected_cctv_num = len(selected_cctv_row)
        selected_door_num = len(selected_door_row)

        if selected_door_num or selected_cctv_num:
            buttonReply = QMessageBox.question(
                self, '연결 해제', 'CCTV {0}개, 도어락 {1}개 연결 해제 하시겠습니까?'.format(selected_cctv_num, selected_door_num),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

            if buttonReply == QMessageBox.Yes:
                self.cctv_ip_num -= selected_cctv_num
                self.door_ip_num -= selected_door_num
                self.detect.get_ip(self.cctv_ip_num)

                for cr in selected_cctv_row:
                    del self.cctv_ip_addresses[cr]
                    self.cctv_flg[cr] = 1
                    SOCK.cctv_clients[cr].close()
                    del SOCK.cctv_clients[cr]
                    del self.frame[cr]
                    self.video_capture[cr].release()
                    del self.video_capture[cr]

                for dr in selected_door_row:
                    del self.door_ip_addresses[dr]
                    SOCK.doorlock_clients[dr].close()
                    del SOCK.doorlock_clients[dr]

                self.cctv_connection_table.clear()
                self.door_connection_table.clear()
                self.cctv_connection_table.setHorizontalHeaderLabels(['cctv'])
                self.door_connection_table.setHorizontalHeaderLabels(['door lock'])

                for cn in range(self.cctv_ip_num):
                    self.cctv_connection_table.setItem(cn, 0, QTableWidgetItem(self.cctv_ip_addresses[cn]))
                for dn in range(self.door_ip_num):
                    self.door_connection_table.setItem(dn, 0, QTableWidgetItem(self.door_ip_addresses[dn]))

                QMessageBox.information(self, '연결 해제', '연결 해제 완료되었습니다.')
        else:
            QMessageBox.warning(self, '연결 해제', '선택된 셀이 없거나 연결된 기기가 존재하지 않습니다.')

        self.cctv_connection_table.clearSelection()
        self.door_connection_table.clearSelection()

    # Checking running time of face detecting
    def check_time_table(self):
        start_time = self.start_time_set.copy()
        end_time = self.end_time_set.copy()
        lt = time.localtime(time.time())
        now = int(lt.tm_hour * 100 + lt.tm_min)
        for i in range(len(start_time)):
            if end_time[i] >= now >= start_time[i]:
                if not self.running_flg:
                    self.resume()
                    self.running_flg = 1
                    print('start detecting')
                    break
                else:
                    continue
            if i == len(start_time) - 1 and self.running_flg:
                print('stop detecting')
                self.pause()
                self.running_flg = 0

    # Update frames from web streaming site
    def update_frames(self):
        # update frame on PyQt GUI
        for i in range(6):
            if self.cctv_ip_num > i:
                ret, self.frame[i] = self.video_capture[i].read()
                self.detect.get_frame(self.frame)
                if ret:
                    frame_rgb = cv2.cvtColor(self.frame[i], cv2.COLOR_BGR2RGB)
                    image = QImage(
                        frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888
                    )
                    pixmap = QPixmap.fromImage(image)

                    self.image[i].resize(500, 500)

                    self.image[i].setPixmap(pixmap.scaled(
                        self.image[i].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                    ))
                else:
                    # Once the connection is disconnected, reassign and checking that the frame is read
                    self.video_capture = [cv2.VideoCapture(self.cctv_ip_addresses[0])]
                    ret, self.frame[i] = self.video_capture[0].read()
                    if not ret:
                        self.cctv_ip_num -= 1
                        self.cctv_flg[i] = 1
            elif self.cctv_flg[i]:
                pixmap = QPixmap('image/none.png')

                self.image[i].resize(500, 500)

                self.image[i].setPixmap(pixmap.scaled(
                    self.image[i].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))
                self.cctv_flg[i] = 0

    def resume(self):
        self.detect.resume()
        self.detect.start()

    def pause(self):
        self.detect.pause()

    def add_btn_clicked(self):
        start_h = self.start_h_spinbox.value()
        start_m = self.start_m_spinbox.value()
        end_h = self.end_h_spinbox.value()
        end_m = self.end_m_spinbox.value()

        start_time = start_h * 100 + start_m
        end_time = end_h * 100 + end_m

        if start_time >= end_time:
            QMessageBox.warning(self, '경고', '종료 시간이 시작 시간보다 빠릅니다.')
        else:
            for i in range(len(self.start_time_set)):
                if (start_time <= self.start_time_set[i]) != (end_time <= self.end_time_set[i]):
                    QMessageBox.warning(self, '경고', '겹치는 동작 시간이 존재합니다.')
                    return
            self.start_time_set.append(start_time)
            self.end_time_set.append(end_time)
            self.start_time_set = sorted(self.start_time_set)
            self.end_time_set = sorted(self.end_time_set)

            self.set_time_table()

    def delete_btn_clicked(self):
        tt = self.time_table.selectedItems()
        selected_tt_row = sorted([t.row() for t in tt], reverse=True)
        selected_tt_num = len(selected_tt_row)

        if selected_tt_num:
            buttonReply = QMessageBox.question(
                self, '시간 제거', '시간대 {0}개 제거하시겠습니까?'.format(selected_tt_num),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

            if buttonReply == QMessageBox.Yes:
                for st in selected_tt_row:
                    del self.start_time_set[st]
                    del self.end_time_set[st]

                self.set_time_table()

            if not len(self.start_time_set):
                self.pause()

    def set_time_table(self):
        self.time_table.clear()
        self.time_table.setHorizontalHeaderLabels(['시작', '종료'])

        for st in range(len(self.start_time_set)):
            set_time = '{0:0>4}'.format(self.start_time_set[st])
            self.time_table.setItem(st, 0, QTableWidgetItem('{0}:{1}'.format(set_time[:2], set_time[2:])))
        for et in range(len(self.end_time_set)):
            set_time = '{0:0>4}'.format(self.end_time_set[et])
            self.time_table.setItem(et, 1, QTableWidgetItem('{0}:{1}'.format(set_time[:2], set_time[2:])))


class SOCKET:

    def __init__(self):
        self.count = 0
        self.names = [[] for _ in range(6)]
        self.faces = [[] for _ in range(6)]
        self.cctv_clients = []
        self.doorlock_clients = []

        self.cctv_ip_addresses = []  # entered cctv ip addresses
        self.door_ip_addresses = []  # entered door lock ip addresses

        self.video_capture = []  # read videos from ip addresses
        self.cctv_ip_num = 0  # the number of entered cctv ip addresses
        self.door_ip_num = 0  # the number of entered door lock ip addresses

        self.exit_flg = [0]
        self.detect_flg = [0]

        # self.HOST_ip = socket.gethostbyname(socket.getfqdn())
        self.HOST_ip = ''
        self.and_clients = []
        self.send_queue = Queue()

        self.detect_cnt = 5

    def get_detection(self, names, faces, idx):
        try:
            if names != self.names[idx] and len(names) > 0 and faces:
                print(self.names[idx], names)
                self.names[idx] = names.copy()
                self.faces[idx] = faces.copy()
                self.detect_student(dump=0, idx=idx)
            else:
                print('no detection', end=' ')
                print(names, idx)
                self.names[idx] = names.copy()
        except Exception as e:
            print('ERROR OCCUR', e)

    def detect_student(self, dump, idx):
        msg = 'detect'.encode()
        try:
            img = np.array(self.faces[idx][0], np.uint8)
            cv2.imwrite('image/face.jpg', img)
            img = cv2.imread('image/face.jpg')
            _, img_encoded = cv2.imencode('.jpg', img)
            img_bytes = img_encoded.tobytes()

            for doorlock in self.doorlock_clients:
                doorlock.send(msg)

            for client in self.and_clients:
                img_length = len(img_bytes)
                client.send(img_length.to_bytes(4, 'big'))
                client.send(img_bytes)

                d_name = self.names[idx][0]
                d_name_encode = d_name.encode('utf-8')
                d_name_len = len(d_name_encode)
                client.send(d_name_len.to_bytes(4, 'big'))
                client.send(d_name_encode)
        except Exception as e:
            print('NO FACES!!!', e)
        try:
            self.cctv_clients[idx].send(msg)
        except ConnectionAbortedError:
            print('connection is aborted')
            self.cctv_clients.clear()

    # Send message for found student to every device
    def Send_msg(self):
        img_file_path = 'image/school.jpg'
        img = cv2.imread(img_file_path)
        _, img_encoded = cv2.imencode('.jpg', img)
        img_bytes = img_encoded.tobytes()

        while 1:
            try:
                # If new client is added, escaping loop for making new thread
                recv = self.send_queue.get()  # waiting for received data
                if recv == 'Group Changed':
                    print('Group Changed')
                    break

                # msg = recv[0]

                msg = 'end'
                # print(msg)
                for conn in self.and_clients:
                    img_len = len(img_bytes)
                    conn.send(img_len.to_bytes(4, 'big'))
                    conn.send(img_bytes)
                    conn.send(len(msg).to_bytes(4, 'big'))
                    conn.send(msg.encode('utf-8'))
                for door in self.doorlock_clients:
                    door.send(msg.encode())
                for cctv in self.cctv_clients:
                    cctv.send(msg.encode())
            except:
                pass

    # Receiving message for found student
    def Recv_msg(self, idx):
        while 1:
            try:
                data = self.and_clients[idx].recv(1024).decode()
                if not data:
                    self.and_clients[idx].close()
                    del self.and_clients[idx]
                    break
                else:
                    self.send_queue.put([data, self.and_clients[idx]])
            except ConnectionAbortedError:
                self.and_clients[idx].close()
                del self.and_clients[idx]
                break
            except ConnectionResetError:
                self.and_clients[idx].close()
                del self.and_clients[idx]
                break
        self.count -= 1
        return

    def and_sock(self, dummy):
        # print(dummy)
        print('Server started')
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((self.HOST_ip, PORT))
        server_sock.listen(5)
        self.count = 0  # the number of connected clients

        while 1:
            self.count += 1
            client, addr = server_sock.accept()  # Open socket and wait clients
            self.and_clients.append(client)
            print('Connected :', str(addr))

            if self.count > 1:
                self.send_queue.put('Group Changed')
                thread1 = threading.Thread(target=self.Send_msg, args=())
                thread1.start()
            else:
                thread1 = threading.Thread(target=self.Send_msg, args=())
                thread1.start()

            thread2 = threading.Thread(target=self.Recv_msg, args=(self.count - 1,))
            thread2.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IPInputWindow()
    SOCK = SOCKET()
    start_new_thread(SOCK.and_sock, (0,))  # 0 is dummy data
    window.show()
    sys.exit(app.exec())
