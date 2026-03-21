
class BlockWorldAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        #Add your code here! Your solve method should receive
		#as input two arrangements of blocks. The arrangements
		#will be given as lists of lists. The first item in each
		#list will be the bottom block on a stack, proceeding
		#upward. For example, this arrangement:
		#
		#[["A", "B", "C"], ["D", "E"]]
		#
		#...represents two stacks of blocks: one with B on top
		#of A and C on top of B, and one with E on top of D.
		#
		#Your goal is to return a list of moves that will convert
		#the initial arrangement into the goal arrangement.
		#Moves should be represented as 2-tuples where the first
		#item in the 2-tuple is what block to move, and the
		#second item is where to put it: either on top of another
		#block or on the table (represented by the string "Table").
		#
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")

        stacks = [list(stack) for stack in initial_arrangement]
        moves = []
        goal_support = {}
        for stack in goal_arrangement:
            for i, block in enumerate(stack):
                if i == 0:
                    goal_support[block] = "Table"
                else:
                    goal_support[block] = stack[i - 1]


        def find_block(block):
            for i, stack in enumerate(stacks):
                if block in stack:
                    return i, stack.index(block)
            return None, None

        def is_clear(block):
            i, h = find_block(block)
            return h == len(stacks[i]) - 1

        def current_support(block):
            i, h = find_block(block)
            if h == 0:
                return "Table"
            return stacks[i][h - 1]

        def move_to_table(block):
            i, _ = find_block(block)
            stacks[i].pop()
            stacks.append([block])
            moves.append((block, "Table"))

        def move_onto(block, target):
            i, _ = find_block(block)
            j, _ = find_block(target)
            stacks[i].pop()
            stacks[j].append(block)
            moves.append((block, target))
        correct_cache = {}

        def is_correct(block):
            if block in correct_cache:
                return correct_cache[block]

            if current_support(block) != goal_support[block]:
                correct_cache[block] = False
                return False

            if goal_support[block] == "Table":
                correct_cache[block] = True
                return True

            result = is_correct(goal_support[block])
            correct_cache[block] = result
            return result

        def recompute_correct():
            correct_cache.clear()
            for stack in stacks:
                for block in stack:
                    is_correct(block)


        recompute_correct()

        while True:

            progress_made = False
            for stack in stacks:
                if not stack:
                    continue

                block = stack[-1]

                if is_correct(block):
                    continue

                target = goal_support[block]

                if target == "Table":
                    if current_support(block) != "Table":
                        move_to_table(block)
                        recompute_correct()
                        progress_made = True
                        break

                else:
                    if is_clear(target) and is_correct(target):
                        move_onto(block, target)
                        recompute_correct()
                        progress_made = True
                        break

            if progress_made:
                continue
            for stack in stacks:
                if not stack:
                    continue

                block = stack[-1]

                if not is_correct(block):
                    move_to_table(block)
                    recompute_correct()
                    progress_made = True
                    break

            if not progress_made:
                break

        return moves
