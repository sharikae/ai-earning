import sys

MAN = 0
WOLF = 1
GOAT = 2
CABBAGE = 3
SEARCH_MAX = 20

__author__ = "Shota Harikae"
__version__ = "1.0"
__date__ = "23 Aug 2018"


class Wgcm:
    def __init__(self, left_side, right_side):
        self.left_side = left_side
        self.right_side = right_side

    @staticmethod
    def __print_state(state):
        """
        状態の表示
        配列の内容に応じて状態を表示する
        :param state: 左岸もしくは右岸の状態
        :return: 状態出力
        """

        out = ''
        ans = [' 男 ', ' 狼 ', ' 山羊 ', ' キャベツ ']
        for index, state in enumerate(state):
            if state == 1:
                out += ans[index]
        return '[{0}]'.format(out)

    @staticmethod
    def __check_state(t, state, past_state):
        """
        状態のチェック

        :param t: ステップ数
        :param state: チェックしたい状態
        :param past_state: 過去の状態
        :return: 狼と山羊、山羊とキャベツを残した状態でもなく、既に探索された状態
                 でもなければ TRUEを返す
                 それ以外は FALSEを返す
        """

        if state[1] == 1 and state[2] == 1 or state[2] == 1 and state[3] == 1:
            return False

        for i in range(t):
            if state == past_state[i][:]:
                return False
        return True

    def __print_ans(self, _step):
        for i in range(_step + 1):
            print('{0}:{1}:{2}'.format(i, self.__print_state(self.left_side[i]), self.__print_state(self.right_side[i])))

    def search(self, t, src_side, dest_side):
        """
        深さ優先探索

        :param t: ステップ数
        :param src_side: 男がいる側の状態
        :param dest_side: 男がいない側の状態
        :return: None
        """

        src_state = [i for i in src_side[t][:]]
        dest_state = [i for i in dest_side[t][:]]

        for index, state in enumerate(src_state):
            if state == 1:
                new_src_state = src_state[:]
                new_dest_state = dest_state[:]
                new_src_state[index] = new_src_state[0] = 0
                new_dest_state[index] = new_dest_state[0] = 1

                if self.__check_state(t, new_src_state, src_side):
                    if t % 2 == 0:
                        self.left_side[t + 1][:] = new_src_state
                        self.right_side[t + 1][:] = new_dest_state

                    else:
                        self.left_side[t + 1][:] = new_dest_state
                        self.right_side[t + 1][:] = new_src_state

                    if self.right_side[t + 1][:] == [1, 1, 1, 1]:
                        self.__print_ans(t + 1)

                    else:
                        if t == SEARCH_MAX:
                            print("探索回数上限")
                        else:
                            self.search(t + 1, dest_side, src_side)


def main():

    wgcm = Wgcm(                                                    # クラス初期化-1値を代入
        [[-1 for _ in range(4)] for _ in range(SEARCH_MAX)],
        [[-1 for _ in range(4)] for _ in range(SEARCH_MAX)]
    )
    wgcm.left_side[0][:] = [1, 1, 1, 1]                             # 全員を戻した状態に
    wgcm.right_side[0][:] = [0, 0, 0, 0]                            # 全員をいない状態に
    wgcm.search(0, wgcm.left_side, wgcm.right_side)                 # 探索開始


if __name__ == '__main__':
    main()
