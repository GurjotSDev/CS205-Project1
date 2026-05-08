import time
import sys
import heapq

# This is to allow for simple changes to the puzzle, just make sure its valid
trench_len = 10
recess_pos = (3, 5, 7)


# The current state of the problem
initial_state = (
    (0, 2, 3, 4, 5, 6, 7, 8, 9, 1),
    (0, 0, 0)
)

# The goal state
goal_state = (
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 0),
    (0, 0, 0)
)

goal_pos = {k : k-1 for k in range(1,trench_len)}

# The node and what information it holds
def make_node(state, parent, depth, path_cost):
    return {
        "State": state,
        "Parent_Node": parent,
        "Depth": depth,
        "Path_Cost": path_cost
    }

# The opeerators of movement
def operators(state):
    trench, recess = state
    # Find all the empty indexes
    for empty in (i for i,v in enumerate(trench) if v == 0):
        # Move a soldier from the right of the empty spot to the empty spot
        for j in range(empty+1, trench_len):
            if trench[j] != 0:
                if all(trench[k] == 0 for k in range (empty+1, j)):
                    newtrench = list(trench)
                    newtrench[empty], newtrench[j] = newtrench[j], 0
                    yield (tuple(newtrench), recess)
                break
        
        # Move a soldier from the left of the empty spot to the empty spot
        for j in range(empty-1, -1, -1):
            if trench[j] != 0:
                if all(trench[k] == 0 for k in range (j+1, empty)):
                    newtrench = list(trench)
                    newtrench[empty], newtrench[j] = newtrench[j], 0
                    yield (tuple(newtrench), recess)
                break

    # Move soldiers into the recess or into trench
    for i, v in enumerate(recess_pos):
        in_trench = trench[v]
        in_recess = recess[i]

        # Move a soldier into the recess
        if in_trench != 0 and in_recess == 0:
            newtrench = list(trench)
            newtrench[v] = 0
            newrecess = list(recess)
            newrecess[i] = in_trench
            yield (tuple(newtrench), tuple(newrecess))
        
        # Move a soldier into the trench
        if in_recess != 0 and in_trench == 0:
            newtrench = list(trench)
            newtrench[v] = in_recess
            newrecess = list(recess)
            newrecess[i] = 0
            yield (tuple(newtrench), tuple(newrecess))

# Heuristics

# For uniform cost search
def h_zero(state):
    return 0

# For misplaced tiles
def h_misplaced(state):
    trench, recess = state
    misplaced = 0

    # Misplaced trench tiles
    for i, v in enumerate(trench):
        if v == 0:
            continue

        if goal_pos[v] != i:
            misplaced += 1
    
    # Misplaced recess tiles
    for v in recess:
        if v != 0:
            misplaced += 1
    
    return misplaced

# For manhattan distance
def h_manhattan(state):
    trench, recess = state
    total_distance = 0

    # For the trench
    for i,v in enumerate(trench):
        if v == 0:
            continue

        goal_index = goal_pos[v]
        distance = abs(i - goal_index)
        total_distance += distance
    
    # For the recess
    for i,v in enumerate(recess):
        if v == 0:
            continue

        trench_pos = recess_pos[i]
        goal_index = goal_pos[v]

        distance = 1 + abs(trench_pos-goal_index)

        total_distance += distance
    
    return total_distance

def general_search(problem, queuing_function):
    nodes = [(0,0,make_node(problem, None, 0, 0))]
    visited = {}
    nodes_expanded = 0
    max_queue_size = 1
    tie_breaker = 0

    while True:
        if len(nodes)==0:
            return "failure", nodes_expanded, max_queue_size

        _, _, node = heapq.heappop(nodes)
        state = node["State"]
        g = node["Path_Cost"]

        # Skip if we expanded this state at a cheaper cost
        if visited.get(state, float("inf")) <= g:
            continue

        visited[state] = g
        nodes_expanded += 1

        h = queuing_function(state)
        print(f"\nThe best state to expand with a g(n)  = {g} and h(n) = {h} is ...")
        print(list(state[0]))
        if any(v != 0 for v in state[1]):
            print(f"Recess: {list(state[1])}")
        
        if state == goal_state:
            return node, nodes_expanded, max_queue_size
        
        for child_state in operators(state):
            child_g = g + 1
            if visited.get(child_state, float("inf")) > child_g:
                child_h = queuing_function(child_state)
                tie_breaker += 1
                child = make_node(child_state, node, node["Depth"] + 1, child_g)
                heapq.heappush(nodes, (child_g + child_h, tie_breaker, child))
        
        if len(nodes) > max_queue_size:
            max_queue_size = len(nodes)
