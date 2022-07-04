import numpy as np
from process_frame import create_screen_channel, create_piece_channel


def getAction(action_vec):
	max_idx = np.argmax(action_vec)
	cont = [0] * 10
	cont[max_idx] = 1
	return ''.join(str(x) for x in cont)


def getFrame(conn):
	data = conn.recv(1024)
	screen, cur_piece, next_piece, reward, game_over, dropped = data.decode().split('\n')
	y, piece_id, x = cur_piece.split(',')
	piece_id = str(hex(int(piece_id)))
	next_piece_id = str(hex(int(next_piece)))

	# process the frame
	frame_array = []
	frame_array.append(create_screen_channel(screen))
	frame_array.append(create_piece_channel(piece_id, int(x), int(y)))
	frame_array.append(create_piece_channel(next_piece_id))
	frame_array = np.asarray(frame_array)

	return frame_array, int(reward), (game_over == '1'), piece_id, dropped


def action_vec(action):
	return [int(x) for x in list(action)]


def get_rotation_dir(pid, target_pid):
	rots = {
		'0x7': {'0x4':'right', '0x5':'right', '0x6':'left'},
		'0x12': {'0x11':'right'},
		'0xe': {'0xd':'left', '0xf':'right', '0x10':'right'},
		'0x2': {'0x0':'right', '0x1':'left', '0x3':'right'}
	}
	if pid in rots.keys():
		return rots[pid][target_pid]
	else:
		return 'right'


def render_board(board):
	for row in range(20):
		print(''.join(['#' if x != 0 else '.' for x in board[row]]))


def get_piece_column(frame):
	col_num = 0
	for col in frame[1].T:
		if sum(col) != 0:
			return col_num
		else:
			col_num += 1