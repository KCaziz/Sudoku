#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def string_line(line:str) -> list:
    ''' requires |line| = 81 '''
    _in = line.replace('.','0')
    return [int(x) for x in _in]

class Reader:
     ''' sudoku blocks' reader '''
     def __init__(self, fname:str):
         print(f'loading {fname} ...')
         with open(fname, 'r') as f:
             lines = f.readlines()
         self.lines = []
         for l in lines: self.lines.extend([int(x) for x in l.strip()])
         zeros = self.lines.count(0)
         if __debug__: print(f"missing {zeros}/81 {100*zeros/81:.2f}%")


if __name__ == '__main__':
    fname = 'data/easy_00.txt'
    print("Reader is 'r'")
    r = Reader(fname)
    print(f"{r.lines = }")
    puzzle = ''.join([str(x) for x in r.lines]).replace('0', '.')
    print(f"{puzzle = }")
    print(f"test string_line(puzzle) == r.lines: "
          f"{string_line(puzzle)==r.lines}")
