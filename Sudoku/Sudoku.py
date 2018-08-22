import numpy as np
from numpy.ma import zeros

import sys

DATA_SIZE0 = 2
DATA_SIZE = DATA_SIZE0 * DATA_SIZE0


def print_board(board):
    """問題/答え出力"""
    for bo in board:
        for b in bo:
            if b == 0:
                print("-", end="")
            else:
                print(int(b), end="")
            print(" ", end="")
        print()
    print()


def block(values, x, y, i):
    """3x3のチェック"""
    xbase = (x // DATA_SIZE0) * DATA_SIZE0
    ybase = (y // DATA_SIZE0) * DATA_SIZE0
    return all(True if i != values[_y][_x] else False
               for _y in range(ybase, ybase + DATA_SIZE0)
               for _x in range(xbase, xbase + DATA_SIZE0))


def column(values, x, i):
    """縦軸のチェック"""
    return all(True if i != values[_y][x] else False for _y in range(DATA_SIZE))


def row(values, y, i):
    """横軸のチェック"""
    return all(True if i != values[y][_x] else False for _x in range(DATA_SIZE))


def check(values, x, y, i):
    """値のチェック"""
    if row(values, y, i) and column(values, x, i) and block(values, x, y, i):
        return True
    return False


def solve(values, x=0, y=0):
    """数独解析"""
    print("[途中経過]")
    print_board(values)
    if y > DATA_SIZE - 1: #ポインタが最後までいったら完成
        print("[答え]")
        print_board(values)
        return True
    elif values[y][x] != 0: #空欄ではないなら飛ばす
        if x == DATA_SIZE -1: #8列までいったら次の行に移動
            if solve(values, 0, y+1):
                return True
        else:
            if solve(values, x+1, y):
                return True
    else:
        for i in range(1, DATA_SIZE + 1):#1から9までの数字を全て試す
            if check(values, x, y, i): #チェックする
                values[y][x] = i #OKなら数字を入れる
                if x == DATA_SIZE - 1: #8列までいったら次の行に移動
                    if solve(values, 0, y+1):
                        return True
                else:
                    if solve(values, x+1, y):
                        return True
        values[y][x] = 0 #戻ってきたら0に戻す
        return False

# /************************************************************************
# メインプログラム
# ************************************************************************/
def main(arg):
    if len(arg) == 1:
        print("使用法 : ./Sudoku.py 問題ファイル")
        board = np.loadtxt('mondai1.dat', delimiter=" ")    # Load Sample
    else:
        board = np.loadtxt(arg[1], delimiter=" ")   # 問題読み込み

    print("[問題]")
    print_board(board)
    solve(board, 0, 0)


if __name__ == "__main__":
    args = sys.argv
    main(args)
