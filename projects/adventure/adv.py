from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
# map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# player.current_room.connect_rooms('n', player.current_room.get_room_in_direction('n'))

# print(player.travel('n', True))
# print(player.travel('n', True))
# print(player.travel('s', True))



# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
trans_graph = {}

for i in room_graph.items():
    trans_graph[i[0]] = {}
    dict_vals = []
    # for value in i[1][1].values():
        # dict_vals.append(value)
    for v in i[1][1].keys():
        trans_graph[i[0]][v] = "?"
        # dict_vals.pop(0)

# print(room_graph)

directions = ['n','e','s','w']

def find_unexplored(room):
    unexplored = []
    for i in room.items():
        if i[1] == '?':
            unexplored.append(i[0])

    return unexplored

def opposite_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

def explore_rooms(player, trans_graph):
    run = True
    while run:
        found = False
        if len(traversal_path) > 0:
            for i in reversed(traversal_path):
                player.travel(opposite_direction(i))
                traversal_path.append(opposite_direction(i))
                if len(find_unexplored(trans_graph[player.current_room.id])) > 0:
                    found = True
                    break
            if not found:
                return traversal_path
        while len(find_unexplored(trans_graph[player.current_room.id])) > 0:
                room_id = player.current_room.id

                unexplored = find_unexplored(trans_graph[room_id])

                random_dir = random.choice(unexplored)

                player.travel(random_dir)

                trans_graph[room_id][random_dir] = player.current_room.id
                trans_graph[player.current_room.id][opposite_direction(random_dir)] = room_id

                traversal_path.append(random_dir)
        

print(explore_rooms(player, trans_graph))

# TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
