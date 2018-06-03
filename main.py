import random
from sys import maxsize


# Represents one of the 4 boards in the game
class Board:
    name = None
    rightRot = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    leftRot = [2, 5, 8, 1, 4, 7, 0, 3, 6]

    def __init__(self, name):
        self.name = name
        self.tiles = ['*', '*', '*', '*', '*', '*', '*', '*', "*"]

    def moveRight(self):
        print(str(self.name) + " Moving Right")

        temp = ['*', '*', '*', '*', '*', '*', '*', '*', "*"]
        for i in range(0, 9):
            temp[self.leftRot[i]] = self.tiles[i]
        self.tiles = temp

    def moveLeft(self):
        print(str(self.name) + " Moving Left")

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
            self.player1 = "w"
            self.player2 = "b"
        else:
            self.player1 = "b"
            self.player2 = "w"
            print("AI's turn")

    def getBoardCopy(self):
        allBoards = []
        allBoards.append(list(self.block1.tiles))
        allBoards.append(list(self.block2.tiles))
        allBoards.append(list(self.block3.tiles))
        allBoards.append(list(self.block4.tiles))
        return allBoards

    def playTurn(self, node):
        choice = None

        if self.turn:
            if self.player1 == "w":
                choice = input("Player 1: Enter your move: ")
            elif self.player2 == "w":
                print("Player 2 is making its move: ", end="")
                tree = Node(0, 1, "w", 0, game.getBoardCopy(), "")
                bestChoice = -maxsize
                decision = None
                for i in range(len(tree.children)):
                    val = minMax(tree.children[i], 0, -1)
                    if val > bestChoice:
                        bestChoice = val
                        decision = tree.children[i].decision
                choice = decision
                print(choice)
        else:
            if self.player1 == "b":
                choice = input("Player 1: Enter your move: ")
            elif self.player2 == "b":

                print("Player 2 is making its move: ", end="")

                tree = Node(0, -1, "b", 0, game.getBoardCopy(), "")
                bestChoice = -maxsize
                decision = None
                for i in range(len(tree.children)):
                    val = minMax(tree.children[i], 0, -1)
                    if val > bestChoice:
                        bestChoice = val
                        decision = tree.children[i].decision
                choice = decision
                print(choice)
        if choice is not None:
            place, rot = choice.split(" ")

            if self.turn:
                self.doMove(self.player1, int(place[0]), int(place[2]), int(rot[0]), rot[1])
                self.turn = 0
            else:
                self.doMove(self.player2, int(place[0]), int(place[2]), int(rot[0]), rot[1])
                self.turn = 1
        self.printGame()

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
            print("INVALID block/position")
            return False

        if not (dir == "L" or dir == "l" or dir == "R" or dir == "r"):
            print("INVALID direction")
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
            return False

    def printGame(self):
        print("+-------+-------+")
        for i in range(0, 9, 3):
            print("|", end="")
            print(" " + self.block1.tiles[i], end="")
            print(" " + self.block1.tiles[i + 1], end="")
            print(" " + self.block1.tiles[i + 2], end="")
            print(" " + "|", end="")
            print(" " + self.block2.tiles[i], end="")
            print(" " + self.block2.tiles[i + 1], end="")
            print(" " + self.block2.tiles[i + 2], end="")
            print(" " + "|", end="")
            print()
        print("+-------+-------+")
        for i in range(0, 9, 3):
            print("|", end="")
            print(" " + self.block3.tiles[i], end="")
            print(" " + self.block3.tiles[i + 1], end="")
            print(" " + self.block3.tiles[i + 2], end="")
            print(" " + "|", end="")
            print(" " + self.block4.tiles[i], end="")
            print(" " + self.block4.tiles[i + 1], end="")
            print(" " + self.block4.tiles[i + 2], end="")
            print(" " + "|", end="")
            print()
        print("+-------+-------+")


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
            for i in range(0, 4):
                for j in range(0, 9):
                    if self.boards[i][j] == '*':
                        choice = str(i + 1) + "/" + str(j + 1) + " " + str(random.randint(1, 4)) + self.rotate()
                        tempBoards = self.copyBoards()
                        tempBoards[i][j] = self.playerColor
                        self.children.append(Node(self.depth + 1,
                                                  self.playerNum * -1,
                                                  self.switchColor(),
                                                  self.realValue(),
                                                  list(tempBoards), choice))

    def realValue(self):
        return 1

    def rotate(self):
        rot = random.randint(1, 2)
        if rot == 1:
            return "L"
        else:
            return "R"

    def switchColor(self):
        if self.playerColor == "w":
            return "b"
        else:
            return "w"

    def copyBoards(self):
        copy = []
        copy.append(list(self.boards[0]))
        copy.append(list(self.boards[1]))
        copy.append(list(self.boards[2]))
        copy.append(list(self.boards[3]))
        return copy


# MinMax Algorithm to get move
def minMax(node, depth, playerNum):
    if depth == 2 or len(node.children) == 0:
        return node.value

    if playerNum == 1:
        bestValue = -maxsize
        for i in node.children:
            v = minMax(i, depth + 1, -1)
            if v > bestValue:
                bestValue = v
        return bestValue
    else:
        bestValue = maxsize
        for i in node.children:
            v = minMax(i, depth + 1, 1)
            if v < bestValue:
                bestValue = v
        return bestValue


############ MAIN PROGRAM #############


# Start game
game = Game()

# Generate the game tree
tree = None
maxPlayer = 0
if game.player1 == "w":
    tree = Node(0, -1, "w", 0, game.getBoardCopy(), "")
    maxPlayer = -1
else:
    tree = Node(0, 1, "w", 0, game.getBoardCopy(), "")
    maxPlayer = 1

# Play game
while not game.gameOver:
    game.playTurn(tree)
    # print("MINMAX RESULT: " + str(minMax(tree, 0, maxPlayer)))
