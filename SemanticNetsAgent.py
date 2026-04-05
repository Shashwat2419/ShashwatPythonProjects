#More details for this project can be found in SemanticNetsAgent.md


from collections import deque
class SemanticNetsAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        self.moves = [(1,0), (0,1), (2,0), (0,2), (1,1)]

    def solve(self, initial_sheep, initial_wolves):
        start = (initial_sheep, initial_wolves, 0, 0, 'L')
        goal = (0, 0, initial_sheep, initial_wolves, 'R')

        queue = deque([(start, [])])
        visited = set([start])

        while queue:
            state, path = queue.popleft()
            if state == goal:
                return path  # Found solution

            left_s, left_w, right_s, right_w, boat = state

            for m_s, m_w in self.moves:
                if boat == 'L':
                    new_state = (left_s - m_s, left_w - m_w,
                                 right_s + m_s, right_w + m_w, 'R')
                else:
                    new_state = (left_s + m_s, left_w + m_w,
                                 right_s - m_s, right_w - m_w, 'L')

                if self.is_valid(new_state, initial_sheep, initial_wolves):
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, path + [(m_s, m_w)]))

        return []  # in case no solution is found

    def is_valid(self, state, total_s, total_w):
        left_s, left_w, right_s, right_w, boat = state

        # Non-negative counts
        if min(left_s, left_w, right_s, right_w) < 0:
            return False
        if left_s > total_s or right_s > total_s:
            return False
        if left_w > total_w or right_w > total_w:
            return False
        # Safety rule: wolves cannot outnumber sheep on either side (unless no sheep present)
        if left_s > 0 and left_w > left_s:
            return False
        if right_s > 0 and right_w > right_s:
            return False

        return True
