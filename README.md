# Access Prevention System

### 특수학교 교출 감지 시스템

| "교출" : 장애학생이 교실 혹은 학교에서 무단 이탈하는 상황
<br>
| 학생의 얼굴을 인식하여 교출 상황을 애플리케이션을 통해 알리고, 교문을 잠금

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/android-34A853?style=for-the-badge&logo=android&logoColor=white">
<img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=white">
<img src="https://img.shields.io/badge/raspberrypi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white">

---
### 주요 기능
- PC
  - Raspberry pi 4B를 이용해 제작한 CCTV와 도어락과 소켓 통신 (GUI)
  - Timetable 설정 기능을 통해 수업 시간에만 교출 감지 기능 동작 (GUI)
  - CCTV 화면 실시간 모니터링 (GUI)
  - 애플리케이션과 소켓 통신
  - CCTV 화면에 대해 얼굴 인식을 수행해 학생을 검출
- Application
  - 학생 별 교출 이력 확인 가능
  - CCTV 화면 실시간 모니터링
  - 교직원별 수색구역 배치표 확인 가능
  - 교출 상황 발생 시 학생의 사진을 메인 화면에 표출
  - 학생 발견 시 알림 버튼 터치로 빠른 상황 종료 전파
- CCTV (Raspberry pi 4B)
  - 카메라 웹 스트리밍을 통한 CCTV 기능 수행
  - 교출 상황 발생 시 학생 검출된 CCTV는 부저 동작 및 LED 점등
- 도어락 (Raspberry pi 4B)
  - 키패드와 서보 모터를 이용해 열림/잠금 기능 수행
  - 교출 상황 발생 시 LED 점등 및 열기 불가능
