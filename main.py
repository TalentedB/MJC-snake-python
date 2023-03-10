import random
import typing
import math



def info() -> typing.Dict:
	print("INFO")

	return {
	 "apiversion": "1",
	 "author": "Talented",  # TODO: Your Battlesnake Username
	 "color": "#F1F1F1",  # TODO: Choose color
	 "head": "snow-worm",  # TODO: Choose head
	 "tail": "block-bum",  # TODO: Choose tail
	 "version": "0.0.1-beta"
	}


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
	print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
	#print(game_state)
	print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:

	set_of_moves = {"up": True, "down": True, "left": True, "right": True}

	my_head = game_state["you"]["body"][0]  # Coordinates of your head
	my_health = game_state["you"]["health"]
	my_length = game_state["you"]["length"]
	#Grab the bad positions and safe moves
	bad_positions, is_move_safe = check_possible_moves(game_state, my_head)

	enemy_heads, dangerous_enemy_head_moves = get_enemy_snake_movement_info(
	 game_state, my_head, my_length)

	if {'x': my_head['x'], 'y': my_head['y'] + 1} in dangerous_enemy_head_moves:
		is_move_safe['up'] = False
	if {'x': my_head['x'], 'y': my_head['y'] - 1} in dangerous_enemy_head_moves:
		is_move_safe['down'] = False
	if {'x': my_head['x'] - 1, 'y': my_head['y']} in dangerous_enemy_head_moves:
		is_move_safe['left'] = False
	if {'x': my_head['x'] + 1, 'y': my_head['y']} in dangerous_enemy_head_moves:
		is_move_safe['right'] = False

	# Are there any safe moves left?
	safe_moves = []
	for move, isSafe in is_move_safe.items():
		if isSafe:
			safe_moves.append(move)
	#If there are no safe moves, move randomly.
	if len(safe_moves) == 0:
		print(
		 f"MOVE {game_state['turn']}: No safe moves detected! Moving towards enemy death zones"
		)
		#return {"move": set_of_moves[random.randint(0, 3)]}
		bad_positions, is_move_safe = check_possible_moves(game_state, my_head)
		for move, isSafe in is_move_safe.items():
			if isSafe:
				safe_moves.append(move)
		if len(is_move_safe):
			return {
			 "move":
			 move_to_closest_food(dangerous_enemy_head_moves, my_head, safe_moves)
			}
		else:
			return {
			 "move":
			 move_to_closest_food(dangerous_enemy_head_moves, my_head, set_of_moves)
			}
	# Choose a random move from the safe ones
	next_move = random.choice(safe_moves)

	#enemy_heads, dangerous_enemy_head_moves = get_enemy_snake_movement_info(game_state, my_head, my_length)

	next_move = move_to_closest_food(enemy_heads, my_head, safe_moves)
	# next_move = _make_a_choice(my_head, bad_positions, safe_moves, {
	#  'x': game_state['board']['width'],
	#  'y': game_state['board']['height']
	# })

	#If Health is below 50 then B line it to food or its the start of the game
	food = game_state['board']['food']
	if my_health < 50 or game_state['turn'] < 20 or len(enemy_heads) == 0:
		next_move = move_to_closest_food(food, my_head, safe_moves)
	
	print(f"MOVE {game_state['turn']}: {next_move}")
	return {"move": next_move}


#Determine the closest food
def closest_food(grocerys, head):
	smallest_distance = 10000
	for food in grocerys:
		# distance = math.dist({head['x'], head['y']}, {food['x'], food['y']})

		distance = math.dist(head.values(), food.values())
		if distance < smallest_distance:
			smallest_distance = distance

	return smallest_distance


#Move towards the closest object in the list
def move_to_closest_food(grocerys, head, possible_moves):
	distances = {}
	for move in possible_moves:
		if move == "up":
			distances[move] = closest_food(grocerys, {
			 'x': head['x'],
			 'y': head['y'] + 1
			})
		if move == "down":
			distances[move] = closest_food(grocerys, {
			 'x': head['x'],
			 'y': head['y'] - 1
			})
		if move == "left":
			distances[move] = closest_food(grocerys, {
			 'x': head['x'] - 1,
			 'y': head['y']
			})
		if move == "right":
			distances[move] = closest_food(grocerys, {
			 'x': head['x'] + 1,
			 'y': head['y']
			})

	return min(distances, key=distances.get)


#Check the possible moves
def check_possible_moves(game_state, my_head):
	bad_positions = []
	is_move_safe = {"up": True, "down": True, "left": True, "right": True}
	board_width = game_state['board']['width']
	board_height = game_state['board']['height']
	#print(my_head["x"], my_head["y"])
	if my_head["x"] + 1 == board_width:
		is_move_safe["right"] = False
	if my_head["x"] == 0:
		is_move_safe["left"] = False
	if my_head["y"] == 0:
		is_move_safe["down"] = False
	if my_head["y"] + 1 == board_height:
		is_move_safe["up"] = False

	# TODO: Step 2 - Prevent your Battlesnake from colliding with itself

	my_body = game_state['you']['body']
	for i, body_part in enumerate(my_body):
		bad_positions.append(body_part)
		if i == len(my_body) - 1:
			#print("break")
			break
		if body_part['x'] == my_head['x'] + 1 and body_part['y'] == my_head['y']:
			is_move_safe["right"] = False
		if body_part['x'] == my_head['x'] - 1 and body_part['y'] == my_head['y']:
			is_move_safe["left"] = False
		if body_part['x'] == my_head['x'] and body_part['y'] == my_head['y'] - 1:
			is_move_safe["down"] = False
		if body_part['x'] == my_head['x'] and body_part['y'] == my_head['y'] + 1:
			is_move_safe["up"] = False

	# TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
	opponents = game_state['board']['snakes']
	for snakes in opponents:
		for i, body_part in enumerate(snakes["body"]):

			if i == len(snakes["body"]) - 1:
				#print("break")
				break
			bad_positions.append(body_part)
			if body_part['x'] == my_head['x'] + 1 and body_part['y'] == my_head['y']:
				is_move_safe["right"] = False
			if body_part['x'] == my_head['x'] - 1 and body_part['y'] == my_head['y']:
				is_move_safe["left"] = False
			if body_part['x'] == my_head['x'] and body_part['y'] == my_head['y'] - 1:
				is_move_safe["down"] = False
			if body_part['x'] == my_head['x'] and body_part['y'] == my_head['y'] + 1:
				is_move_safe["up"] = False
	return bad_positions, is_move_safe


