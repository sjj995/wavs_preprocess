import argparse
import sys
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input text file(Default: stdin)",
    )

    return parser.parse_args()


class Add_Times:
    h,m,s,ms = 0,0,0,0
    
    def __init__(self,hours,mins,seconds,milliseconds):
        self.hours = hours
        self.mins = mins
        self.seconds = seconds
        self.milliseconds = milliseconds
    
    def add_times(self,hours,mins,seconds,milliseconds):
    
        if Add_Times.ms+int(self.milliseconds) >= 100:
            Add_Times.s += (Add_Times.ms+int(self.milliseconds)) // 100
            Add_Times.ms = (Add_Times.ms+int(self.milliseconds)) % 100
        elif Add_Times.ms+int(self.milliseconds) < 100:
            Add_Times.ms += int(self.milliseconds)

        if Add_Times.s+int(self.seconds) >= 60:
            Add_Times.m += (Add_Times.s+int(self.seconds)) // 60
            Add_Times.s = (Add_Times.s+int(self.seconds)) % 60
        elif Add_Times.s+int(self.seconds) < 60:
            Add_Times.s += int(self.seconds)

        if Add_Times.m+int(self.mins) >= 60:
            Add_Times.h += (Add_Times.m+int(self.mins)) // 60
            Add_Times.m = (Add_Times.m+int(self.mins)) % 60
        elif Add_Times.m+int(self.mins) < 60:
            Add_Times.m += int(self.mins)

        Add_Times.h += int(self.hours)
    
        return Add_Times.h,Add_Times.m,Add_Times.s,Add_Times.ms
    

def main():
    args = get_args()

    if args.input is None :
        f = sys.stdin
    else :
        assert Path(args.input).is_file()
        f = open(args.input, "r")

    
    for line in f:
        line = line.replace('\n','')
        milliseconds = line[-2:]
        seconds = line[-5:-3]
        mins = line[3:5]
        hours = line[0:2]
        time_calculate = Add_Times(hours,mins,seconds,milliseconds)
        h,m,s,ms = time_calculate.add_times(hours,mins,seconds,milliseconds)
        
    
    print(f'해당 데이터의 오디오는 총 {h}시간 {m}분 {s}.{ms}초 입니다.')


if __name__ == "__main__":

    main()