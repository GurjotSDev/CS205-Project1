import time
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

# The operators  of movement
def operators(state):
    trench, recess = state
    # Find all the empty indexes
    for empty in (i for i,v in enumerate(trench) if v == 0):
        # Move soldier from right to empty
        if empty + 1 < trench_len and trench[empty+1] !=0:
            newtrench = list(trench)
            newtrench[empty], newtrench[empty+1] = newtrench[empty+1], 0
            yield (tuple(newtrench), recess)
        
        # Move a soldier from the left to empty
        if empty - 1 >= 0 and trench[empty-1] !=0:
            newtrench = list(trench)
            newtrench[empty], newtrench[empty-1] = newtrench[empty-1], 0
            yield (tuple(newtrench), recess)

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
    # Make the Queue
    nodes = [(0,0,make_node(problem, None, 0, 0))]
    visited = {}
    nodes_expanded = 0
    max_queue_size = 1
    tie_breaker = 0

    while True:
        # Empty check
        if len(nodes)==0:
            return "failure", nodes_expanded, max_queue_size

        # Get a node
        _, _, node = heapq.heappop(nodes)
        state = node["State"]
        g = node["Path_Cost"]


        # Skip if we expanded this state at a cheaper cost
        if state in visited and visited[state] <= g:
            continue
        
        # Mark node visited
        visited[state] = g
        nodes_expanded += 1

        # Print the node being expanded
        h = queuing_function(state)
        print(f"\nThe best state to expand with a g(n)  = {g} and h(n) = {h} is ...")
        print(list(state[0]))
        if any(v != 0 for v in state[1]):
            print(f"Recess: {list(state[1])}")
        
        # Goal state check
        if state == goal_state:
            return node, nodes_expanded, max_queue_size
        
        # Insert children
        for child_state in operators(state):
            child_g = g + 1
            child_h = queuing_function(child_state)
            tie_breaker += 1
            child = make_node(child_state, node, node["Depth"] + 1, child_g)
            heapq.heappush(nodes, (child_g + child_h, tie_breaker, child))
        
        if len(nodes) > max_queue_size:
            max_queue_size = len(nodes)

def main():
    print("Welcome to the Nine Men in a Trench Puzzle solver")
    print("Type '1' to use the default puzzle or '2' to create your own")

    choice = input().strip()

    if choice == "1":
        start = initial_state
    elif choice == "2":
        global trench_len, goal_state, goal_pos
        # Get trench length
        print("\nHow many positions does the trench have?")
        trench_len = int(input().strip())

        # Get number of soldiers and positions
        print("\nHow many soldiers are there?")
        num_soldiers = int(input().strip())
        print("Enter the soldier positions in the trench where 0 is empty and separate with space")
        trench = tuple(int(x) for x in input().split())

        # Get the number of recesses and indexes
        print("\nHow many recesses are there?")
        num_recesses = int(input().strip())
        print("Enter the index the recess is on separated by space")
        recess_pos = tuple(int(x) for x in input().split())
        recess = tuple(0 for _ in recess_pos)

        # Get goal state
        soldiers = sorted(v for v in trench if v !=0)
        goal_trench = tuple(soldiers) + tuple(0 for _ in range(trench_len-num_soldiers))
        goal_state = (goal_trench, recess)
        # Different from default because soldier count might be different
        goal_pos = {v: i for i, v in enumerate(goal_trench) if v != 0}

        start = (trench, recess)

    else:
        print("Invalid choice. Doing default")
        start = initial_state
    
    print("\nSelect algorithm")
    print("(1) for Uniform Cost Search")
    print("(2) for Misplaced Tiles Heuristic")
    print("(3) for Manhattan Distance Heuristic")
    algorithm = input().strip()

    if algorithm == "1":
        heuristic = h_zero
    elif algorithm == "2":
        heuristic = h_misplaced
    elif algorithm == "3":
        heuristic = h_manhattan
    else:
        print("Invalid choice. Using uniform search cost")
        heuristic = h_zero
    
    start_time = time.time()
    result, nodes_expanded, max_queue_size = general_search(start, heuristic)
    end_time = time.time()
    if result == "failure":
        print("\nFailure: no solution found")
    else:
        print("\nGoal state found")
        print(f"Solution depth: {result['Depth']}")
        print(f"Number of nodes expanded: {nodes_expanded}")
        print(f"Max queue size: {max_queue_size}")
        print(f"Time to solve: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
