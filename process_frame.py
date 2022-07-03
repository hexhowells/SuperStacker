import matplotlib.pyplot as plt
import numpy as np
import pieces

# 0 - frame buffer
# 1 - current piece [y, ID, x]
# 2 - controller vector
# 3 - next piece ID


def _renderPiece(x, _y, piece_id):
	blank_screen = [[0] * 10] * 20

	# return blank screen during line clear animation
	if piece_id == '0x13':
		return blank_screen

	# set the y offset
	y_offset = pieces.y_offsets[piece_id]
	y = _y - y_offset

	# scan over each used line on the screen
	for i, Y in enumerate(range(y, y+len(pieces.renders[piece_id]))):
		row = [0] * 10
		p_row = pieces.renders[piece_id][i]
		x_pos = x - pieces.x_offsets[piece_id]

		row[x_pos:x_pos+len(p_row)] = p_row
		blank_screen[Y] = row

	# if piece at top then clear bottom two lines (removes screen overflow)
	if y <= 1:
		blank_screen[-1] = [0] * 10
		blank_screen[-2] = [0] * 10
	
	return blank_screen


def create_piece_channel(piece_id, x=5, y=16):
	return _renderPiece(x, y, piece_id)


def create_screen_channel(screen):
	screen = [int(x) for x in screen.split(',')]
	channel = []

	for i in range(0, 200, 10):
		channel.append(screen[i:i+10])

	return channel
