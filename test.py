import time
import logging
import logging.handlers
from neuromeka import IndyDCP3 # DigitalState, TaskTeleopType

robot_ip = '192.168.0.100'
indy = IndyDCP3(robot_ip)
# idle_state = False

# while True:
# a=indy.get_di()
# print(a)

# def getDi():
# while True:
#     t1=indy.get_di()["signals"][1]
#     t2=indy.get_di()["signals"][2]
#     t3=indy.get_di()["signals"][3]
#     t4=indy.get_di()["signals"][4]
#     print(t1, t2, t3, t4)
#     time.sleep(0.5) 
    
def setup_logger():
    """시간 기반으로 파일을 회전시키는 로거를 설정합니다."""
    
    # 1. 로거 인스턴스 생성
    logger = logging.getLogger('IndyStatusLogger')
    logger.setLevel(logging.INFO)  # 로그 레벨 설정 (INFO 이상만 기록)

    # 2. 로그 포맷 설정 (시간 - 메시지 형식)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 3. TimedRotatingFileHandler 설정
    #    - 'indy_di.log': 로그 파일의 기본 이름
    #    - when='M': 회전 주기를 '분(Minute)'으로 설정
    #    - interval=2: 2분마다 파일을 새로 생성
    #    - backupCount=30: 최대 30개의 백업 로그 파일을 유지 (30 * 2분 = 1시간)
    handler = logging.handlers.TimedRotatingFileHandler(
        'indy_di.log', 
        when='M', 
        interval=2, 
        backupCount=30,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)

    # 4. 로거에 핸들러 추가
    logger.addHandler(handler)

    # 콘솔에도 로그를 출력하고 싶다면 아래 주석을 해제하세요.
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)

    return logger

def main():
    logger = setup_logger()
    while True:
        try:
            # DI(Digital Input) 신호 가져오기
            di_signals = indy.get_di()["signals"]
            
            # 필요한 신호 추출
            t1 = di_signals[1]
            t2 = di_signals[2]
            t3 = di_signals[3]
            t4 = di_signals[4]
            
            # 로그 메시지 생성 및 기록
            log_message = f"DI Signals - T1: {t1}, T2: {t2}, T3: {t3}, T4: {t4}"
            logger.info(log_message)
            
            # 콘솔에도 현재 상태 출력 (확인용)
            print(log_message)
            
            # 0.5초 대기
            time.sleep(0.5)
            
        except Exception as e:
            error_message = f"데이터 수신 중 오류 발생: {e}"
            logger.error(error_message)
            print(error_message)
            time.sleep(5) # 오류 발생 시 5초 후 재시도
if __name__=='__main__':
    main()