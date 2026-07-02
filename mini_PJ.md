# 🏎️ Autocar Prime + NX 미니 과제 소스코드 세부 분석 리포트

본 문서는 웹 인터페이스 기반의 원격 제어 인프라와 Jetson NX 하드웨어 계층(`pop` 라이브러리) 간의 연동 메커니즘을 파일 및 라인 단위로 분석한 명세서입니다.

---

## 📂 1. 프로젝트 아키텍처 및 데이터 흐름 개요

```text
[노트북 크롬 브라우저] (웹 UI / JS 조이스틱 연산)
         │  ▲
  HTTP   │  │  MJPEG
  POST   ▼  │  Stream
[Flask 웹 서버 (server.py)] ── (스레드 병렬 처리)
         │
         ├─► [car_controller.py] ──► [pop.Pilot] ──► (I2C Bus 1: 모터 및 조향 서보)
         ├─► [camera_controller.py] ─► [pop.Util] ──► (GStreamer / 팬틸트 서보)
         └─► [sound_controller.py] ──► [PyAudio] ──► (PWM 사운드 / TTS 엔진)


⚙️ 2. 소스코드 라인별 상세 분석
① config.py (전역 설정 파일)
USE_ACTUAL_HARDWARE = True

분석: 실제 하드웨어(pop 라이브러리가 설치된 Jetson NX 임베디드 환경)를 가동할지, 노트북 디버깅용 가상 모드(Mock)로 작동할지 결정하는 마스터 스위치입니다.

LIMIT_SPEED_MAX = 99 / LIMIT_SPEED_MIN = 20

분석: pop.Pilot 내부의 Driving 모듈이 수용하는 DC 모터 변속기 물리 입력 한계 스케일(20~99)을 제한하여 저속 구동 불능 현상 및 고속 과부하를 방지합니다.

LIMIT_STEER_MIN = -1.0 / LIMIT_STEER_MAX = 1.0

분석: 앞바퀴 조향 서보모터의 회전 반경 범위를 정규화된 실수값인 -1.0(최대 좌회전)에서 1.0(최대 우회전) 사이로 고정하여 링크 기구부 파손을 방방합니다.

PAN_MAX, PAN_MIN = 180, 0 / TILT_MAX, TILT_MIN = 180, 0

분석: 카메라 2축 관절 서보모터의 하드웨어 한계 각도(0~180도)를 고정하여 내부 기어가 헛돌거나 타버리는 현상을 방지합니다.

🏎️ ② car_controller.py (차량 구동 및 조향)
from pop import Pilot

분석: 하드웨어 가동 상태일 때 Jetson 전용 임베디드 제어 패키지 내 Pilot 헬퍼 클래스를 동적 로드합니다.

self.car = Pilot.get_Control()

분석: pop 라이브러리의 하드웨어 스캔 함수입니다. 내부적으로 I2C Bus 1의 0x5c 주소를 탐색하여, 성공 시 6번 장치 기종인 AutoCar Prime + NX 인스턴스를 자동 할당합니다.

self.car.stop()

분석: 주행 모터 구동 칩셋(0x5e 주소)의 PWM 듀티 사이블 출력을 즉시 0으로 떨어뜨려 휠 공급 전류를 전면 차단합니다.

abs_speed = max(LIMIT_SPEED_MIN, min(LIMIT_SPEED_MAX, abs_speed))

분석: 알고리즘 연산 오류로 인해 폭주하는 속도 값이 들어오더라도 하드웨어 한계치 안으로 강제 고정(Clamping)하는 소프트웨어 방어 로직입니다.

self.car.forward(abs_speed) / self.car.backward(abs_speed)

분석: pop 드라이빙 인터페이스를 통해 모터 드라이버 레지스터에 정방향/역방향 주파수 제어 패킷을 밀어 넣습니다.

self.car.steering = angle

분석: Wheel 클래스 속성에 값을 대입합니다. 내부 커널단에서 기종(_cat == 6)을 감지하고, 서보 설계 배치 구조에 맞추어 angle에 자동으로 -1을 곱해 하드웨어 물리 반전 처리를 수행한 뒤 I2C Bus 1의 주소 0x5c 채널 15번으로 PWM 제어 신호를 전달합니다.

self.car.steering = 0.0

분석: 위험 상황 정지 시 구동을 멈추는 것뿐만 아니라, 꺾여있던 앞바퀴 서보모터를 완전히 정중앙 정렬 상태로 정치(Neutralization) 시킵니다.

🎥 ③ camera_controller.py (카메라 및 관절 제어)
cam = Util.gstrmer(width=640, height=480, fps=30, flip=0)

분석: pop.Util 모듈을 호출하여 엔비디아 Jetson 가속 프레임워크인 nvarguscamerasrc 파이프라인 문자열 명령어를 시스템에 맞춤형 빌드합니다.

cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)

분석: 생성된 GStreamer 파이프라인 구문을 OpenCV 비디오 엔진에 바인딩하여 커널 레벨의 고속 멀티미디어 프레임 캡처 통로를 개방합니다.

self.car.camPan(self.pan) / self.car.camTilt(self.tilt)

분석: pop.Pilot 구조 내부의 CameraPod 객체를 호출하여 0x5c 주소 내 14번(Pan), 13번(Tilt) 서보 인터페이스 축의 하드웨어 물리 관절 각도를 조작합니다.

ret, frame = self.cap.read()

분석: 비디오 하드웨어 버퍼 파이프라인으로부터 3차원 넘파이 행렬 배열(Raw BGR 이미지 데이터)을 실시간으로 가져옵니다.

cv2.imencode('.jpg', frame)

분석: 무겁고 직렬화되지 않은 원본 넘파이 픽셀 데이터를 웹 환경에서 빠르게 패킷으로 나를 수 있도록 경량 압축 이미지 포맷인 JPEG로 변환합니다.

yield (b'--frame\r\n'...)

분석: 웹 브라우저 표준 MJPEG(Motion JPEG) 연속 스트리밍 규약에 맞게 헤더 파트(Content-Type: image/jpeg)와 바이트 스트림을 조합해 호출 루프에 실시간 제너레이터 형태로 데이터를 배출합니다.

🔊 ④ sound_controller.py (오디오 신호 및 TTS 제어)
p = pyaudio.PyAudio()

분석: 리눅스 OS 사운드 아키텍처와 직접 인터페이스를 수행하는 포트오디오(PortAudio) 핵심 추상화 인스턴스를 시동합니다.

stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True)

분석: 48kHz 샘플링 레이트 환경 하에 모노(1) 채널, 32비트 부동소수점 데이터 규격으로 하드웨어 스피커에 데이터를 다이렉트로 써 내려갈 출력 버퍼 스트림을 개방합니다.

np.sin(2 * np.pi * t * freq / rate)

분석: DSP(디지털 신호 처리) 물리 수학 공식입니다. 시간축 배열 t 위에 인자로 받은 특정 주파수(freq)를 투영하여 가상의 순수 디지털 사인파 오디오 신호 배열을 수학적으로 연산해 냅니다.

stream.write(0.3 * sample)

분석: 과도한 볼륨으로 스피커 진동판이 손상되지 않도록 진폭 가중치 오프셋(0.3)을 곱셈 연산 처리한 뒤 사운드 카드 하드웨어 드라이버 버퍼에 써서 물리 비프음을 발생시킵니다.

tts = gTTS(text=text, lang='ko') / tts.save("tts_temp.mp3")

분석: 구글의 온라인 음성 합성 OpenAPI 웹 서버에 접속하여 텍스트 데이터에 부합하는 정밀 한국어 오디오 파일(MP3) 스트림을 전송받아 로컬 공간에 임시 저장합니다.

os.system("mpg123 tts_temp.mp3 > /dev/null 2>&1")

분석: 리눅스 OS 네이티브 셸 명령 체계를 강제 가동하여 백그라운드 콘솔 디바이스 플레이어(mpg123) 프로그램으로 음성 소리 출력을 실행합니다. 불필요한 시스템 로그 찌꺼기는 비트 버킷(>/dev/null)으로 소거합니다.

os.system(f"espeak -v ko \"{text}\" > /dev/null 2>&1")

분석: 네트워크 연결이 단절되는 예외(Exception) 국면 돌입 시, 인터넷 연결이 필요 없는 임베디드 로컬 전용 음성 합성 패키지인 espeak 코드를 방어 기제로 대신 가동(Fallback)시킵니다.

🌐 ⑤ server.py (최상위 Flask REST API 웹 서버)
__main__._camera_flip_method = 0

분석: 가장 중요한 하드웨어 예외 해결 코드입니다. pop.Util.gstrmer 코드가 비동기 스레드 실행 시 메인 커널 영역(__main__)에 하드코딩된 변수를 무조건 참조하도록 설계되어 생기는 런타임 크래시를 방지하기 위해 가짜 환경 속성을 런타임 시작과 동시에 전역 메모리에 강제 선언해 둡니다.

app = Flask(__name__) / CORS(app)

분석: Flask 인스턴스를 할당하고, 웹 브라우저 프론트엔드가 크로스 도메인 보안 규약 때문에 비동기 패킷 전송을 차단하는 자바스크립트 CORS 보안 이슈를 전면 해제하는 미들웨어 필터를 작동시킵니다.

@app.route('/api/status', methods=['GET'])

분석: 자바스크립트 타이머 루프가 500ms(0.5초)마다 하드웨어의 최신 상태(현재 속도, 조향각, 카메라 각도)를 물어보고 실시간으로 모니터링 패널을 갱신하는 폴링(Polling) 엔드포인트입니다.

x, y = float(data['x']), float(data['y'])

분석: 자바스크립트 가상 조이스틱 엔진이 물리 수식(피타고라스 거리 가공)을 통해 도출해 낸 -1.0 ~ 1.0 범위의 기하학적 좌표 비율 데이터를 인계받습니다.

target_speed = int(y * LIMIT_SPEED_MAX)

분석: 조이스틱의 상하 이동 정보 비례 실수 값(y)을 하드웨어 구동 모터 가동 제어 범위 정수형 속도로 스케일 가중치를 곱해 변환합니다.

@app.route('/') / def index():

분석: 리눅스 X11 GUI 디스플레이 서버가 존재하지 않는 원격 주피터 터미널 환경에서 대시보드 창을 띄우지 못해 생기는 그래픽 크래시 에러를 우회하는 해결 루틴입니다. 사용자가 크롬 창에 IP를 치고 진입하면 내장된 통합 프론트엔드 코드(HTML/CSS/JS 조이스틱 물리 연산 엔진)를 클라이언트로 직접 쏴줍니다.

app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

분석: 0.0.0.0 설정을 통해 무선 랜카드로 들어오는 외부 접근 통로를 전면 개방하고, threaded=True 멀티스레딩 옵션을 켜서 고용량 카메라 스트리밍 데이터 전송 루프와 실시간 사용자 모터 제어 명령 수신 처리가 단일 프로세스 내에서 뭉개지지 않고 완전히 독립 병렬(Non-blocking) 작동하도록 구성합니다.