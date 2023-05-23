import copy

class SixSidedDie:
    side_values = [None, None, None, None, None, None]
    score = 0
    xpos = 0
    ypos = 0
    move_count = 0
    top = 1
    bottom = 6
    up = 4
    down = 3
    left = 2
    right = 5
    score_history = []
    pos_history = []


    def __init__(self, side_values, top, bottom, up, down, left, right, score, xpos, ypos, move_count, score_history, pos_history):
        self.side_values = side_values
        self.top = top
        self.bottom = bottom
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.score = score
        self.xpos = xpos
        self.ypos = ypos
        self.move_count = move_count
        self.score_history = score_history
        self.pos_history = pos_history

    def __str__(self):
        str_die = f"Orientation top: {self.top} up: {self.up} right: {self.right}"  + "\n" + f"side values: {str(self.side_values)}" + "\n" + f"xpos: {self.xpos} ypos: {self.ypos}" + "\n" + f"score: {self.score} move count: {self.move_count}" + "\n"
        return str_die

    def getMoveCount(self):
        return self.move_count

    def incMoveCount(self):
        self.move_count += 1

    def getSideValue(self, side):
        return self.side_values[side - 1]

    def setSideValue(self, side, val):
        self.side_values[side - 1] = val

    def getOrientationAfterMoveLeft(self):
        new_top = self.right
        new_bottom = self.left
        new_right = self.bottom
        new_left = self.top
        return (new_top, new_bottom, self.up, self.down, new_left, new_right)

    def getOrientationAfterMoveRight(self):
        new_top = self.left
        new_bottom = self.right
        new_right= self.top
        new_left = self.bottom
        return (new_top, new_bottom, self.up, self.down, new_left, new_right)


    def getOrientationAfterMoveUp(self):
        new_top = self.down
        new_bottom = self.up
        new_down = self.bottom
        new_up = self.top
        return (new_top, new_bottom, new_up, new_down, self.left, self.right)


    def getOrientationAfterMoveDown(self):
        new_top = self.up
        new_bottom = self.down
        new_up = self.bottom
        new_down = self.top
        return (new_top, new_bottom, new_up, new_down, self.left, self.right)



    def getOrientationAfterMove(self, move):
        if move == "left":
            return self.right
        if move == "right":
            return self.left
        if move == "up":
            return self.down
        if move == "down":
            return self.up

    def getNextPossibleMoves(self):
        moves = []

        # horizontal moves
        if self.xpos > 0:
            moves.append((self.xpos - 1, self.ypos, self.getOrientationAfterMove("left"), self.getOrientationAfterMoveLeft()))
        if self.xpos < 5:
            moves.append((self.xpos + 1, self.ypos, self.getOrientationAfterMove("right"), self.getOrientationAfterMoveRight()))
        # vertical moves
        if self.ypos > 0:
            moves.append((self.xpos, self.ypos - 1, self.getOrientationAfterMove("down"), self.getOrientationAfterMoveDown()))
        if self.ypos < 5:
            moves.append((self.xpos, self.ypos + 1, self.getOrientationAfterMove("up"), self.getOrientationAfterMoveUp()))

        return moves

    def getCurrentSide(self):
        if self.current_side_on_top is None:
            return self.side1
        return self.current_side_on_top




# initialize the grid
grid = [[0, 77, 32, 403, 337, 452],
        [5, 23, -4, 592, 445, 620],
        [-7, 2, 357, 452, 317, 395],
        [186, 42, 195, 704, 452, 228],
        [81, 123, 240, 443, 353, 508],
        [57, 33, 132, 268, 492, 732]]

def answer(die):
    die.score_history.append(die.score)
    die.pos_history.append((die.xpos, die.ypos))
    if die.xpos == 5 and die.ypos == 5:
        print(die.score_history)
        print(die.pos_history)
        print(die)
        return die

    for move in die.getNextPossibleMoves():
        x, y, orientation, all_sides_orientation = move
        new_top, new_bottom, new_left, new_right, new_up, new_down = all_sides_orientation
        score_required = grid[y][x]
        current_score = die.score

        if die.getSideValue(orientation) is None:
            new_dice = SixSidedDie(copy.deepcopy(die.side_values), new_top, new_bottom, new_left, new_right, new_up,
                                   new_down, score_required, x, y, die.move_count + 1, copy.deepcopy(die.score_history), copy.deepcopy(die.pos_history))
            new_dice_side_val = (score_required - current_score) / (die.move_count + 1)
            new_dice.setSideValue(orientation, new_dice_side_val)
            answer(new_dice)
        else:
            if current_score + (die.getMoveCount() + 1) * die.getSideValue(orientation) == score_required:
                new_dice = SixSidedDie(copy.deepcopy(die.side_values), new_top, new_bottom, new_left, new_right, new_up,
                                       new_down, score_required, x, y, die.move_count + 1, copy.deepcopy(die.score_history), copy.deepcopy(die.pos_history))
                answer(new_dice)


die = SixSidedDie([None, None, None, None, None, None], 1, 6, 5, 2, 4, 3, 0, 0, 0, 0, [], [])

answer(die)

score_history = [0, 5, 23, -4, 32, 77, 23, 2, 42, 123, 33, 132, 240, 123, 81, 186, 42, 195, 357, 452, 592, 403, 337, 452, 620, 395, 317, 452, 704, 443, 353, 508, 732]

pos_his = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (2, 4), (1, 4), (0, 4), (0, 3), (1, 3), (2, 3), (2, 2), (3, 2), (3, 1), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (4, 2), (3, 2), (3, 3), (3, 4), (4, 4), (5, 4), (5, 5)]

grid_seen = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

for x, y in pos_his:
    # print(f"{x}, {y}")
    grid_seen[y][x] = 1

grid_list = []
for row in grid:
    grid_list += row

seen_list = []
for row in grid_seen:
    seen_list += row

print(grid_list)
print(seen_list)

sum = 0
for i in range(len(seen_list)):
    if seen_list[i] == 0:
        sum += grid_list[i]

print(f"The answer is: {sum}")
