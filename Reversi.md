# 黑白棋


## 实验内容

​	黑白棋(Reversi)，也叫苹果棋，翻转棋，是一个经典的策略性游戏。一般棋子双面为黑白两色，故称“黑白棋”。因为行棋之时将对方棋子翻转，变为己方棋子，故又称“翻转棋”。它使用8x 8的棋盘，由两人执黑子和白子轮流下棋，最后子多方为胜方。

​	本实验将根据黑白棋的规则编写一个黑白棋AI，与玩家进行游戏。



## 实验要求

1. 使用MCTS算法实现miniAlphaGo for Reversi；
2. MCTS算法部分尽量自己实现，尽量不使用现有的包、工具或接口；
3. 在博弈过程中显示miniAlphaGo每一步所花费的时间以及总时间；
4. 需要有简单的图形界面用于人机交互；
5. 使用语言不限。



## 实验原理

### 蒙特卡洛树搜索

​	蒙特卡洛树搜索（简称 MCTS）是 Rémi Coulom 在2006年在它的围棋人机对战引擎中首次发明并使用，全称是Monte Carlo Tree Search，是一种人工智能问题中做出最优决策的方法，一般是在组合博弈中的行动规划形式，它结合了随机模拟的一般性和树搜索的准确性。

​	它一般有如下四步：

1. **选择**(Selection)：从根节点开始，递归选择最优的子节点直到达到叶子节点L。
2. **扩展** (expansion)：如果L不是一个终止节点，不会导致博弈游戏终止，那么就创建一个或者更多的字子节点，选择其中一个C。
3. **模拟**(Simluation)：从C开始运行一个模拟的输出，直到博弈游戏结束。
4. **回溯**(Backpropagation)：用模拟的结果输出更新当前行动序列。

​	每一步的详细介绍不再赘述，这里再介绍一下节点选择时的策略，有如下的函数：
$$
UCT(v_{i},v)=\frac{Q(v_{i})}{N(v_{i})}+C\sqrt{\frac{log(N(v))}{N(v_{i})}}
$$
​	其中，Q(v) 是该节点赢的次数，N(v) 是该节点模拟的次数，C 是一个常数。因此我们每次选择时，从根节点出发，遵循最大最小原则，每次选择己方 UCT 值最优的一个节点，向下搜索，直到找到一个未完全展开的节点，随机选择一个未访问的子节点进行扩展。

### Tkinter

​	 Tkinter模块（Tk 接口）是Python的标准Tk GUI工具包的接口，Python可以通过它快速创建GUI的界面。



## 实验过程

​	本次实验使用Python语言实现，利用tkinter图形界面库实现了友好的人机交互环境，下面针对每一个模块进行介绍。

​	首先实验建立了一个棋盘类：

```python
class ReversiBoard(Tk.Canvas)
```

​	棋盘类主要包含了对棋盘画布的各种动作，包括初始化、刷新、放置棋子、轮次转换等功能。同时定义了一些参数：

```python
 	cell_size = 46			#方格大小
    margin = 5				#间距偏移
    board = rvs.getInitialBoard()    #获得棋盘
    validBoard = True				#棋盘合法
    isPayerTurn = True				#玩家先行
    step = []						#记录步数
```

​	然后建立了棋盘的框架类，主要建立棋盘的主体框架：

```python
class Reversi(Tk.Frame)
```

​	最后是MCTS算法的核心部分，即蒙特卡洛搜索树的核心算法结构，另外建立mcts_reversi.py文件作为模块导入。棋盘定义一个8$\times$8的矩阵然后映射到棋盘画布的位置，矩阵内用棋子颜色替代棋子，各种操作主要针对矩阵，然后将每一步的矩阵变化映射到棋盘画布，刷新棋盘画布即可完成人机交互。

​	下面对每个部分的代码进行一个简要的介绍。

### 棋盘框架

​	主要代码如下：

```python
class Reversi(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("打败人工智障")
        l_title = Tk.Label(self, text='Reversi_AI', font=('Times', '24', ('italic', 'bold')), fg='#191970', bg='#EEE8AA',
                           width=12)
        l_title.pack(padx=10, pady=10)
        self.f_board = ReversiBoard(self)
        self.f_board.pack(padx=10, pady=10)
```

​	此部分代码主要是实现了棋盘画布的定义，此后对棋盘的各种操作都以此部分为基础。其中，Tk.Label()函数定义了画布的基本属性，包括文本、字体的相关属性。最后打包以备后续处理。

### 棋盘操作类

​	首先进行棋盘的初始化，完成棋盘的初始状态。

