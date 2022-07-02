import numpy as np
import pieces
from process_data import renderPiece


# any empty cell with a solid cell above it
def holes(board):
	count = 0
	coords = []
	for row in range(1,20):
		for col in range(10):
			if (board[row][col] == 0) and (board[row-1][col] != 0):
				count += 1
				coords.append((row, col))
	return count, coords


# count number of rows with no empty cells
def line_clears(board):
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
	heights = [20] * 10
	for col in range(10):
		for row in range(20):
			if board[row][col] != 0:
				heights[col] = row
				break
	return heights


def render_board(board):
	for row in range(20):
		print(''.join(['#' if x != 0 else '.' for x in board[row]]))


# (x, y) = bottom left corner of the pieces hitbox
def render_piece(x, y, pieceID):
	piece_array = pieces.renders[pieceID]
	
	height = len(piece_array)
	width = len(piece_array[0])
	x -= (height - 1)

	coords = []

	for row in range(height):
		for col in range(width):
			if piece_array[row][col] == 1:
				coords.append((x+row, y+col))

	return coords


def is_valid_placement(board, tile_coords, holes):
	for (x, y) in tile_coords:
		# tile in solid block or hole
		if (board[x][y] != 0) or ((x, y) in holes):
			return False

	for (x, y) in tile_coords:
		_x = x + 1
		if _x == 20:
			return True
		if board[_x][y] != 0:
			return True

	return False



def get_placeable_area(board, pieceID='0x4'):
	heights = surface_heights(board)
	low_bound = max(heights)
	high_bound = max( 0, (min(heights) - 1) )

	max_col = 10 - pieces.col_offsets[pieceID]

	valids = []

	_, _holes = holes(board)

	for row in range(high_bound, low_bound):
		for col in range(0, max_col):
			tile_coords = render_piece(row, col, pieceID)

			if is_valid_placement(board, tile_coords, _holes):
				valids.append([pieceID, row, col])

				_board = np.zeros((20, 10))
				for (x, y) in tile_coords:
					_board[x][y] = 1
				render_board(_board)
	
	return valids
				

