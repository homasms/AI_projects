import numpy as np
from ple import PLE
from ple.games.snake import Snake

agent = Snake(width=256, height=256)

env = PLE(agent, fps=15, force_fps=False, display_screen=True)

env.init()
actions = env.getActionSet()


q_states = {
    ((1, 1), 0): 0
}

count_q = {
    (0, 0): 0
}
w = np.random.rand(4)
alpha = 0.5
gama = 1
epsilon = 0.7
steps = 1


# checked: correct :)
def compute_sprim(state, action):
    new_state = (0, 0)
    if action == 119:
        new_state = (state[0], state[1] + 1)
    if action == 97:
        new_state = (state[0] + 1, state[1])
    if action == 100:
        new_state = (state[0] - 1, state[1])
    if action == 115:
        new_state = (state[0], state[1] - 1)
    return new_state


def reward(state):
    re = 0
    if agent.getGameState()["food_x"] == state[0] and agent.getGameState()["food_y"] == state[1]:
        re = 1
    elif env.game_over():
        print("game over")
        re = -1
    return re


# checked: correct
# feature 1
def to_goal(state):
    distance = np.abs(state[0] - agent.getGameState()["food_x"]) + np.abs(state[1] - agent.getGameState()["food_y"])
    # print("head =", state[0], "food =", agent.getGameState()["food_x"])
    # print("dist = ", distance, "1/= dist= ", 1/distance )
    if distance == 0:
        return 1

    return 1 / (0.004 * distance + 1)


# feature 2
def to_body():
    if agent.getGameState()["snake_body"].__contains__(0):
        return -1
    return 0


# checked: correct :)
# feature 3
def to_wall(state):
    rew = 0
    if state[0] == 0 or state[0] == env.getScreenDims()[0]:
        # env.act(actions[0])
        rew = - 1
    if state[1] == 0 or state[1] == env.getScreenDims()[1]:
        rew = -1
    # print("screen= ", env.getScreenDims()[0])
    return rew


# correct :)
# all features
def compute_features(state):
    features = np.array([to_goal(state), to_body(), to_wall(state)])
    return features


def compute_q(s, action):
    if not count_q.keys().__contains__(s):
        count_q[s] = 1
    else:
        count_q[s] += 1

    # print("s, action=", s, action)
    sprim = compute_sprim(s, action)
    # print(sprim)
    if not count_q.keys().__contains__(sprim):
        count_q[sprim] = 1
    q_states[(s, action)] = w[0] * compute_features(sprim)[0] \
                            + w[1] * compute_features(sprim)[1] \
                            + w[2] * compute_features(sprim)[2] \
                            + w[3] / count_q[sprim]
    print("w= ", w)
    # print("features= ", compute_features(sprim))
    return q_states[(s, action)]


def q_max(state):
    maximum = -1000
    for a in actions:
        if a == actions[4]:
            break
        maximum = max(maximum, compute_q(state, a))
        # print("q_max= ", compute_q(state, a))
    return maximum


def compute_epsilon():
    return (10 + steps) * epsilon / (10 * steps)


def exploit(state):
    maximum = -10000
    act = 0
    # print("exploit s= ", state)
    for action in actions:
        if action == actions[4]:
            break
        best_state = compute_q(s, action)
        print("compute_q= ", compute_q(s, action), "action= ", action)
        if best_state > maximum:
            maximum = best_state
            act = action
    if not count_q.keys().__contains__(state):
        count_q[state] = 1
    else:
        count_q[state] += 1
    # print(act)
    return act


def explore(state):
    act = np.random.randint(0, len(actions))
    act_exp = actions[act]
    q_states[state, act] = compute_q(state, act)
    return act_exp


def update_w(s, sprim, acts):
    if not q_states.keys().__contains__((s, acts)):
        q_states[(s, acts)] = 0
    difference = (gama * q_max(sprim)) + reward(sprim) - q_states[(s, acts)]
    # print("q_max(sprim)", q_max(sprim))
    # print("reward(s)=", reward(s))
    # print("difference= ", difference)
    for i in range(3):
        w[i] += alpha * difference * compute_features(s)[i]
    # print("w= ", w)
    return


def choose_action(state):
    # print("choose s= ", state)
    prob = np.random.rand()
    if prob < compute_epsilon():
        return explore(state)
    else:
        return exploit(state)


for i in range(10000):
    steps += 1
    if env.game_over():
        env.reset_game()
    s = (int(agent.getGameState()["snake_head_x"]), int(agent.getGameState()["snake_head_y"]))
    print("----------")
    print("s = ", s)
    action = choose_action(s)
    env.act(action)
    print(action)
    sprim = (0, 0)
    if action == 119:
        sprim = (s[0], s[1]+1)
        update_w(s, sprim, action)
    if action == 97:
        sprim = (s[0]+1, s[1])
        update_w(s, sprim, action)
    if action == 100:
        sprim = (s[0]-1, s[1])
        update_w(s, sprim, action)
    if action == 115:
        sprim = (s[0], s[1]-1)
        update_w(s, sprim, action)