---
### 동작 시나리오
- PC
![PC](https://github.com/user-attachments/assets/d814a549-43fa-49e9-90db-fb36af2d85ca)
<br><br>
- Application
![Application](https://github.com/user-attachments/assets/74415e80-5ac6-48b9-9f87-2c4a683c9f36)
<br><br>
- CCTV
![CCTV](https://github.com/user-attachments/assets/a6522f4c-5173-4982-bec1-b0842f83290f)
<br><br>
- 도어락
![doorlock](https://github.com/user-attachments/assets/e3f9409d-7cb2-4c40-b626-1246476cf0d9)
---
### 동작

### PC (GUI)

<img src="https://github.com/user-attachments/assets/f8e1b7a0-710b-4893-b63c-7784b3326f7b" width="400" height="200"/>

  - 기기(CCTV, 도어락) IP 입력으로 연결

<img src="https://github.com/user-attachments/assets/fa6171f6-73bf-4c7d-b664-60ba3fb026ee" width="400" height="200"/>

  - Timetable 설정
    - 수업 시간에만 인식 수행
    - 입력된 시간이 겹치는 경우 알림

<img src="https://github.com/user-attachments/assets/0ed42990-a8c6-4bfa-920e-5cf8ebe137bc" width="400" height="200"/>


### Application

- 학생 별 교출 기록 확인
  
<img src="https://github.com/user-attachments/assets/10f2ad5d-7ce4-40a6-8b9d-5207eeb72a0e" width="200" height="400"/>

- CCTV 화면 실시간 모니터링
  
<img src="https://github.com/user-attachments/assets/10485fd1-6947-4ace-b45c-de0a742226ba" width="200" height="400"/>

- 교직원 별 수색구역 배치표 확인

<img src="https://github.com/user-attachments/assets/3e48114d-73b0-47f5-a9e6-01a0ab7bea82" width="200" height="400"/>

- 교출 상황 발생 시 알림
  - 푸시 알림 기능

<img src="https://github.com/user-attachments/assets/4b628cad-df80-45dd-ae31-b2b18e058bf7" width="200" height="400"/>
<img src="https://github.com/user-attachments/assets/69bbe8f0-bf75-43ff-bb74-9c3961ac6c98" width="200" height="400"/>

### CCTV

- 교출 상황 발생 시 학생 검출된 CCTV는 부저 동작 및 LED 점등

<img src="https://github.com/user-attachments/assets/246e2a7f-6ba7-4206-8e89-709d239e61a0" width="500" height="300"/>

### 도어락

- 키패드와 서보 모터를 이용해 열림/잠금 기능 수행
  
<img src="https://github.com/user-attachments/assets/1da7d9e0-8b15-4589-b563-938965d43c5d" width="500" height="300"/>

---

### Python Face Recognitoion in Real Time

- face recognition library
  - 딥러닝으로 구축된 dlib의 얼굴 인식 기능을 사용하여 구축됨
  - Haar Cascade Classifier를 이용해 얼굴을 인식
  - 주요 기능
    - 얼굴 검출 : 이미지 내에서 하나 이상의 얼굴을 검출
    - 얼굴 특징점 검출 : 얼굴의 주요 특징점(눈, 코, 입 등) 위치를 검출
    - 얼굴 인식 : 인식된 얼굴이 데이터베이스의 어떤 얼굴과 일치하는지 확인
    - 얼굴 비교 : 두 얼굴이 같은 사람의 것인지 비교

- HAAR Cascade Classifiers
  - 'Rapid Object Detection using a Boosted Cascade of Simple Features' 논문(2001년 발표)에서 제안한 객체 검출기
  - 간단한 feature 값을 바탕으로 이미지를 분류
    - feature = HAAR feature
    - HAAR feature란 HAAR filter를 통해 추출된 feature
  - feature는 이미지 픽셀을 인코딩하는 역할을 수행
  - feature 기반 검출 시스템은 픽셀 기반 검출 시스템보다 빠름
  - 'Edge features', 'Line features', 'Center-surround features'의 feature 존재
  - HAAR filter로 이미지를 순회하며 feature 값을 추출
    - HAAR 필터를 여러 방향, 여러 스케일로 조정해서 사용 가능
    - 여러 방향, 스케일의 특징을 추출하여 객체의 경계를 검출
  - feature 값을 바탕으로 얼굴의 주요 특징점의 위치를 계산, 동일 인물인지 판단 가능

---

### 트러블 슈팅

- 소켓 통신을 통한 이미지 전송
  - 애플리케이션에 학생이 인식된 사진 전송 기능 필요
  - 이미지는 numpy의 ndarray type이므로 데이터 패킷에 그대로 전송 불가능
  - 데이터 변환을 수행해 변환 필요
  - 이미지를 '.jpg'로 인코딩 후 numpy의 '.tobytes()' 메서드를 이용해 array에서 bytes로, raw date로 변환하여 전송 가능

```python
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
```

- face_recognition 라이브러리를 이용한 얼굴 인식
  - 얼굴 인식 과정에서 에러 발생
  - 기능 단위 테스트를 통해 'face_location' 메서드에서 에러가 발생함 발견
  - stackoverflow를 통해 BGR -> RGB 변환 과정에서 문제가 발생함을 확인
  - https://stackoverflow.com/questions/75926662/face-recognition-problem-with-face-encodings-function

``` python
# return list of dlib.rectangle
    def locate_faces(self, locate_frame):
        if self.ratio == 1.0:
            # rgb = locate_frame[:, :, ::-1]
            rgb = cv2.cvtColor(locate_frame, cv2.COLOR_BGR2RGB)
        else:
            small_frame = cv2.resize(locate_frame, (0, 0), fx=self.ratio, fy=self.ratio)
            # rgb = small_frame[:, :, ::-1]
            rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        try:
            boxes = face_recognition.face_locations(rgb)
        except Exception as e:
            print('ERROR OCCUR', e)
        if self.ratio == 1.0:
            return boxes
        else:
            return []
```

- GUI에서 CCTV 화면 프레임 드랍
  - 기존에는 'CCTV 화면을 읽어옴 -> GUI에 표시 -> 해당 프레임에 얼굴 인식 수행'의 과정
  - 얼굴 인식 과정이 느려 GUI에 CCTV 화면이 표시되는 간격이 길어짐
  - 'QThread'를 이용해 'GUI에 표시' 과정과 '얼굴 인식 수행' 과정을 병렬적으로 처리하여 프레임 드랍 개선

```python
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
```