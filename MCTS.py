import random
import math
import time

BOARD_SIZE = 8
PLAYER_NUM = 2
COMPUTER_NUM = 1
MAX_THINK_TIME = 60
direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


# 初始化棋盘数组
def getInitialBoard():
    board = {}

    for i in range(0, BOARD_SIZE):
        board[i] = {}

        for j in range(0, BOARD_SIZE):
            board[i][j] = 0

    board[BOARD_SIZE / 2 - 1][BOARD_SIZE / 2 - 1] = COMPUTER_NUM
    board[BOARD_SIZE / 2][BOARD_SIZE / 2] = COMPUTER_NUM

    board[BOARD_SIZE / 2 - 1][BOARD_SIZE / 2] = PLAYER_NUM
    board[BOARD_SIZE / 2][BOARD_SIZE / 2 - 1] = PLAYER_NUM

    return board


# 返回棋子数
def countTile(board, tile):
    stones = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if board[i][j] == tile:
                stones += 1

    return stones


# 返回一个颜色棋子可能的下棋位置
def possible_positions(board, tile):
    positions = []
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if board[i][j] != 0:
                continue
            if updateBoard(board, tile, i, j, checkonly=True) > 0:
                positions.append((i, j))
    return positions

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


# 是否是合法走法，如果合法返回需要翻转的棋子列表
def updateBoard(board, tile, i, j, checkonly=False):
    # 该位置已经有棋子或者出界了，返回False
    reversed_stone = 0

    # 临时将tile 放到指定的位置
    board[i][j] = tile
    if tile == 2:
        change = 1
    else:
        change = 2

    # 要被翻转的棋子
    need_turn = []
    for xdirection, ydirection in direction:
        x, y = i, j
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == change:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            # 一直走到出界或不是对方棋子的位置
            while board[x][y] == change:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            # 出界了，则没有棋子要翻转
            if not isOnBoard(x, y):
                continue
            # 是自己的棋子，中间的所有棋子都要翻转
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    # 回到了起点则结束
                    if x == i and y == j:
                        break
                    # 需要翻转的棋子
                    need_turn.append([x, y])
    # 将前面临时放上的棋子去掉，即还原棋盘
    board[i][j] = 0  # restore the empty space
    # 没有要被翻转的棋子，则走法非法。翻转棋的规则。
    for x, y in need_turn:
        if not (checkonly):
            board[i][j] = tile
            board[x][y] = tile  # 翻转棋子
        reversed_stone += 1
    return reversed_stone


# 蒙特卡洛树搜索
def mctsNextPosition(board):
    def ucb1(node_tuple, t, cval):
        name, nplayout, reward, childrens = node_tuple

        if nplayout == 0:
            nplayout = 0.00000000001

        if t == 0:
            t = 1

        return (reward / nplayout) + cval * math.sqrt(2 * math.log(t) / nplayout)

    def find_playout(tep_board, tile, depth=0):
        def eval_board(tep_board):
            player_tile = countTile(tep_board, PLAYER_NUM)
            computer_tile = countTile(tep_board, COMPUTER_NUM)
            if computer_tile > player_tile:
                return True
            return False
        if depth > 32:
            return eval_board(tep_board)
        turn_positions = possible_positions(tep_board, tile)

        # 查看是否可以在这个位置下棋
        if len(turn_positions) == 0:
            if tile == COMPUTER_NUM:
                neg_turn = PLAYER_NUM
            else:
                neg_turn = COMPUTER_NUM

            neg_turn_positions = possible_positions(tep_board, neg_turn)

            if len(neg_turn_positions) == 0:
                return eval_board(tep_board)
            else:
                tile = neg_turn
                turn_positions = neg_turn_positions

        # 随机放置一个棋子
        temp = turn_positions[random.randrange(0, len(turn_positions))]
        updateBoard(tep_board, tile, temp[0], temp[1])

        # 转换轮次
        if tile == COMPUTER_NUM:
            tile = PLAYER_NUM
        else:
            tile = COMPUTER_NUM

        return find_playout(tep_board, tile, depth=depth + 1)

    def expand(tep_board, tile):
        positions = possible_positions(tep_board, tile)
        result = []
        for temp in positions:
            result.append((temp, 0, 0, []))
        return result

    def find_path(root, total_playout):
        current_path = []
        child = root
        parent_playout = total_playout
        isMCTSTurn = True

        while True:
            if len(child) == 0:
                break
            maxidxlist = [0]
            cidx = 0
            if isMCTSTurn:
                maxval = -1
            else:
                maxval = 2

            for n_tuple in child:
                parent, t_playout, reward, t_childrens = n_tuple

                #实现最大最小搜索，电脑选择最大值，玩家选择最小值
                if isMCTSTurn:
                    cval = ucb1(n_tuple, parent_playout, 0.1)

                    if cval >= maxval:
                        if cval == maxval:
                            maxidxlist.append(cidx)
                        else:
                            maxidxlist = [cidx]
                            maxval = cval
                else:
                    cval = ucb1(n_tuple, parent_playout, -0.1)

                    if cval <= maxval:
                        if cval == maxval:
                            maxidxlist.append(cidx)
                        else:
                            maxidxlist = [cidx]
                            maxval = cval

                cidx += 1

            # 随机进行下棋，扩展
            maxidx = maxidxlist[random.randrange(0, len(maxidxlist))]
            parent, t_playout, reward, t_childrens = child[maxidx]
            current_path.append(parent)
            parent_playout = t_playout
            child = t_childrens
            isMCTSTurn = not (isMCTSTurn)

        return current_path

    root = expand(board, COMPUTER_NUM)
    current_board = getInitialBoard()
    current_board2 = getInitialBoard()
    start_time = time.time()

    for loop in range(0, 5000):

        # 思考最大时间限制
        if (time.time() - start_time) >= MAX_THINK_TIME:
            break

        # current_path是一个放置棋子的位置列表，根据此列表进行后续操作
        current_path = find_path(root, loop)

        tile = COMPUTER_NUM
        for temp in current_path:
            updateBoard(current_board, tile, temp[0], temp[1])
            if tile == COMPUTER_NUM:
                tile = PLAYER_NUM
            else:
                tile = COMPUTER_NUM

        #复制棋盘，因为会在find_playout函数修改了棋盘
        isWon = find_playout(current_board2, tile)

        #自顶向下传递参数
        child = root
        for temp in current_path:
            idx = 0
            for n_tuple in child:
                parent, t_playout, reward, t_childrens = n_tuple
                if temp[0] == parent[0] and temp[1] == parent[1]:
                    break
                idx += 1

            if temp[0] == parent[0] and temp[1] == parent[1]:
                t_playout += 1
                if isWon:
                    reward += 1
                if t_playout >= 5 and len(t_childrens) == 0:
                    t_childrens = expand(current_board, tile)

                child[idx] = (parent, t_playout, reward, t_childrens)

            child = t_childrens

    print("loop count: ", loop)
    max_avg_reward = -1
    mt_result = (0, 0)
    for n_tuple in root:
        parent, t_playout, reward, t_childrens = n_tuple

        if (t_playout > 0) and (reward / t_playout > max_avg_reward):
            mt_result = parent
            max_avg_reward = reward / t_playout

    return mt_result
