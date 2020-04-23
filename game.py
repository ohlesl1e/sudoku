import copy
import util
import time


def printGrid(grid):
	for i in range(0, 9):
		print(grid[i])


def genericSearch(gameState, searchType):
	frontier = ''
	if searchType == 'bfs':
		frontier = util.Queue()
	elif searchType == 'dfs':
		frontier = util.Stack()

	if gameState.grid[0][0] == 0:
		firstVal = gameState.getValue((0, 0))
		for v in firstVal:
			frontier.push((copy.deepcopy(gameState), [((0, 0), v)]))
	else:
		gameState.position = gameState.getNextPos()
		firstVal = gameState.getValue()
		for v in firstVal:
			frontier.push((copy.deepcopy(gameState), [(gameState.position, v)]))
	while not frontier.isEmpty():
		current, steps = frontier.pop()
		newState, val = current.getSuccessors(steps[-1][1])
		if len(val) == 0:
			if current.isEndState():
				return steps
			continue
		for v in val:
			frontier.push((copy.deepcopy(newState), steps + [(newState.position, v)]))
	return []


def DFS(gameState):
	return genericSearch(gameState, 'dfs')


def BFS(gameState):
	return genericSearch(gameState, 'bfs')


class State:
	def __init__(self, currentGrid, position):
		self.grid = currentGrid
		self.fixed = []
		for i in range(0, 9):
			for j in range(0, 9):
				if not self.grid[i][j] == 0:
					self.fixed.append((i, j))
		self.position = position

	def getSuccessors(self, value):
		x, y = self.position
		if self.grid[x][y] == 0:
			self.grid[x][y] = value
		nextPos = self.getNextPos()
		nextValue = self.getValue(nextPos)
		return State(self.grid, nextPos), nextValue

	def getNextPos(self):
		x, y = self.position
		if self.grid[x][y] == 0:
			return x, y
		while True:
			y = y + 1
			if y > 8:
				y = y % 9
				if x < 8:
					x += 1
			if self.grid[x][y] == 0:
				break
			if x == 8 and y == 8 and not self.grid[x][y] == 0:
				break

		return x, y

	def isEndState(self):
		for x in range(0, 9):
			if 0 in self.grid[x]:
				return False
		return True

	def getRow(self, pos):
		return self.grid[pos[0]]

	def getCol(self, pos):
		col = []
		for x in range(0, 9):
			col.append(self.grid[x][pos[1]])
		return col

	def squareList(self, x1, x2, y1, y2):
		square = []
		for x in range(x1, x2):
			for y in range(y1, y2):
				square.append(self.grid[x][y])
		return square

	def getSquare(self, pos):
		x, y = pos
		if 0 <= x < 3:
			if 0 <= y < 3:
				return self.squareList(0, 3, 0, 3)
			elif 3 <= y < 6:
				return self.squareList(0, 3, 3, 6)
			else:
				return self.squareList(0, 3, 6, 9)
		elif 3 <= x < 6:
			if 0 <= y < 3:
				return self.squareList(3, 6, 0, 3)
			elif 3 <= y < 6:
				return self.squareList(3, 6, 3, 6)
			else:
				return self.squareList(3, 6, 6, 9)
		else:
			if 0 <= y < 3:
				return self.squareList(6, 9, 0, 3)
			elif 3 <= y < 6:
				return self.squareList(6, 9, 3, 6)
			else:
				return self.squareList(6, 9, 6, 9)

	def getValue(self, pos=None):
		if pos is None:
			pos = self.position
		row = self.getRow(pos)
		col = self.getCol(pos)
		square = self.getSquare(pos)
		value = []
		for v in range(1, 10):
			if v not in row and v not in col and v not in square:
				value.append(v)
		return value


if __name__ == '__main__':
	gameGrid = [
		[9, 0, 0, 0, 0, 0, 0, 4, 0],
		[0, 1, 7, 5, 0, 0, 0, 0, 0],
		[0, 0, 0, 8, 6, 0, 2, 0, 1],
		[0, 0, 0, 0, 5, 0, 7, 0, 0],
		[5, 9, 0, 0, 0, 0, 0, 3, 6],
		[0, 0, 6, 0, 8, 0, 0, 0, 0],
		[4, 0, 9, 0, 3, 1, 0, 0, 0],
		[0, 0, 0, 0, 0, 8, 3, 6, 0],
		[0, 3, 0, 0, 0, 0, 0, 0, 4]
	]

	state = State(gameGrid, (0, 0))

	searchFunction = ["bfs", "dfs"]

	print("Before")
	printGrid(gameGrid)

	for f in range(0, 2):
		function = ''
		postGrid = copy.deepcopy(gameGrid)
		result = []
		timeSpent = 0
		startTime = time.time()
		if f == 0:
			function = "\nBreadth First Search(runtime: "
			result = BFS(state)
		elif f == 1:
			function = "\nDepth First Search(runtime: "
			result = DFS(state)
		function = function + str(time.time() - startTime) + ")"

		for r in result:
			resultPos, resultValue = r
			postGrid[resultPos[0]][resultPos[1]] = resultValue
		print(function)
		printGrid(postGrid)