# Start server when `python main.py` is run


#Determine where snakes can move
def get_enemy_snake_movement_info(game_state, my_head, my_length):
	enemy_heads = []
	dangerous_enemy_head_moves = []
	for snake in game_state['board']['snakes']:
		if snake['body'][0] == my_head:
			continue
		if (len(game_state['board']['snakes']) <= 2 and snake['length'] < my_length and math.dist(my_head.values(), snake['body'][0].values()) < 10 ) or (len(game_state['board']['snakes']) > 2 and snake['length'] < my_length and math.dist(my_head.values(), snake['body'][0].values()) < 4):
			enemy_heads.append({
			 'x': snake['body'][0]['x'] + 1,
			 'y': snake['body'][0]['y']
			})
			enemy_heads.append({
			 'x': snake['body'][0]['x'],
			 'y': snake['body'][0]['y'] - 1
			})
			enemy_heads.append({
			 'x': snake['body'][0]['x'] - 1,
			 'y': snake['body'][0]['y']
			})
			enemy_heads.append({
			 'x': snake['body'][0]['x'],
			 'y': snake['body'][0]['y'] + 1
			})
		elif snake['length'] >= my_length:
			dangerous_enemy_head_moves.append({
			 'x': snake['body'][0]['x'] + 1,
			 'y': snake['body'][0]['y']
			})
			dangerous_enemy_head_moves.append({
			 'x': snake['body'][0]['x'],
			 'y': snake['body'][0]['y'] - 1
			})
			dangerous_enemy_head_moves.append({
			 'x': snake['body'][0]['x'] - 1,
			 'y': snake['body'][0]['y']
			})
			dangerous_enemy_head_moves.append({
			 'x': snake['body'][0]['x'],
			 'y': snake['body'][0]['y'] + 1
			})
	return enemy_heads, dangerous_enemy_head_moves


#Flood Fill
def _count_spaces(currSpaces, noGo, block, board_size):
	# one to the right
	if _right_of(block) in noGo or _right_of(block) in currSpaces or _right_of(
	  block)['x'] == board_size['x']:
		pass
	else:
		currSpaces.append(_right_of(block))
		currSpaces = _count_spaces(currSpaces, noGo, _right_of(block), board_size)
	# one to the left
	if _left_of(block) in noGo or _left_of(block) in currSpaces or _left_of(
	  block)['x'] == -1:
		pass
	else:
		currSpaces.append(_left_of(block))
		currSpaces = _count_spaces(currSpaces, noGo, _left_of(block), board_size)
	# one to the down
	if _down_of(block) in noGo or _down_of(block) in currSpaces or _down_of(
	  block)['y'] == -1:
		pass
	else:
		currSpaces.append(_down_of(block))
		currSpaces = _count_spaces(currSpaces, noGo, _down_of(block), board_size)
	# one to the up
	if _up_of(block) in noGo or _up_of(block) in currSpaces or _up_of(
	  block)['y'] == board_size['y']:
		pass
	else:
		currSpaces.append(_up_of(block))
		currSpaces = _count_spaces(currSpaces, noGo, _up_of(block), board_size)

	return currSpaces



def number_of_bigger_snakes(snakes, my_length):
	amount = 0
	for snake in snakes:
		if snake['length'] >= my_length:
			amount += 1
	return amount

#Right of space
def _right_of(space):
	return {'x': space['x'] + 1, 'y': space['y']}


#Left of space
def _left_of(space):
	return {'x': space['x'] - 1, 'y': space['y']}


#Below space
def _down_of(space):
	return {'x': space['x'], 'y': space['y'] - 1}


#Above space
def _up_of(space):
	return {'x': space['x'], 'y': space['y'] + 1}


#Determine the best move to make
def _make_a_choice(my_head, bad_positions, possible_moves, board_size):
	moveRight = []
	moveLeft = []
	moveDown = []
	moveUp = []

	move_count = {
	 'right': moveRight,
	 'left': moveLeft,
	 'down': moveDown,
	 'up': moveUp
	}

	for i in possible_moves:
		currSpaces = []

		if i == 'right':
			moveRight.append(
			 len(
			  _count_spaces(currSpaces, bad_positions, _right_of(my_head), board_size)))
		if i == 'left':
			moveLeft.append(
			 len(_count_spaces(currSpaces, bad_positions, _left_of(my_head),
			                   board_size)))
		if i == 'down':
			moveDown.append(
			 len(_count_spaces(currSpaces, bad_positions, _down_of(my_head),
			                   board_size)))
		if i == 'up':
			moveUp.append(
			 len(_count_spaces(currSpaces, bad_positions, _up_of(my_head), board_size)))

	return max(move_count, key=move_count.get)


if __name__ == "__main__":
	from server import run_server

	run_server({"info": info, "start": start, "move": move, "end": end})
