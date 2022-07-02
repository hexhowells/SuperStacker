import numpy as np
from process_data import screenBuffer, renderPiece, pieceChannel


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

	# process the frame
	frame_array = []
	frame_array.append(screenBuffer(screen))
	frame_array.append(renderPiece(int(x), int(y), piece_id))
	frame_array.append(pieceChannel(str(hex(int(next_piece)))))
	frame_array = np.asarray(frame_array)

	return frame_array, int(reward), (game_over == '1'), piece_id, dropped


def action_vec(action):
	return [int(x) for x in list(action)]
