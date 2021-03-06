import random
from sys import maxsize


# Represents one of the 4 boards in the game
import copy


class Board:
    name = None
    rightRot = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    leftRot = [2, 5, 8, 1, 4, 7, 0, 3, 6]

    def __init__(self, name):
        self.name = name
        self.tiles = ['*', '*', '*', '*', '*', '*', '*', '*', "*"]

    def moveRight(self):
        #print(str(self.name) + " Moving Right")

        temp = ['*', '*', '*', '*', '*', '*', '*', '*', "*"]
        for i in range(0, 9):
            temp[self.leftRot[i]] = self.tiles[i]
        self.tiles = temp

    def moveLeft(self):
        #print(str(self.name) + " Moving Left")

        temp = ['*', '*', '*', '*', '*', '*', '*', '*', "*"]
        for i in range(0, 9):
            temp[self.rightRot[i]] = self.tiles[i]
        self.tiles = temp

    def placePiece(self, piece, pos):
        if self.tiles[pos] == '*':
            self.tiles[pos] = piece
            return True
        else:
            return False

    def printSimpleBoard(self):

        for i in range(0, 9):
            if i % 3 == 0:
                print()
            print(self.tiles[i] + " ", end='')


# Represents the full game board
class Game:
    block1 = Board("Block1")
    block2 = Board("Block1")
    block3 = Board("Block3")
    block4 = Board("Block4")
    player1 = None
    player2 = None
    gameOver = False

    # 1 = White, 0 = Black
    turn = 1

    def __init__(self):
        choose = random.randint(0, 1)
        if choose:
            print("Your Turn: Player 1")
            file.write("Player 1: You - White")
            file.write("\n")
            file.write("Player 2: AI - Black\n\n")
            self.player1 = "w"
            self.player2 = "b"
        else:
            self.player1 = "b"
            self.player2 = "w"
            file.write("Player 1: AI - White")
            file.write("\n")
            file.write("Player 2: You - Black")
            file.write("\n\n")
            print("AI's turn")

    def getBoardCopy(self):
        allBoards = []
        allBoards.append(copy.deepcopy(self.block1))
        allBoards.append(copy.deepcopy(self.block2))
        allBoards.append(copy.deepcopy(self.block3))
        allBoards.append(copy.deepcopy(self.block4))

        return allBoards

    def playTurn(self):
        choice = None

        if self.turn:
            if self.player1 == "w":
                choice = input("Player 1: Enter your move: ")
                file.write("Player 1 (w) made the move: " + choice + "\n")
            elif self.player2 == "w":
                print("AI thinking...")
                print("Player 2 is making its move: ", end="")
                tree = Node(0, 1, "w", 0, game.getBoardCopy(), "")
                bestChoice = -maxsize
                decision = None
                for i in range(len(tree.children)):

                    # val = minMax(tree.children[i], 0, -1)
                    val = minMaxAlphaBeta(tree.children[i], 0, -maxsize, maxsize, -1)
                    if val > bestChoice:
                        bestChoice = val
                        decision = tree.children[i].decision
                choice = decision
                print(choice)
                file.write("Player 2 (w) made the move: " + choice + "\n")
        else:
            if self.player1 == "b":
                choice = input("Player 1: Enter your move: ")
                file.write("Player 1 (b) made the move: " + choice + "\n")
            elif self.player2 == "b":
                print("AI thinking...")
                print("Player 2 is making its move: ", end="")

                tree = Node(0, 1, "b", 0, game.getBoardCopy(), "")
                bestChoice = -maxsize
                decision = None
                for i in range(len(tree.children)):

                    # val = minMax(tree.children[i], 0, -1)
                    val = minMaxAlphaBeta(tree.children[i], 0, -maxsize, maxsize, 1)
                    if val > bestChoice:
                        bestChoice = val
                        decision = tree.children[i].decision
                choice = decision
                print(choice)
                file.write("Player 2 (b) made the move: " + choice + "\n")
        if choice is not None:
            try:
                place, rot = choice.split(" ")
                if self.turn:
                    report = self.doMove(self.player1, int(place[0]), int(place[2]), int(rot[0]), rot[1])
                    if not report:
                        print("Try Again")
                        file.write("\nTry Again\n")
                    else:
                        self.turn = 0
                else:
                    self.doMove(self.player2, int(place[0]), int(place[2]), int(rot[0]), rot[1])
                    self.turn = 1
            except ValueError:
                print("Wrong Characters")
                file.write("\nWrong Characters\n")

        self.printGame()

        self.checkWinner()

    def getBlock(self, num):
        if num == 1:
            return self.block1
        elif num == 2:
            return self.block2
        elif num == 3:
            return self.block3
        else:
            return self.block4

    def doMove(self, color, block, pos, block2, dir):

        # Check input
        if block < 1 or block2 < 1 or block > 4 or block2 > 4 or pos < 1 or pos > 9:
            print("\nINVALID block/position\n")
            file.write("\nINVALID block/position")
            return False

        if not (dir == "L" or dir == "l" or dir == "R" or dir == "r"):
            print("INVALID direction")
            file.write("\nINVALID direction\n")
            return False

        # do move
        pickedBlock = self.getBlock(int(block))
        valid = pickedBlock.placePiece(color, pos - 1)

        # do rotate
        if valid:
            pickedBlock = self.getBlock(int(block2))
            if dir == "L" or dir == "l":
                pickedBlock.moveLeft()
            else:
                pickedBlock.moveRight()
            return True
        else:
            print("INVALID piece already there")
            file.write("\nINVALID piece already there\n")
            return False

    # Check the winner of the game
    def checkWinner(self):

        # Copy the game board into 1D array for easy checking

        board = []

        board.extend(copy.deepcopy(self.block1.tiles[0:3]))
        board.extend(copy.deepcopy(self.block2.tiles[0:3]))

        board.extend(copy.deepcopy(self.block1.tiles[3:6]))
        board.extend(copy.deepcopy(self.block2.tiles[3:6]))

        board.extend(copy.deepcopy(self.block1.tiles[6:]))
        board.extend(copy.deepcopy(self.block2.tiles[6:]))

        board.extend(copy.deepcopy(self.block3.tiles[0:3]))
        board.extend(copy.deepcopy(self.block4.tiles[0:3]))

        board.extend(copy.deepcopy(self.block3.tiles[3:6]))
        board.extend(copy.deepcopy(self.block4.tiles[3:6]))

        board.extend(copy.deepcopy(self.block3.tiles[6:]))
        board.extend(copy.deepcopy(self.block4.tiles[6:]))


        countb = 0
        streakb = 0

        countw = 0
        streakw = 0

        tie = True

        # Check Vertical
        for i in range(0, 6):
            for j in range(0, 6):
                mul = j * 6
                if board[i + mul] == 'w':
                    countw += 1
                else:
                    if countw > streakw:
                        streakw = countw
                    countw = 0

                if board[i + mul] == 'b':
                    countb += 1
                else:
                    if countb > streakb:
                        streakb = countb
                    countb = 0
                if countw > streakw:
                    streakw = countw
                if countb > streakb:
                    streakb = countb


        countw = 0
        countb = 0

        # Check Horizontal
        for i in range(0, 6):
            for j in range(0, 6):
                mul = i * 6
                if board[mul + j] == 'w':
                    countw += 1
                else:
                    if countw > streakw:
                        streakw = countw
                    countw = 0
                if board[mul + j] == 'b':
                    countb += 1
                else:
                    if countb > streakb:
                        streakb = countb
                    countb = 0
                if countw > streakw:
                    streakw = countw
                if countb > streakb:
                    streakb = countb

        countw = 0
        countb = 0

        # Check Diagonal Right
        for i in range(0, 3):

            start = i
            if i == 2:
                start = 6

            countw = 0
            countb = 0
            for j in range(0, 6):

                mul = j * 7
                if start == 1 or start == 6 and j == 5:
                    break
                if board[start + mul] == 'w':
                    countw += 1
                else:
                    if countw > streakw:
                        streakw = countw
                    countw = 0
                if board[start + mul] == 'b':
                    countb += 1
                else:
                    if countb > streakb:
                        streakb = countb
                    countb = 0
                if countw > streakw:
                    streakw = countw
                if countb > streakb:
                    streakb = countb

        countw = 0
        countb = 0

        # Check Diagonal Left
        for i in range(4, 7):

            start = i
            if i == 6:
                start = 11

            countw = 0
            countb = 0
            for j in range(0, 6):

                mul = j * 5
                if start == 4 or start == 11 and j == 5:
                    break
                if board[start + mul] == 'w':
                    countw += 1
                else:
                    if countw > streakw:
                        streakw = countw
                    countw = 0
                if board[start + mul] == 'b':
                    countb += 1
                else:
                    if countb > streakb:
                        streakb = countb
                    countb = 0
                if countw > streakw:
                    streakw = countw
                if countb > streakb:
                    streakb = countb

        # Check if winner
        if streakw >= 5 and streakb >= 5:
            self.gameOver = True
            print("TIE")
            file.write("\nTIE\n")
        elif streakw >= 5:
            self.gameOver = True
            print("WINNER: W")
            file.write("\nWINNER: W\n")
        elif streakb >= 5:
            self.gameOver = True
            print("WINNNER: B")
            file.write("\nWINNER: B\n")

        # Lastly check for a tie game
        for i in range(0, 35):
            if board[i] == '*':
                tie = False
        if tie:
            self.gameOver = True
            print("TIE")
            file.write("\nTIE\n")

    def printGame(self):
        print("+-------+-------+")
        file.write("+-------+-------+\n")
        for i in range(0, 9, 3):
            print("|", end="")
            file.write("|")
            print(" " + self.block1.tiles[i], end="")
            file.write(" " + self.block1.tiles[i])
            print(" " + self.block1.tiles[i + 1], end="")
            file.write(" " + self.block1.tiles[i + 1])
            print(" " + self.block1.tiles[i + 2], end="")
            file.write(" " + self.block1.tiles[i + 2])
            print(" " + "|", end="")
            file.write(" |")
            print(" " + self.block2.tiles[i], end="")
            file.write(" " + self.block2.tiles[i])
            print(" " + self.block2.tiles[i + 1], end="")
            file.write(" " + self.block2.tiles[i + 1])
            print(" " + self.block2.tiles[i + 2], end="")
            file.write(" " + self.block2.tiles[i + 2])
            print(" " + "|", end="")
            file.write(" |\n")
            print()
        print("+-------+-------+")
        file.write("+-------+-------+\n")
        for i in range(0, 9, 3):
            print("|", end="")
            file.write("|")
            print(" " + self.block3.tiles[i], end="")
            file.write(" " + self.block3.tiles[i])
            print(" " + self.block3.tiles[i + 1], end="")
            file.write(" " + self.block3.tiles[i + 1])
            print(" " + self.block3.tiles[i + 2], end="")
            file.write(" " + self.block3.tiles[i + 2])
            print(" " + "|", end="")
            file.write(" |")
            print(" " + self.block4.tiles[i], end="")
            file.write(" " + self.block4.tiles[i])
            print(" " + self.block4.tiles[i + 1], end="")
            file.write(" " + self.block4.tiles[i + 1])
            print(" " + self.block4.tiles[i + 2], end="")
            file.write(" " + self.block4.tiles[i + 2])
            print(" " + "|", end="")
            file.write(" |\n")
            print()
        print("+-------+-------+")
        file.write("+-------+-------+\n")

