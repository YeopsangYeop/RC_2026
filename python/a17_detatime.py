import datetime

def main():
    now = datetime.datetime.now()
    if(9< now.hour < 12):
        print(f"현재 시각은 {now.hour}시 {now.minute}분으로 오전입니다")
    elif(now.hour < 9):
        print(f"현재 시각은 {now.hour}시 {now.minute}분으로 아침입니다")
    else:
        print(f"현재 시각은 {now.hour}시 {now.minute}분으로 오후입니다")

    print(f"{now.month}월", end=" ") #now.month is int type
    if( 3<= now.month <= 5):
        print("봄입니다")
    elif( 6<= now.month <= 8):
        print("여름입니다")
    elif( 9<= now.month <= 11):
        print("가을입니다")
    else:
        print("겨울입니다")

if __name__ == "__main__":
    main()