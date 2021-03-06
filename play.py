import socket
import numpy as np
import random

import utils
from evaluation import get_value
import evaluation as ev
from placements import get_all_piece_placements
import pieces



def get_values(frame, piece_id, next_piece_id):
	values = []
	for (pid, t_coords, x, y) in get_all_piece_placements(frame, piece_id):
		val = get_value(frame, pid, t_coords, (x, y))
		values.append([val, pid, t_coords, x])

	return values


def get_best_location(values):
	best_val = -1_000_000
	location = {'pid':None, 'x':None, 'tile_coords':None}
	for (val, pid, t_coords, x) in reversed(values):
		if val > best_val:
			location['pid'] = pid
			location['x'] = x
			location['tile_coords'] = t_coords
			best_val = val

	return location


config = {
	'host':'127.0.0.1', 
	'port':65432, 
	'timeout':1.0
	}


actions = {
	'rotate_right': 2,
	'rotate_left': 8,
	'left': 3,
	'right': 9
}


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((config['host'], config['port']))
	sock.settimeout(config['timeout'])
	print("Listening on port {}".format(config['port']))

	prev_dropped = 0
	
	while True:
		action = [0,0,0,0,0,0,0,0,0,0]

		sock.listen()

		# allows for keyboard interrupt
		try:
			conn, addr = sock.accept()
		except socket.timeout:
			continue

		with conn:
			# process frame
			frame, piece_id, next_piece_id, dropped = utils.getFrame(conn)

			# only analyse board when new piece arrives
			if (dropped != prev_dropped):
				values = get_values(frame[0], piece_id, next_piece_id)
				location = get_best_location(values)

			#  rotate piece
			if location['pid'] != piece_id:
				action_str = "rotate_" + utils.get_rotation_dir(piece_id, location['pid'])
				action[actions[action_str]] = 1

			# move piece left or right
			p_col = utils.get_piece_column(frame)
			if p_col == None:
				pass
			elif location['x'] < p_col:
				action[actions['left']] = 1
			elif location['x'] > p_col:
				action[actions['right']] = 1

			# perform action
			if sum(action) > 0:
				action = ''.join([str(x) for x in action])
				conn.sendall(action.encode())
			else:
				conn.sendall('0000000000'.encode())
			
			prev_dropped = dropped