# Represents a Node in the tree
class Node:
    depth = 0
    playerColor = None
    value = None
    playerNum = None
    decision = ""

    def __init__(self, depth, num, color, value, boards, decision):
        self.depth = depth
        self.children = []
        self.decision = decision
        self.playerColor = color
        self.playerNum = num
        self.value = value
        self.boards = boards
        self.createChildren()

    def createChildren(self):
        if self.depth < 2:
            # First 2 loops to get position
            for i in range(0, 4):
                for j in range(0, 9):
                    # Next 2 loops to get rotations
                    for k in range(0, 4):
                        for l in range(0, 2):

                            if self.boards[i].tiles[j] == '*':
                                rot = self.rotate(l)
                                choice = str(i + 1) + "/" + str(j + 1) + " " + str(random.randint(1, 4)) + rot
                                tempBoards = self.copyBoards()
                                tempBoards[i].placePiece(self.playerColor, j)
                                if rot == "L":
                                    tempBoards[k].moveLeft()
                                else:
                                    tempBoards[k].moveRight()

                                tempNode = Node(self.depth + 1, self.playerNum + -1, self.switchColor(), 0, list(tempBoards), choice)
                                tempNode.value = tempNode.realValue()
                                self.children.append(tempNode)

    def realValue(self):

        # Check for pairs of...
        # Copy the game board into 1D array for easy checking

        board = []

        board.extend(copy.deepcopy(self.boards[0].tiles[0:3]))
        board.extend(copy.deepcopy(self.boards[1].tiles[0:3]))

        board.extend(copy.deepcopy(self.boards[0].tiles[3:6]))
        board.extend(copy.deepcopy(self.boards[1].tiles[3:6]))

        board.extend(copy.deepcopy(self.boards[0].tiles[6:]))
        board.extend(copy.deepcopy(self.boards[1].tiles[6:]))

        board.extend(copy.deepcopy(self.boards[2].tiles[0:3]))
        board.extend(copy.deepcopy(self.boards[3].tiles[0:3]))

        board.extend(copy.deepcopy(self.boards[2].tiles[3:6]))
        board.extend(copy.deepcopy(self.boards[3].tiles[3:6]))

        board.extend(copy.deepcopy(self.boards[2].tiles[6:]))
        board.extend(copy.deepcopy(self.boards[3].tiles[6:]))

        countb = 0
        streakb = 0

        countw = 0
        streakw = 0

        tie = True

        # Check Vertical
        for i in range(0, 6):
            for j in range(0, 6):
                mul = j * 6
                if board[i + mul] == 'w':
                    countw += 1
                else:
                    if countw > streakw:
                        streakw = countw
                    countw = 0

                if board[i + mul] == 'b':
                    countb += 1
                else:
                    if countb > streakb:
                        streakb = countb
                    countb = 0
        countw = 0
        countb = 0

        # Check Horizontal
        for i in range(0, 6):
            for j in range(0, 6):
                mul = i * 6
                if board[mul + j] == 'w':
                    countw += 1
                else:
                    if countw > streakw:
                        streakw = countw
                    countw = 0
                if board[mul + j] == 'b':
                    countb += 1
                else:
                    if countb > streakb:
                        streakb = countb
                    countb = 0

        finalVal = maxVal(streakw, streakb)
        return finalVal

    def findMathcing(self, index, board):
        count = 1

        # current piece to check aginst others
        current = board[index]

        if current == self.playerColor:

            # checking bottom
            if index + 6 < 35:
                if current == board[index + 6]:
                    count += 1
            # Checking top
            if index - 6 > 0:
                if current == board[index - 6]:
                    count += 1
            # Checking right
            if index + 1 < 35 and index % 5 != 0:
                if current == board[index + 1]:
                    count += 1
            # Checking left
            if index - 1 > 0 and index % 6 != 0:
                if current == board[index - 1]:
                    count += 1
        return count


    def rotate(self, int):
        if int == 1:
            return "L"
        else:
            return "R"

    def switchColor(self):
        if self.playerColor == "w":
            return "b"
        else:
            return "w"

    def copyBoards(self):
        dc = []
        dc.append(copy.deepcopy(self.boards[0]))
        dc.append(copy.deepcopy(self.boards[1]))
        dc.append(copy.deepcopy(self.boards[2]))
        dc.append(copy.deepcopy(self.boards[3]))

        return dc


