import numpy as np


def get_value(board, piece, x, y):
	pass
	# evaluate based on following
	#   line clears
	#   addition block height
	#   holes
	#   wells


# any empty cell with a solid cell above it
def holes(board):
	count = 0
	for row in range(1,20):
		for col in range(10):
			if (board[row][col] == 0) and (board[row-1][col] != 0):
				count += 1
	return count


# count number of rows with no empty cells
def line_clear(board):
	count = 0
	for row in range(20):
		full = sum([1 if x != 0 else 0 for x in board[row]])
		if sum(full) == 10:
			count += 1
	return count


# any empty cell with solid cells on the right AND left
def wells(board):
	new_col = np.ones((20,1))
	board = np.hstack((new_col, board, new_col))

	count = 0
	for row in range(20):
		for col in range(1, 11):
			if board[row][col] == 0:
				if (board[row][col-1] != 0) and (board[row][col+1] != 0):
					count += 1
	return count


def block_height(board):
	rows = np.sum(board, axis=1)
	h_idx = np.nonzero(rows)[0]

	if len(h_idx) == 0:
		return 0
	else:
		inv_highest_row = h_idx[0]
		highest_row = 20 - inv_highest_row
		return highest_row


# new block height - current block height
# min value of 0 (negative means line clears)
def added_height(cur_height, new_height):
	return max(0, (new_height - cur_height))



def surface_heights(board):
	heights = [-1] * 10
	for col in range(10):
		for row in range(20):
			if board[row][col] != 0:
				heights[col] = row
				break
	return heights