```python
    def __init__(self, master):
        cwidth = rvs.BOARD_SIZE * self.cell_size
        Tk.Canvas.__init__(self, master, relief=Tk.RAISED, bd=4, bg='white', width=cwidth, height=cwidth,cursor="cross")
        self.bind("<1>", self.put_stones)
        for i in range(rvs.BOARD_SIZE):
            for j in range(rvs.BOARD_SIZE):
                bcolor = "#808000"
                x0 = i * self.cell_size + self.margin
                y0 = j * self.cell_size + self.margin
                self.create_rectangle(x0, y0, x0 + self.cell_size, y0 + self.cell_size, fill=bcolor, width=1)

        self.refresh()
```

​	这里首先定义了棋子的大小，然后绑定鼠标左键点击事件，将四个棋子放置到合理位置，然后刷新，结果如下：

<img src="C:\Users\l\AppData\Roaming\Typora\typora-user-images\image-20210522050755888.png" alt="image-20210522050755888" style="zoom:60%;" />

​	棋盘初始化完成。

​	随后是放置棋子，放置棋子动作主要考虑玩家的动作，因为玩家移动鼠标点击的位置是一个范围，因此要对坐标进行转化，然后对点击的范围与位置进行判定是否合法，若合法则进行后续包括翻转棋子、轮次转换等步骤：

```python
    def put_stones(self, event):  # 放置棋子
        # 是否游戏结束
        if self.validBoard == False:
            self.validBoard = True
            self.board = rvs.getInitialBoard()
            self.isPayerTurn = True

            for numid in self.step:
                self.delete(numid)
            self.step = []
            self.refresh()
            return

        # 电脑轮次
        if not (self.isPayerTurn):
            return
        # 玩家轮次
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        # 获得坐标 根据方格大小计算
        i = int(x / self.cell_size)
        j = int(y / self.cell_size)
        #更新棋盘显示 if判断是否有合适的位置
        if self.board[i][j] != 0 or rvs.updateBoard(self.board, rvs.PLAYER_NUM, i, j, checkonly=True) == 0:
            return
        rvs.updateBoard(self.board, rvs.PLAYER_NUM, i, j)
        self.refresh()
        #人类下完 转换到电脑
        isPayerTurn = False
        self.after(100, self.AI_move)
```

​	一次玩家合法的点击结果：

<img src="C:\Users\l\AppData\Roaming\Typora\typora-user-images\image-20210522050622868.png" alt="image-20210522050622868" style="zoom:60%;" />

​	接下来是电脑的轮次：

```python
 def AI_move(self):
        while True:
            player_possibility = len(rvs.possible_positions(self.board, rvs.PLAYER_NUM))
            mcts_possibility = len(rvs.possible_positions(self.board, rvs.COMPUTER_NUM))
            if mcts_possibility == 0:
                break
            #获得一次运行时间
            start= time.time()
            stone_pos = rvs.mctsNextPosition(self.board)
            end =time.time()
            print("Computer position:", stone_pos)
            print("Step time:",format(end-start, '.4f'),"s")
            total.append(one_time)
            rvs.updateBoard(self.board, rvs.COMPUTER_NUM, stone_pos[0], stone_pos[1])
            self.refresh()

            player_possibility = len(rvs.possible_positions(self.board, rvs.PLAYER_NUM))
            mcts_possibility = len(rvs.possible_positions(self.board, rvs.COMPUTER_NUM))

            if mcts_possibility == 0 or player_possibility > 0:
                break

        if player_possibility == 0 and mcts_possibility == 0:
            self.showResult()
            self.validBoard = False

        self.isPayerTurn = True
```

​	这一部分主要是MCTS算法的入口部分，是电脑执子的时候执行的动作，首先根据黑白棋的规则判断电脑是否有地方可以下，然后执行蒙特卡洛树搜索返回一个下子的坐标，更新棋盘；然后判断是否游戏结束。电脑的一步下棋结果：

<img src="C:\Users\l\AppData\Roaming\Typora\typora-user-images\image-20210522052157407.png" alt="image-20210522052157407" style="zoom:60%;" />

​	游戏结束的条件就是人和电脑都没有位置可以下，根据棋子数有如下三种对局结果，在此情况下执行：

```python
    def showResult(self):
        player_stone = rvs.countTile(self.board, rvs.PLAYER_NUM)
        mcts_stone = rvs.countTile(self.board, rvs.COMPUTER_NUM)

        if player_stone > mcts_stone:
            tkinter.messagebox.showinfo('Game Over', "You won")

        elif player_stone == mcts_stone:
            tkinter.messagebox.showinfo('Game Over', "Draw")

        else:
            tkinter.messagebox.showinfo('Game Over', "You lose")
        print(sum(total))
```

