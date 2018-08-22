import sys

MAN = 0
WOLF = 1
GOAT = 2
CABBAGE = 3
SEARCH_MAX = 20

left_side = [[]]
right_side = [[]]


def print_state(state):
    out = ''
    ans = [' 男 ', ' 狼 ', ' 山羊 ', ' キャベツ ']
    for index, state in enumerate(state):
        if state == 1:
            out += ans[index]
    return '[{0}]'.format(out)


def print_ans(_step):
    for i in range(_step + 1):
        print('{0}:{1}:{2}'.format(i, print_state(left_side[i]), print_state(right_side[i])))


def check_state(t, state, past_state):
    if state[1] == 1 and state[2] == 1 or state[2] == 1 and state[3] == 1:
        return 0

    for i in range(t):
        if state == past_state[i][:]:
            return 0
    return 1


def search(t, src_side, dest_side):
    src_state = [i for i in src_side[t][:]]
    dest_state = [i for i in dest_side[t][:]]

    for index, state in enumerate(src_state):
        if state == 1:
            new_src_state = src_state[:]
            new_dest_state = dest_state[:]
            new_src_state[index] = new_src_state[0] = 0
            new_dest_state[index] = new_dest_state[0] = 1

            if check_state(t, new_src_state, src_side):
                if t % 2 == 0:
                    left_side[t + 1][:] = new_src_state
                    right_side[t + 1][:] = new_dest_state

                else:
                    left_side[t + 1][:] = new_dest_state
                    right_side[t + 1][:] = new_src_state

                if right_side[t + 1][:] == [1, 1, 1, 1]:
                    print_ans(t + 1)
                    print('test')
                    sys.exit(0)
                else:
                    if t == SEARCH_MAX:
                        print("探索回数上限")
                    else:
                        search(t + 1, dest_side, src_side)


def main():
    global left_side, right_side
    left_side = [[-1 for _ in range(4)] for _ in range(SEARCH_MAX)]
    right_side = [[-1 for _ in range(4)] for _ in range(SEARCH_MAX)]
    left_side[0][:] = [1, 1, 1, 1]
    right_side[0][:] = [0, 0, 0, 0]

    search(0, left_side, right_side)


if __name__ == '__main__':
    main()
