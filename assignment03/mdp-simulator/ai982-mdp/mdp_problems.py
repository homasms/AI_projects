from utilities import Actions, initialize_mdp_parameters


class MDPProblem:
    """

    :param grid_dim: a tuple of (height, width) which declares dimensions of the world grid.
    :param exit_locations: a dictionary with exit states as keys and rewards as values.
    example given: self.exit_locations[(0, 2)] = -1 or self.exit_locations = {(0, 2): -1, ...}


    """

    def __init__(self, grid_dim, exit_locations):
        self.grid_dim = grid_dim
        self.exit_locations = exit_locations

    def compute_policy(self, reward=-0.01, gama=1, steps=10):
        """

        :param reward: reward of moving from one cell to another. (Living reward)
        :param gama: Discount coefficient
        :param steps: depth of computation. (How many turns agent can play)
        :return:
        1-2D grid of computed V*_k(s) after each step.
        Example Given for 3x3 world after some steps.
       [ 0     0.8  1
       -0.02 -0.1 -1
        0   -0.02  0 ]
        2- A 2D grid of computed Policies. (same as v_states but filled with Actions class instances.)
        a naive policy:
      [ Actions.N Actions.N Actions.EXIT
        Actions.N Actions.N Actions.EXIT
        Actions.N Actions.N Actions.N ]
        """

        width, height = self.grid_dim

        # Use pre_v_states for keeping previous V states. (former iteration)
        v_states, pre_v_states, policy = initialize_mdp_parameters(width, height, self.exit_locations)
        for row in v_states:
            print(*row)
        print('******************')
        for row in pre_v_states:
            print(*row)
        print('******************')
        for row in policy:
            print(*row)
        print('******************')
        actions = [Actions.N, Actions.S, Actions.E, Actions.W]

        for k in range(0, steps):
            for i in range(0, width):
                for j in range(0, height):
                    """ YOUR CODE HERE"""
                    current_state = (i, j)
                    if (current_state, -1) in self.exit_locations.items():
                        break
                    self.update_v_state(current_state, actions, reward, gama,
                                        v_states, policy, pre_v_states)
            # DO NOT CHANGE yield Line. You should return V and Pi computed in each step.
            yield v_states, policy

    def update_v_state(self, state, actions, reward, gama, v_states, policy, pre_v_states):
        weight = state[0]
        height = state[1]
        for action in actions:
            new_value = self.compute_action_value(state, action, reward, gama, pre_v_states)
            if new_value > v_states[weight][height]:
                v_states[weight][height] = new_value
                policy[weight][height] = action
            pre_v_states[weight][height] = v_states[weight][height]
        return

    def compute_action_value(self, state, action, reward, gama, pre_v_states):
        value = 0
        for transition in self.get_transition(state, action):
            pre_v_state = pre_v_states[transition[0]][transition[1]]
            value += transition[2] * (reward + (gama * pre_v_state))
        return value

    def get_transition(self, state, action):
        """

        :param state: a tuple of (x, y) as dimensions
        :param action: object of Actions enum class. (such as:
        Actions.N)
        :return: given current state and chosen action, returns next non-determinist states with
        corresponding transition probabilities. example given: [(x, y, 0.8), (z, t, 0,2), ...] means after choosing
        action, agent goes to (x, y) with probability of 80% and goes to (z, t) with probability of 20%.

        """

        next_state_dict = {Actions.N: (-1, 0), Actions.S: (1, 0), Actions.E: (0, 1), Actions.W: (0, -1)}
        non_determinist_dict = {Actions.N: Actions.E, Actions.E: Actions.S, Actions.S: Actions.W, Actions.W: Actions.N}
        transitions = []
        next_x, next_y = tuple(map(sum, zip(next_state_dict[action], state)))
        if (0 <= next_x < self.grid_dim[0]) and (0 <= next_y < self.grid_dim[1]):
            transitions += [(next_x, next_y, 0.8)]
        next_x, next_y = tuple(map(sum, zip(next_state_dict[non_determinist_dict[action]], state)))
        if (0 <= next_x < self.grid_dim[0]) and (0 <= next_y < self.grid_dim[1]):
            transitions += [(next_x, next_y, 0.2)]
        return transitions
