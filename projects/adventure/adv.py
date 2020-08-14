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
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

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

# def explore_rooms(player, trans_graph):
#     run = True
#     iteration = 0
#     while run:
#         iteration += 1
       
#         found = False
#         count = 0
       
#         for i in trans_graph.values():
                
#                 if "?" in i.values():
#                     count +=1
                
#         if count == 0:
#             print('ran')
#             return traversal_path

#         if len(traversal_path) > 0:
#             for i in reversed(traversal_path):
#                 player.travel(opposite_direction(i))
#                 traversal_path.append(opposite_direction(i))
#                 if len(find_unexplored(trans_graph[player.current_room.id])) > 0:
#                     found = True
#                     break
#             if not found:
#                 return traversal_path
#         while len(find_unexplored(trans_graph[player.current_room.id])) > 0:
#                 room_id = player.current_room.id

#                 unexplored = find_unexplored(trans_graph[room_id])

#                 random_dir = random.choice(unexplored)

#                 player.travel(random_dir)

#                 trans_graph[room_id][random_dir] = player.current_room.id
#                 trans_graph[player.current_room.id][opposite_direction(random_dir)] = room_id

#                 traversal_path.append(random_dir)
        

def explore_rooms(player, trans_graph, traversal_path):
    # variable to keep while loop running
    run = True
    # while loop to keep running everything
    while run:
        # count to check how many ? the check found
        count = 0
        # for loop to check if there are any ?'s in the trans_graph
        for i in trans_graph.values():
            # if there is a ?...
            if "?" in i.values():
                # increate count by 1
                count +=1
                # break out of the for loop
                break
        
        # if count is greater than 0...
        if count == 0:
            # break out of the function
            return

        # while loop to check if the surrounding rooms are unexplored
        while len(find_unexplored(trans_graph[player.current_room.id])) > 0:
                # get the current room id
                room_id = player.current_room.id

                # find the unexplored directions
                unexplored = find_unexplored(trans_graph[room_id])

                # randomly select a direction
                random_dir = random.choice(unexplored)

                # travel to that random direction
                player.travel(random_dir)

                # in the current room, set the random directions room to the new room
                trans_graph[room_id][random_dir] = player.current_room.id
                # in the new room, set the opposite direction of the random direction to the previous room
                trans_graph[player.current_room.id][opposite_direction(random_dir)] = room_id
                # add the traversal to the traversal_path list
                traversal_path.append(random_dir)

        # another check to see if there are no "?"
        count = 0
        for i in trans_graph.values():
            if "?" in i.values():
                count +=1
                break
                
        if count == 0:
            return 

        # instantiate queue
        q = Queue()
        # set to hold already visited rooms
        visited = set()
        # variable that holds the current room id
        room_id = player.current_room.id
        # grab all the possible directions we can go from the current room
        for i in trans_graph[room_id]:
            # enqueue it to the queue
            q.enqueue([i])
        # if the size of the path is greater than 0...
        while q.size() > 0:
            # dequeue the queued path
            v = q.dequeue()
            # reset the room_id for the next iteration
            room_id = player.current_room.id
            # iterate through the directions
            for i in v:
                # save the previous room id
                old_room_id = room_id
                # change the room_id to to the room at i direction
                room_id = trans_graph[room_id][i]
            # add the room id to visited
            visited.add(room_id)
            # if the current room is undiscovered...
            if room_id == "?":
                # iterate through the current directions
                for i in v:
                    # travel to the new room
                    player.travel(i)
                    # add the directions to the traversal_path list
                    traversal_path.append(i)
                # set the current room v[-1] direction to the current room (the new room)
                trans_graph[old_room_id][v[-1]] = player.current_room.id
                # set the new room's opposite direction of v[-1] to the old_room
                trans_graph[player.current_room.id][opposite_direction(v[-1])] = old_room_id
                # break out of while loop if a undiscovered room was found
                break
            # if it did not find a undiscovered room with the directions...
            else:
                # iterate through the curren'ts room exits
                for i in trans_graph[room_id]:
                    # if that exit room has not been visted
                    if trans_graph[room_id][i] not in visited:
                        # copy the current path it was working on
                        new_path = v.copy()
                        # append the new direction to the current path
                        new_path.append(i)
                        # enqueue the new path
                        q.enqueue(new_path)

        
lowest_moves = 2000                    
for i in range(20000):
    player = Player(world.starting_room)
    traversal_path = []
    trans_graph1 = {}

    for i in room_graph.items():
        trans_graph[i[0]] = {}
        dict_vals = []
        for v in i[1][1].keys():
            trans_graph[i[0]][v] = "?"
            
    explore_rooms(player=player, trans_graph=trans_graph, traversal_path=traversal_path)



    # TRAVERSAL TEST
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

    if len(traversal_path) < lowest_moves:
        lowest_moves = len(traversal_path)
        print(f"New lowest moves: {lowest_moves}")

print(f"Final lowest: {lowest_moves}")

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
