import numpy as np

import sys

__author__ = "Shota Harikae"
__version__ = "1.0"
__date__ = "23 Aug 2018"


class Sudoku:
    def __init__(self, data_size, file_patch):
        self.DATA_SIZE0 = data_size
        self.DATA_SIZE = self.DATA_SIZE0 * self.DATA_SIZE0
        self.board = np.loadtxt(file_patch, delimiter=" ")

    @staticmethod
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

    def __block(self, values, x, y, i):
        """3x3のチェック"""
        xbase = (x // self.DATA_SIZE0) * self.DATA_SIZE0
        ybase = (y // self.DATA_SIZE0) * self.DATA_SIZE0
        return all(True if i != values[_y][_x] else False
                   for _y in range(ybase, ybase + self.DATA_SIZE0)
                   for _x in range(xbase, xbase + self.DATA_SIZE0))

    def __column(self, values, x, i):
        """縦軸のチェック"""
        return all(True if i != values[_y][x] else False for _y in range(self.DATA_SIZE))

    def __row(self, values, y, i):
        """横軸のチェック"""
        return all(True if i != values[y][_x] else False for _x in range(self.DATA_SIZE))

    def __check(self, values, x, y, i):
        """値のチェック"""
        if self.__row(values, y, i) and self.__column(values, x, i) and self.__block(values, x, y, i):
            return True
        return False

    def solve(self, values, x=0, y=0):
        """数独解析"""
        print("[途中経過]")
        self.print_board(values)
        if y > self.DATA_SIZE - 1:
            print("[答え]")
            self.print_board(values)
            return True
        elif values[y][x] != 0:                                # 空欄ではないなら飛ばす
            if x == self.DATA_SIZE - 1:                        # 8列までいったら次の行に移動
                if self.solve(values, 0, y+1):
                    return True
            else:
                if self.solve(values, x+1, y):
                    return True
        else:
            for i in range(1, self.DATA_SIZE + 1):            # 1から9までの数字を試す
                if self.__check(values, x, y, i):             # チェック
                    values[y][x] = i                          # OKなら数字を入れる
                    if x == self.DATA_SIZE - 1:               # 8列までいったら次の行に移動
                        if self.solve(values, 0, y+1):
                            return True
                    else:
                        if self.solve(values, x+1, y):
                            return True
            values[y][x] = 0                             # 戻ってきたら0に戻す
            return False


def main(arg):
    """
    メインプログラム
    :param arg: 範囲と問題fileのパスの配列
    :return: None
    """
    if len(arg) == 3:
        su = Sudoku(int(arg[1]), arg[2])         # クラス初期化,問題読み込み
    else:
        print("使用法 : ./Sudoku.py 問題ファイル")
        su = Sudoku(3, 'mondai1.dat')       # Load Sample

    print("[問題]")                          # 問題を解く
    su.print_board(su.board)
    su.solve(su.board, 0, 0)


if __name__ == "__main__":
    args = sys.argv
    main(args)
