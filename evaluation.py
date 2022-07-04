import numpy as np
import utils


# any empty cell with a solid cell above it
def _holes(board):
	count = 0
	coords = []
	for row in range(1,20):
		for col in range(10):
			if (board[row][col] == 0) and (board[row-1][col] != 0):
				count += 1
				coords.append((row, col))
	return count, coords


# count number of rows with no empty cells
def _line_clears(board):
	count = 0
	for row in range(20):
		full = sum([1 if x != 0 else 0 for x in board[row]])
		if full == 10:
			count += 1
	return count


# any empty cell with solid cells on the right AND left
def _wells(board):
	new_col = np.ones((20,1))
	board = np.hstack((new_col, board, new_col))

	count = 0
	for row in range(20):
		for col in range(1, 11):
			if board[row][col] == 0:
				if (board[row][col-1] != 0) and (board[row][col+1] != 0):
					count += 1
	return count


def _holes_and_wells(board):
	new_col = np.ones((20,1))
	board = np.hstack((new_col, board, new_col))

	hole_count = 0
	well_count = 0
	transitions = 0
	for row in range(20):
		prev_cell = 0
		for col in range(1, 11):
			cell = board[row][col]
			if cell == 0:
				# wells
				if (board[row][col-1] != 0) and (board[row][col+1] != 0):
					well_count += 1
				# holes
				if row != 0 and (board[row-1][col] != 0):
					hole_count += 1
			# transitions
			if cell != prev_cell:
				transitions += 1
			if (row != 0) and (cell != board[row-1][col]):
				transitions

			prev_cell = cell
				
	return hole_count, well_count, transitions


# highest placed block on the screen
def _block_height(board):
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
def _added_height(cur_height, new_height):
	return max(0, (new_height - cur_height))


# create array from individual tile coordinates
def _create_tile_array(tile_coords):
	_board = np.zeros((20, 10))
	for (x, y) in tile_coords:
		_board[x][y] = 1
	return _board


def get_value(board, pieceID, tile_coords, coords):
	piece_array = _create_tile_array(tile_coords)
	new_board = np.add(board, piece_array)

	cur_height = _block_height(board)
	new_height = _block_height(new_board)

	# individual value features
	lines_clears = _line_clears(new_board)

	if lines_clears != 0:
		board = utils.clear_lines(board)

	holes, wells, transitions = _holes_and_wells(new_board)
	#holes = _holes(new_board)
	#wells = _wells(new_board)

	added_height = _added_height(cur_height, new_height)

	# value calculation
	value = (lines_clears ** 2) - (holes * 4) - (wells) - (added_height) + (coords[1])

	return value
