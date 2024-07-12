# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    

    import util

    # Δημιουργία στοίβας για να αποθηκεύσω καταστάσεις και ενέργειες
    stack = util.Stack()

    # Δημιουργία set με ενέργειες που επισκέφθηκε
    visited = set()

    # κάνω push στην στοίβα με την να ξεκινήσει η αρχική κατάσταση μαζί με μία άδεια λίστα από ενέργειες
    stack.push((problem.getStartState(), []))

    # Όσο η στοίβα δεν είναι άδεια 
    while not stack.isEmpty():
        # κάνω pop στην στοίβα με την τωρινή κατάσταση και και τις αντίστοιχες καταστάσεις από την στοίβα μου
        state, actions = stack.pop()

        # αν ειμαστε στην κατασταση στόχου επιστροφή λίστα με ενέργειες
        if problem.isGoalState(state):
            return actions

        # επίσης αν δεν έχει επισκεφθεί τότε την κατάσταση αυτή την κάνουμε add και γίνεται visited
        if state not in visited:
            
            visited.add(state)

            # οι successors του current state
            successors = problem.getSuccessors(state)

            # για κάθε successor κάνω push την κατάστασή του! και την updated λίστα ενεργειών 
            for next_state, action, _ in successors:
                stack.push((next_state, actions + [action]))

    # αν δεν βρεθεί λύση επιστρέφεται άδεια λίστα
    return []

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    import util

    # αντί για στοίβα στον bfs θα δημιουργήσουμε ουρά για αποθήκευση καταστάσεων, ενεργειών
    queue = util.Queue()

    
    visited = set()

  
    queue.push((problem.getStartState(), []))

    # όσο δεν είναι άδεια η ουρά
    while not queue.isEmpty():
        #  pop στην ουρά
        state, actions = queue.pop()

        # 
        if problem.isGoalState(state):
            return actions

        
        if state not in visited:
            
            visited.add(state)

         
            successors = problem.getSuccessors(state)

           
            for next_state, action, _ in successors:
                queue.push((next_state, actions + [action]))

    
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    


    import util

    #Φτιαχνω αρχικα μια ουρά προτεραιότητας για να αποθηκεύσω καταστάσεις, ενέργειες  
    pq = util.PriorityQueue()

   
    visited = set()

    # κάνω push στην ουρά pq με την να ξεκινήσει η αρχική κατάσταση
    pq.push((problem.getStartState(), [], 0), 0)

    # μέχρι η pq να μην ειναι αδεια
    while not pq.isEmpty():
        # κανω pop την τωρινη κατασταση και τις ενεργειες της και το μεχρι στιγμης κόστος
        state, actions, cost = pq.pop()

        # If  cur state is the GoalState, επιστρεφω τις ενέργειες
        if problem.isGoalState(state):
            return actions

       
        if state not in visited:
            # προσθετω την κατασταση που δεν την επισκεφθει και μολις την επισκεφθηκε στα visited
            visited.add(state)

           
            successors = problem.getSuccessors(state)

            
            for next_state, action, step_cost in successors:
                # an to successor state den to exei episkefthei tote ipologizo to sinoliko kostos gia na ftaso sto successor state
                if next_state not in visited:
                    
                    total_cost = cost + step_cost

                    # kano push to successor state kai tin lista energeion alla kai to sinoliko kostos tis priority queue moy
                    pq.push((next_state, actions + [action], total_cost), total_cost)

 
    return []

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
   

    pq = util.PriorityQueue()

        # αρχικοποιω το συνολο επισκεφθεντων κομβων
    visited = set()

        # Αρχικοποίηση της ουράς προτεραιότητας με την αρχική κατάσταση και το μηδενικο κοστο αλλα και την εκτιμηση της ευρετικης συναρτησης
    pq.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState(), problem))

        # Επανάληψη μέχρι η ουρά προτεραιότητας να ειναι αδεια
    while not pq.isEmpty():
            # Αφαίρεση του επόμενου κόμβου από την ουρά
        state, actions, cost = pq.pop()

            # Έλεγχος αν ο κόμβος είναι ο στόχος
        if problem.isGoalState(state):
                return actions

            # Αν δεν το εχει επισκεφθεί ακόμα τον κομβο
        if state not in visited:
                # προστιθεται στο συνολο
            visited.add(state)

                # καταστασεις διαδοχης
            successors = problem.getSuccessors(state)

                # Για καθε διαδοχο
            for next_state, action, step_cost in successors:
                if next_state not in visited:
                        # Υπολογισμός συνολικού κόστους μέχρι τον κομβο διάδοχου
                    total_cost = cost + step_cost

                        #  γινεται push το successor state και η lista energeion και το συνολικο κοστος της pq αλλα και της ευρετικης
                    pq.push((next_state, actions + [action], total_cost), total_cost + heuristic(next_state, problem))

        # Επιστροφή της κενής λίστας αν δεν βρει λυση
    return []

    util.raiseNotDefined()






# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
