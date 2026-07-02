# 🏎️ 멀티스레드(Multi-Thread) 기반 LiDAR 물체 추종 코드 정밀 명세서

본 문서는 단일 스레드의 블로킹(Blocking) 문제를 해결하기 위해 백그라운드 센서 스캔 스레드와 메인 차량 제어 스레드를 분리하여 구현한 멀티태스킹 자율 추종 시스템 분석 리포트입니다.

---

## 🏗️ 1. 스레드 간 데이터 공유 아키텍처

```text
[ 백그라운드 라이다 스레드 ]                   [ 메인 제어/구동 스레드 ]
 (lidar_scan_thread)                             (__main__ Loop)
         │                                               │
         ▼ (0.08초 주기 계측 및 필터링)                 │ (0.1초 주기 데이터 모니터링)
   ┌───────────┐                                         │
   │ data_lock │ ── [공유 메모리: lidar_data 딕셔너리] ──┤
   └───────────┘       - avg_angle (평균 각도)           │
         ▲             - min_distance (최근접 거리)      ▼ (10도 임계치 판별)
         │             - has_target (타겟 유무 변수)    [하드웨어 즉각 제어]
         │                                               - car.steering = 비율
         └─────────────────────────────────────────────── - car.forward(50)
⚙️ 2. 소스코드 라인별 상세 분석 (.md)① 초기 라이브러리 로드 및 하드웨어 인스턴스 선언import threading분석: 파이썬 환경에서 병렬 프로세싱(비동기 멀티태스킹) 인터페이스를 구축하기 위한 코어 스레드 라이브러리를 로드합니다.from pop import Pilot, LiDAR분석: 차량의 구동 및 조향을 담당하는 Pilot 모듈과 라이다 센서 제어용 LiDAR 모듈을 임베디드 하드웨어 패키지에서 가져옵니다.import numpy as np분석: 대량의 라이다 포인트 각도 데이터를 벡터화하여 평균값(np.mean)을 실시간 고속 연산하기 위해 로드합니다.car = Pilot.get_Control()분석: pop 라이브러리를 기점으로 I2C 통신 버스를 스캔하여 실차 하드웨어(AutoCar Prime)의 제어 객체를 할당받습니다.lidar = LiDAR.Rplidar()분석: 360도 회전식 레이저 거리 측정 센서인 RPLiDAR 제어를 위한 전용 클래스 인스턴스를 메모리에 생성합니다.lidar.connect() / lidar.startMotor()분석: 라이다 물리 장치의 내부 시리얼 디바이스 통신 라인을 개방하고, 상단 레이저 스캐너 헤드를 구동하는 모터를 회전시킵니다.② 스레드 간 데이터 공유 징검다리 및 락(Lock) 정의lidar_data = { "avg_angle": 0.0, "min_distance": 9999.0, "has_target": False }분석: 전역(Global) 공간에 선언된 공유 딕셔너리 메모리입니다. 라이다 스레드가 채워 넣은 최신 연산 데이터를 메인 스레드가 읽어가는 통로입니다.data_lock = threading.Lock()분석: 멀티스레드 환경의 핵심 안전장치입니다. 두 개의 스레드가 공유 딕셔너리에 동시에 읽기/쓰기를 시도할 때 발생하는 메모리 충돌 크래시(Race Condition)를 차단하는 상호 배제 뮤텍스(Mutex) 열쇠를 정의합니다.is_running = True분석: 프로그램 전체의 생명 주기를 관장하는 불리언 플래그입니다. 강제 종료 시 False로 변환되어 모든 백그라운드 루프를 연쇄 중단시킵니다.🔄 ③ 백그라운드 라이다 스캔 및 데이터 토스 스레드 함수def lidar_scan_thread():분석: 메인 루프의 흐름과 완전히 독립되어 백그라운드에서 오직 라이다 센싱 및 데이터 필터링만 전담 마크하는 별동대 함수입니다.vectors = lidar.getVectors()분석: 하드웨어 버퍼로부터 현재 스캔 주기에 잡힌 [(각도, 거리, 신뢰도), ...] 구조의 고밀도 수치 배열 리스트를 수집합니다.if 150 <= distance <= 700:분석: 추종할 타겟(사람의 손이나 상자)의 유효 반경을 최소 15cm에서 최대 70cm로 한정하여 원거리 벽면이나 근거리 자체 노이즈 데이터를 소거합니다.if angle <= 45: ... elif angle >= 315:분석: 정면($0^\circ$)을 기준으로 좌우 $\pm 45^\circ$(총 $90^\circ$ 시야각) 범위를 지정하여 후방 및 측면 데이터를 제외한 전방 감지 영역을 슬라이싱합니다.target_angles.append(angle - 360)분석: 정면 좌측 영역($315^\circ \sim 360^\circ$) 각도 데이터에서 360을 감산하여 음수 각도($-45^\circ \sim 0^\circ$)로 수학적 정형화를 수행합니다. 이를 통해 평균 계산 시 좌/우 방향성이 부호로 직관적으로 분리됩니다.with data_lock:분석: 공유 영역 수정을 위해 열쇠(data_lock)를 획득합니다. 이 컨텍스트 블록 안에서 데이터를 안전하게 업데이트하며, 작업이 끝나면 자동으로 열쇠를 반환합니다.lidar_data["avg_angle"] = np.mean(target_angles)분석: 시야 내에 잡힌 포인트들의 산술 평균 각도를 도출하여 타겟 물체의 전체적인 무게중심 방향을 최종 확정합니다.time.sleep(0.08)분석: 라이다 스레드가 CPU 자원을 과도하게 독점하지 않도록 0.08초 동안 프로세스를 대기 상태(Sleep)로 전환시키는 커널 배려 로직입니다.🏎️ ④ 메인 주행 구동 및 조건문 제어 엔진 영역t = threading.Thread(target=lidar_scan_thread, daemon=True)분석: 앞서 정의한 라이다 전담 함수를 병렬로 실행할 독립 스레드 객체로 빌드합니다. daemon=True 설정을 통해 메인 프로세스가 종료되면 이 스레드도 즉각 강제 퇴근하도록 바인딩합니다.t.start()분석: 운영체제(OS) 스케줄러에 스레드 출발 신호를 인가하여 백그라운드 라이다 수집 연산을 실시간 구동시킵니다.with data_lock: has_target = lidar_data["has_target"] ...분석: 메인 구동 루프 시작점에서 락을 걸고, 라이다 스레드가 실시간으로 토스(갱신)해 둔 최신 데이터 스냅샷을 안전하게 로컬 변수로 복사해 옵니다.if min_distance < 200: car.stop()분석: 최우선 인터럽트 방어선입니다. 물체가 20cm 이내로 진입하면 즉시 하드웨어 구동 칩셋의 출력을 차단하여 충돌을 물리적으로 방지합니다.if avg_angle <= -10: car.steering = -0.8분석: 토스받은 타겟의 평균 위치가 좌측 10도 이상 범위 바깥으로 틀어졌음을 감지하고 바퀴 조향 서보를 좌측 파워 스케일(-0.8)로 확 꺾어 정렬합니다.elif avg_angle >= 10: car.steering = 0.8분석: 타겟의 평균 위치가 우측 10도 이상 범위 바깥으로 밀려났음을 감지하고 바퀴 조향 서보를 우측 파워 스케일(0.8)로 확 꺾어 정렬합니다.else: car.steering = 0.0분석: 물체의 평균 위치가 데드존 범위(좌우 10도 이내 정면)에 안정적으로 포지셔닝되어 있다면 바퀴를 정중앙(0.0)으로 정렬시켜 직진 상태를 유지합니다.car.forward(50)분석: 조향각 설정이 완료되면 저전압 토크 부족 현상(모터 데드존)을 극복하고 바닥 마찰력을 차고 나갈 수 있는 적정 기동 출력(50)을 DC 모터에 인가하여 전진시킵니다.time.sleep(0.1)분석: 메인 구동 판단 루프를 0.1초(10Hz) 간격으로 정렬하여 라이다 데이터 수신 패킷 속도와 제어 타이밍의 싱크를 맞춰줍니다.🛑 ⑤ 시스템 안전 종료 및 하드웨어 자원 회수 (Cleanup)except KeyboardInterrupt:분석: 사용자가 콘솔 터미널 환경에서 Ctrl + C를 눌러 프로그램을 인위적으로 터뜨릴 때 발생하는 인터럽트 신호를 안전하게 캐치하여 예외가 예쁘게 처리되도록 유도합니다.is_running = False분석: 가동 플래그를 꺼서 백그라운드에서 돌아가고 있던 라이다 스캔 스레드의 while 무한 루프 조건을 파괴하여 안전하게 퇴근(종료)시킵니다.car.stop() / car.steering = 0.0 / lidar.stopMotor()분석: 프로세스가 완전히 셧다운되기 직전, 굴러가던 차량 구동 모터를 완전히 정지시키고 꺾여있던 서보모터를 정중앙으로 중립 정렬하며 고속 회전 중이던 라이다의 물리 레이저 헤드 모터 전원까지 전면 차단하여 시스템의 메모리 및 하드웨어 자원을 깔끔하게 커널로 반환합니다.

# 코드 구현 부분
import time
import threading
from pop import Pilot, LiDAR
import numpy as np

# 하드웨어 글로벌 초기화
car = Pilot.get_Control()
lidar = LiDAR.Rplidar()

lidar.connect()
lidar.startMotor()

# ─── 스레드 간 데이터 공유를 위한 전역 변수 (인프라 징검다리) ───
lidar_data = {
    "avg_angle": 0.0,
    "min_distance": 9999.0,
    "has_target": False
}
data_lock = threading.Lock()  # 데이터 동시 접근으로 인한 크래시 방지용 락(Lock)

is_running = True  # 전체 시스템 가동 플래그


# 🛠️ [스레드 기능 1] 백그라운드 라이다 고속 스캔 및 데이터 토스 루프
def lidar_scan_thread():
    global is_running, lidar_data
    print("[THREAD] LiDAR 백그라운드 스캔 스레드 가동 시작")
    
    while is_running:
        try:
            vectors = lidar.getVectors()
            
            target_angles = []
            target_distances = []
            
            for vec in vectors:
                angle = vec[0]
                distance = vec[1]
                
                # 물체 인식 유효 거리 (15cm ~ 70cm)
                if 150 <= distance <= 700:
                    if angle <= 45:
                        target_angles.append(angle)
                        target_distances.append(distance)
                    elif angle >= 315:
                        target_angles.append(angle - 360)
                        target_distances.append(distance)
            
            # 공유 변수 갱신 영역 (락을 걸어 메인 스레드와 안전하게 데이터 교환)
            with data_lock:
                if target_angles:
                    lidar_data["avg_angle"] = np.mean(target_angles)
                    lidar_data["min_distance"] = min(target_distances)
                    lidar_data["has_target"] = True
                else:
                    lidar_data["has_target"] = False
                    
        except Exception as e:
            print(f"[THREAD ERROR] 라이다 스캔 실패: {e}")
            
        time.sleep(0.08)  # 0.08초 주기로 미세하게 쉬어주며 센서 샘플링 대기


# ─── 메인 실행 영역 (구동 제어 전담) ───
if __name__ == '__main__':
    # 1. 라이다 백그라운드 스레드 생성 및 실행
    t = threading.Thread(target=lidar_scan_thread, daemon=True)
    t.start()
    
    ttime = time.time()
    print("[MAIN] 메인 제어 루프 가동 시작 (5분 제한)")
    
    # 조향 파워 상수
    current_steering = 0.0
    
    try:
        while time.time() - ttime < 300:
            # 2. 안전하게 라이다 스레드가 토스한 최신 데이터 스냅샷 복사
            with data_lock:
                has_target = lidar_data["has_target"]
                avg_angle = lidar_data["avg_angle"]
                min_distance = lidar_data["min_distance"]
            
            # 3. 토스받은 데이터 기반 독립적인 즉각 제어 판단
            if has_target:
                # 충돌 방지
                if min_distance < 200:
                    print(f"[🚨 EMERGENCY] 너무 가까움 ({min_distance}mm) -> 즉각 제동")
                    car.stop()
                    continue
                
                # 평균 10도 기준 조건문 및 조향 판단
                if avg_angle <= -10:
                    car.steering = -0.8
                    print(f"◀◀ [LEFT] 좌측 10도 이상 치우침 ({avg_angle:.1f}°) -> 좌회전")
                elif avg_angle >= 10:
                    car.steering = 0.8
                    print(f"▶▶ [RIGHT] 우측 10도 이상 치우침 ({avg_angle:.1f}°) -> 우회전")
                else:
                    car.steering = 0.0
                    print(f"▲▲ [STRAIGHT] 정면 10도 범위 내 유지 중 ({avg_angle:.1f}°)")
                
                # 모터 기동 (데드존 극복 출력)
                car.forward(50)
            else:
                print("[SEARCHING] 토스된 타겟 없음 -> 탐색 정지 대기")
                car.stop()
                car.steering = 0.0
            
            # 제어 루프 주기 정렬 (라이다 토스 속도와 발맞춤)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n[SYSTEM] 사용자에 의해 강제 종료 요청됨")
        
    # 4. 클린업 프로세스
    is_running = False
    time.sleep(0.2)  # 스레드가 안전하게 멈추는 시간 확보
    car.stop()
    car.steering = 0.0
    lidar.stopMotor()
    print("[SYSTEM] 멀티스레드 제어 주행이 안전하게 종료되었습니다.")