​	如图所示为玩家胜利情况：

<img src="C:\Users\l\AppData\Roaming\Typora\typora-user-images\image-20210522051820113.png" alt="image-20210522051820113" style="zoom:60%;" />

​	下棋中间过程记录，记录题目要求的单步思考时间与总思考时间，思考时间与最大深度等参数有关：

<img src="C:\Users\l\AppData\Roaming\Typora\typora-user-images\image-20210522052129443.png" alt="image-20210522052129443" style="zoom:67%;" />

​	至此，棋盘的相关操作与结果已经介绍完毕，这一部分主要使用了Tk模块，可以看出这个模块对于创建应用程序GUI十分的方便。接下来介绍本次实验的核心部分，蒙特卡洛树搜索的实现。

### 蒙特卡洛树搜索函数

​	由于图形界面并不容易进行分析，所以蒙特卡洛树搜索部分使用映射的8$\times$8的矩阵，首先定义一些参数：

```python
BOARD_SIZE = 8				#矩阵大小
PLAYER_NUM = 2				#2代表黑棋
COMPUTER_NUM = 1			#1代表白棋
MAX_THINK_TIME = 60			#最大思考时间1min
direction=[[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]						#方向，根据此判断是否为一次合法下棋
```

​	然后是初始化矩阵：

```python
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
```

​	前面介绍的GUI棋盘的初始化就依赖于这个初始化的矩阵。

​	为了实现搜素算法，还需要各种辅助函数，主要包括寻找可以下棋的位置、是否到达边界、更新棋盘矩阵等等：

```python

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
    # 该位置已有棋子或者出界
    reversed_stone = 0
    

# 是否是合法走法，如果合法返回需要翻转的棋子列表
def updateBoard(board, tile, i, j, checkonly=False):
    # 该位置已经有棋子或者出界了，返回False
    reversed_stone = 0
    # 临时将tile放到指定的位置
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
            # 出界了，则没有棋子可以翻转
            if not isOnBoard(x, y):
                continue
            # 是自己的棋子，二者之间的棋子都要被翻转
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    # 回到了起点则结束
                    if x == i and y == j:
                        break
                    # 需要翻转的棋子
                    need_turn.append([x, y])
    # 将前面临时放上的棋子去掉
    board[i][j] = 0
    # 没有要被翻转的棋子，则走法非法。
    for x, y in need_turn:
        if not (checkonly):
            board[i][j] = tile
            board[x][y] = tile  # 翻转棋子
        reversed_stone += 1
    return reversed_stone
```

​	这里解释介绍一下updateBoard()函数，其返回需要被翻转的棋子个数，checkonly参数主要用来进行判断是否是仅仅用来检查，若为True，说明这个函数只是用来计算个数的；若为False，说明该函数还需将棋子翻转。具体运用情况见后续代码。

​	接下来是MCTS实现部分，代码如下：

```python

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
```

​	此部分函数主要是蒙特卡洛树搜索四个步骤的具体实现，定义模拟次数为5000次。基本思路是寻找最可能的节点，“最可能”定义为规定的模拟次数下获胜的次数最多。选择步骤根据计算的UCB的值，从根自顶向下进行最大最小搜索，直到找到一个可扩展的节点，随机选择其中一个叶子节点进行扩展，将刚刚选择的叶子节点加上一个统计信息为’0/0‘的节点，进入下一步模拟。模拟只进行一步走子即输出结果，利用函数判断输赢，更新本节点的输赢情况，已经被模拟的次数。最后进行回溯，从本节点开始，沿着刚刚向下的路径往回走，自底向上地沿途更新各个父节点的统计信息，即输赢与模拟次数的信息。

​	至此实现了整个MCTS的简单应用。

## 实验结果

​	基本实现了蒙特卡洛搜索树算法，应用到了黑白棋游戏中，并创建了友好的图形界面与交互，实现了题目的要求。具体单步的结果见实验过程。



## 实验总结

​	本次实验加深了我对蒙特卡洛树搜索的理解，并通过算法将其实现，将理论化为实际。在写代码过程中遇到很多困难，也查阅了很多相关资料，让我深深地感受到高级算法实现的复杂性。通过本次实验我还学会使用Python的GUI库，本实验还可以用图片来生成棋盘与棋子，后续改进可以将画布改为导入的图片，这样得到的界面更美观。总之通过本次实验我收获颇丰。
