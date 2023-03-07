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
	}


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
	print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
	print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:

	set_of_moves = {"up": True, "down": True, "left": True, "right": True}

	my_head = game_state["you"]["body"][0]  # Coordinates of your head
	my_health = game_state["you"]["health"]
	my_length = game_state["you"]["length"]
	#Grab the bad positions and safe moves
	bad_positions, is_move_safe = check_possible_moves(game_state, my_head)

	

	enemy_heads, dangerous_enemy_head_moves = get_enemy_snake_movement_info(game_state, my_head, my_length)

	if {'x': my_head['x'],'y': my_head['y'] + 1} in dangerous_enemy_head_moves:
		is_move_safe['up'] = False
	if {'x': my_head['x'],'y': my_head['y'] - 1} in dangerous_enemy_head_moves:
		is_move_safe['down'] = False
	if {'x': my_head['x'] - 1,'y': my_head['y']} in dangerous_enemy_head_moves:
		is_move_safe['left'] = False
	if {'x': my_head['x'] + 1,'y': my_head['y']} in dangerous_enemy_head_moves:
		is_move_safe['right'] = False
	
	# Are there any safe moves left?
	safe_moves = []
	for move, isSafe in is_move_safe.items():
		if isSafe:
			safe_moves.append(move)
	#If there are no safe moves, move randomly.
	if len(safe_moves) == 0:
		print(f"MOVE {game_state['turn']}: No safe moves detected! Moving randomly")
		return {"move": set_of_moves[random.randint(0, 3)]}

	# Choose a random move from the safe ones
	next_move = random.choice(safe_moves)


	#enemy_heads, dangerous_enemy_head_moves = get_enemy_snake_movement_info(game_state, my_head, my_length)
	print("attacking enemy")
	next_move = move_to_closest_food(enemy_heads, my_head, safe_moves)
	print(enemy_heads)

	#If Health is below 50 then B line it to food or its the start of the game
	food = game_state['board']['food']
	if my_health < 50 or game_state['turn'] < 20 or len(enemy_heads) == 0:
		next_move = move_to_closest_food(food, my_head, safe_moves)

	print(f"MOVE {game_state['turn']}: {next_move}")
	return {"move": next_move}


def closest_food(grocerys, head):
	smallest_distance = 10000
	for food in grocerys:
		# distance = math.dist({head['x'], head['y']}, {food['x'], food['y']})

		distance = math.dist(head.values(), food.values())
		if distance < smallest_distance:
			smallest_distance = distance

	return smallest_distance


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


def check_possible_moves(game_state, my_head):
	bad_positions = []
	is_move_safe = {"up": True, "down": True, "left": True, "right": True}
	board_width = game_state['board']['width']
	board_height = game_state['board']['height']
	print(my_head["x"], my_head["y"])
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
			print("break")
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
				print("break")
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

def get_enemy_snake_movement_info(game_state, my_head, my_length):
	enemy_heads = []
	dangerous_enemy_head_moves = []
	for snake in game_state['board']['snakes']:
		if snake['body'][0] == my_head:
			continue
		if snake['length'] < my_length and math.dist(my_head.values(),
		                                             snake['body'][0].values()) < 10:
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
	
if __name__ == "__main__":
	from server import run_server

	run_server({"info": info, "start": start, "move": move, "end": end})
