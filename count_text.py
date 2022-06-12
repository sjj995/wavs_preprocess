#!/usr/bin/env python3
 # -*- coding: utf-8 -*-

#import os
import sys
import argparse



from pathlib import Path

#from trans import sentranslit as trans
#from g2pk import G2p
#g2p = G2p()
##from KoG2P.g2p import runKoG2P

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default="char",
        help="type option: char, word. "
        "    the type cat ",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input text file(Default: stdin)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output of count text file(Default: stdout). "
        "   Format: <item>\tcount",
    )

    return parser.parse_args()

def LINE():
    return sys._getframe(1).f_lineno

def main():
    args = get_args()

    print(args)

    items_dict = {}
    item_type = args.type.lower()

    #with open(args.input) as f:
    if args.input is None :
        f = sys.stdin
    else :
        assert Path(args.input).is_file()
        f = open(args.input, "r")

    if args.output is None :
        fw = sys.stdout
    else :
        fw = open(args.output, "w")

    for line in f:
        words = line.split()
        for word in words:
            if item_type == "word":
                if word not in items_dict:
                    items_dict[word] = 1
                else:
                    items_dict[word] += 1
            else:
                for char in word:
                    if char not in items_dict:
                        items_dict[char] = 1
                    else:
                        items_dict[char] += 1
    for key in sorted(items_dict) :
        print(f"{key}\t{items_dict[key]}", file = fw) 
    print(f"Total number of items: {len(items_dict)}") 
    f.close()
    fw.close()


if __name__ == "__main__":

    main()
