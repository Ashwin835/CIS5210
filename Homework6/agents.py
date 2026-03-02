student_name = "Ashwin Verma"


class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        self.g = game
        self.gamma = discount
        self.vals = {}
        for s in game.states:
            self.vals[s] = 0

    def get_value(self, state):
        if state not in self.vals:
            return 0
        return self.vals[state]

    def get_q_value(self, state, action):
        total = 0
        trans = self.g.get_transitions(state, action)
        for s2, p in trans.items():
            r = self.g.get_reward(state, action, s2)
            total += p * (r + self.gamma * self.get_value(s2))
        return total

    def get_best_policy(self, state):
        possible = self.g.get_actions(state)
        if not possible:
            return None
        best = max(possible, key=lambda a: self.get_q_value(state, a))
        return best

    def iterate(self):
        updated = {}
        for s in self.g.states:
            acts = self.g.get_actions(s)
            if not acts:
                updated[s] = 0
            else:
                updated[s] = max(self.get_q_value(s, a) for a in acts)
        self.vals = updated


class PolicyIterationAgent(ValueIterationAgent):

    def iterate(self):
        thresh = 1e-6

        cur_policy = {}
        for s in self.g.states:
            cur_policy[s] = self.get_best_policy(s)

        while True:
            new_vals = {}
            for s in self.g.states:
                a = cur_policy[s]
                if a is None:
                    new_vals[s] = 0
                else:
                    new_vals[s] = self.get_q_value(s, a)

            if not new_vals:
                break

            biggest_change = max(
                abs(new_vals[s] - self.get_value(s)) for s in self.g.states
            )
            self.vals = new_vals
            if biggest_change < thresh:
                break


def question_3():
    d = 0.9
    n = 0.0
    return d, n


def question_4a():
    d = 0.1
    n = 0.0
    lr = 0.0
    return d, n, lr


def question_4b():
    d = 0.2
    n = 0.2
    lr = 0.0
    return d, n, lr


def question_4c():
    d = 0.9
    n = 0.0
    lr = 0.0
    return d, n, lr


def question_4d():
    d = 0.9
    n = 0.2
    lr = 0.0
    return d, n, lr


def question_4e():
    d = 0.9
    n = 0.2
    lr = 10.0
    return d, n, lr


feedback_question_1 = """
around 3 hours
"""

feedback_question_2 = """
policy iteration was tricky, kept getting confused about when to update
the values vs when to keep them fixed. also the batch in value iteration
tripped me up at first
"""

feedback_question_3 = """
none, I thought the instructions were pretty clear
and the code was well
"""
