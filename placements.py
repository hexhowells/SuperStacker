import pieces
from evaluation import _holes


def _surface_heights(board):
	heights = [20] * 10
	for col in range(10):
		for row in range(20):
			if board[row][col] != 0:
				heights[col] = row
				break
	return heights


# (x, y) = bottom left corner of the pieces hitbox
def _get_tile_coords(x, y, pieceID):
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


def _is_valid_placement(board, tile_coords, holes):
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


def get_placeable_area(board, pieceID):
	heights = _surface_heights(board)
	low_bound = max(heights)
	high_bound = max( 0, (min(heights) - 1) )

	max_col = 10 - pieces.col_offsets[pieceID]

	valids = []

	_, holes = _holes(board)

	for row in range(high_bound, low_bound):
		for col in range(0, max_col):
			tile_coords = _get_tile_coords(row, col, pieceID)

			if _is_valid_placement(board, tile_coords, holes):
				valids.append([pieceID, tile_coords, col, row])
	
	return valids