# MinMax with Alpha Beta Pruning
def minMaxAlphaBeta(node, depth, alpha, beta, playerNum):

    global depthMMAB1
    global depthMMAB2
    if depth == 0:
        depthMMAB1 += 1
    elif depth == 1:
        depthMMAB2 += 1

    if depth == 2 or len(node.children) == 0:
        return node.value

    # Max player
    if playerNum == 1:
        value = -maxsize
        for i in node.children:
            rec = minMaxAlphaBeta(i, depth + 1, alpha, beta, -1)
            value = maxVal(value, rec)
            alpha = maxVal(alpha, value)
            if beta <= alpha:
                break
        return value

    # Min Player
    if playerNum == -1:
        value = maxsize
        for i in node.children:
            rec = minMaxAlphaBeta(i, depth + 1, alpha, beta, 1)
            value = minVal(value, rec)
            beta = minVal(beta, value)
            if beta <= alpha:
                break
        return value

def minVal(val1, val2):
    if val1 == None:
        return val2
    elif val2 == None:
        return val1

    if val1 <= val2:
        return val1
    elif val2 <= val1:
        return val2
    elif val2 == val1:
        return val1

def maxVal(val1, val2):
    if val1 > val2:
        return val1
    elif val2 > val1:
        return val2
    elif val1 == val2:
        return val1


