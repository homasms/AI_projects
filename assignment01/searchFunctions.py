import util

from game import Directions

UNREACHABLE_GOAL_STATE = [Directions.STOP]


def tinyMazeSearch(problem):
    """"
    Run to get familiar with directions.
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    Run this function to get familiar with how navigations works using Directions enum.
    """

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    to_goal_easy_directions = [s, s, w, s, w, w, s, w]
    return to_goal_easy_directions


def simpleMazeSearch(problem):
    """
    Q1:
    Search for the goal using right-hand or left-hand method explained in docs.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getNextStates(problem.getStartState())
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    "*** YOUR EXPLANATION HERE***"
    """ """


def dfs(problem):
    """
    Q2:
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal.
    Make sure to implement a graph search algorithm.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    stack = util.Stack()
    stack.push(start)
    visited = [start]
    parent_dictionary = {}
    find_goal = False

    while not stack.isEmpty() and not find_goal:
        dad = stack.pop()
        next_states = problem.getNextStates(dad)
        for item in next_states:
            if item[0] in visited:
                continue
            parent_dictionary[item[0]] = dad
            if problem.isGoalState(item[0]):
                goal = item[0]
                find_goal = True
                break
            stack.push(item[0])
            visited.append(item[0])

    if not find_goal:
        return UNREACHABLE_GOAL_STATE
    dir = []
    while not goal == start:
        if goal[0] == parent_dictionary[goal][0]:
            if goal[1] > parent_dictionary[goal][1]:
                dir.append(Directions.NORTH)
            else:
                dir.append(Directions.SOUTH)
        else:
            if goal[0] > parent_dictionary[goal][0]:
                dir.append(Directions.EAST)
            else:
                dir.append(Directions.WEST)
        goal = parent_dictionary[goal]

    dir.reverse()
    return dir

    "*** YOUR EXPLANATION HERE ***"
    """ """


def bfs(problem):
    """
    Q3:
    Search the shallowest nodes in the search tree first.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getNextStates(problem.getStartState())
    dir = []
    start = problem.getStartState()
    q = util.Queue()
    parent_dictionary = {}
    check = [start]
    q.push(start)
    find_goal = False

    while not q.isEmpty() and not find_goal:
        dad = q.pop()
        next_states = problem.getNextStates(dad)
        for item in next_states:
            if item[0] in check:
                continue
            parent_dictionary[item[0]] = dad
            if problem.isGoalState(item[0]):
                find_goal = True
                goal = item[0]
                break
            q.push(item[0])
            check.append(item[0])

    while not goal == start:
        if goal[0] == parent_dictionary[goal][0]:
            if goal[1] > parent_dictionary[goal][1]:
                dir.append(Directions.NORTH)
            else:
                dir.append(Directions.SOUTH)
        else:
            if goal[0] > parent_dictionary[goal][0]:
                dir.append(Directions.EAST)
            else:
                dir.append(Directions.WEST)
        goal = parent_dictionary[goal]
    dir.reverse()
    return dir

    "*** YOUR EXPLANATION HERE***"
    """ """


def deadend(problem):
    """
    Q5: Search for all dead-ends and then go for goal state.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    # find deadends
    start = problem.getStartState()
    q = util.Queue()
    check = [start]
    q.push(start)
    deadends = []

    while not q.isEmpty():
        dad = q.pop()
        next_states = problem.getNextStates(dad)
        if len(problem.getNextStates(dad)) == 1 and not problem.isGoalState(dad)\
                and not dad == start:
            deadends.append(dad)
        for item in next_states:
            if item[0] in check:
                continue
            if problem.isGoalState(item[0]):
                real_goal = item[0]
            q.push(item[0])
            check.append(item[0])

    q = util.Queue()
    check = [real_goal]
    q.push(real_goal)
    temp = []
    while not q.isEmpty():
        dad = q.pop()
        next_states = problem.getNextStates(dad)
        for item in next_states:
            if item[0] in check:
                continue
            if item[0] in deadends:
                temp.append(item[0])
            q.push(item[0])
            check.append(item[0])
    print temp
    # find direction
    complete_dir = []
    last_goal = False
    while len(deadends) >= 0 and not last_goal:
        dir = []
        q = util.Queue()
        q.push(start)
        check = [start]
        find_goal = False
        parent_dictionary = {}
        c = 0
        while not q.isEmpty() and not find_goal:
            dad = q.pop()
            next_states = problem.getNextStates(dad)
            for item in next_states:
                if item[0] in check:
                    continue
                parent_dictionary[item[0]] = dad

                # start
                if start == problem.getStartState():
                    if item[0] == temp[len(temp)-1]:
                        goal = item[0]
                        find_goal = True
                        check.append(item[0])
                        deadends.remove(item[0])
                        break
                if item[0] in deadends and not start == problem.getStartState()\
                        and c == 0:
                    temp_goal = item[0]
                    c = 1
                    if len(deadends) > 1:
                        deadends.remove(temp_goal)
                else:
                    q.push(item[0])
                    check.append(item[0])
                if item[0] in deadends and not start == problem.getStartState():
                    if temp.index(temp_goal) > temp.index(item[0]):
                            goal = temp_goal
                    else:
                        goal = item[0]
                        if len(deadends) > 1:
                            deadends.append(temp_goal)
                        deadends.remove(item[0])
                    find_goal = True
                    check.append(goal)
                    break

                # final
                if len(deadends) == 0 and problem.isGoalState(item[0]):
                    goal = item[0]
                    find_goal = True
                    check.append(item[0])
                    last_goal = True
                    break
        while not goal == start:
            if goal[0] == parent_dictionary[goal][0]:
                if goal[1] > parent_dictionary[goal][1]:
                    dir.append(Directions.NORTH)
                else:
                    dir.append(Directions.SOUTH)
            else:
                if goal[0] > parent_dictionary[goal][0]:
                    dir.append(Directions.EAST)
                else:
                    dir.append(Directions.WEST)
            goal = parent_dictionary[goal]
        start = check[len(check)-1]
        dir.reverse()
        for i in dir:
            complete_dir.append(i)

    return complete_dir


def ucs(problem):
    """
    Q7: Search the node of least total cost first.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    dir = []
    start = problem.getStartState()
    q = util.PriorityQueue()
    parent_dictionary = {}
    check = [start]
    q.push(start, problem.cost_function(start))
    find_goal = False

    while not q.isEmpty() and not find_goal:
        dad = q.pop()
        next_states = problem.getNextStates(dad)
        for item in next_states:
            if item[0] in check:
                continue
            parent_dictionary[item[0]] = dad
            if problem.isGoalState(item[0]):
                find_goal = True
                goal = item[0]
                break
            q.push(item[0], problem.cost_function(item[0]))
            check.append(item[0])

    while not goal == start:
        if goal[0] == parent_dictionary[goal][0]:
            if goal[1] > parent_dictionary[goal][1]:
                dir.append(Directions.NORTH)
            else:
                dir.append(Directions.SOUTH)
        else:
            if goal[0] > parent_dictionary[goal][0]:
                dir.append(Directions.EAST)
            else:
                dir.append(Directions.WEST)
        goal = parent_dictionary[goal]
    dir.reverse()
    return dir

    "*** YOUR EXPLANATION HERE***"
    """ """