# MinMax Algorithm to get move
def minMax(node, depth, playerNum):

    global depthMM1
    global depthMM2

    if depth == 0:
        depthMM1 += 1
    elif depth == 1:
        depthMM2 += 1

    if depth == 2 or len(node.children) == 0:
        return node.value

    if playerNum == 1:
        bestValue = -maxsize
        for i in node.children:
            v = minMax(i, depth + 1, -1)
            if v == None: v = 0
            if v > bestValue:
                bestValue = v
        return bestValue
    else:
        bestValue = maxsize
        for i in node.children:
            v = minMax(i, depth + 1, 1)
            if v == None: v = 0
            if v < bestValue:
                bestValue = v
        return bestValue

############ MAIN PROGRAM #############

depthMM1 = 0
depthMM2 = 0

depthMMAB1 = 0
depthMMAB2 = 0

file = open("Output.txt", "w")

# Start game
game = Game()
game.printGame()

# Play game
while not game.gameOver:
    game.playTurn()
    # print("Nodes expanded at depth 1 in MinMax:: " + str(depthMM1))
    # print("Nodes expanded at depth 2 in MinMax:: " + str(depthMM2))
    #
    # print("Nodes expanded at depth 1 in MinMax AlphaBeta: " + str(depthMMAB1))
    # print("Nodes expanded at depth 2 in MinMax AlphaBeta: " + str(depthMMAB2))

    depthMM1 = 0
    depthMM2 = 0

    depthMMAB1 = 0
    depthMMAB2 = 0
file.close()