# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

    # Έλεγχος αν ολοκληρώθηκε η αναζήτηση στο βάθος
        def isTerminalState(gameState, depth):
            return depth == self.depth or gameState.isWin() or gameState.isLose()

        # Αναδρομική συνάρτηση αξιολόγησης
        def value(state, depth, agentIndex):
            if isTerminalState(state, depth):
                return self.evaluationFunction(state)
            
            # Εάν ο παίκτης είναι ο Pacman (MAX)
            if agentIndex == 0:
                return max_value(state, depth, agentIndex)
            # Εάν ο παίκτης είναι φάντασμα (MIN)
            else:
                return min_value(state, depth, agentIndex)

        # Συνάρτηση max-value
        def max_value(state, depth, agentIndex):
            v = float("-inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                v = max(v, value(successorState, depth, agentIndex + 1))
            return v

        # Συνάρτηση min-value
        def min_value(state, depth, agentIndex):
            v = float("inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                if agentIndex == state.getNumAgents() - 1:  # Αν το τρέχον από τα φαντάσματα είναι το τελευταίο
                    v = min(v, value(successorState, depth + 1, 0))  # Προχωράμε στον επόμενο βαθμό βάθους και ο επόμενος παίκτης είναι ο Pacman
                else:
                    v = min(v, value(successorState, depth, agentIndex + 1))  # Παραμένουμε στο ίδιο βάθος αναζήτησης
            return v

        # Βρίσκουμε την καλύτερη ενέργεια για τον Pacman
        bestAction = None
        bestValue = float("-inf")
        legalActions = gameState.getLegalActions(0)  # Ο Pacman έχει agentIndex = 0
        for action in legalActions:
            successorState = gameState.generateSuccessor(0, action)
            newValue = value(successorState, 0, 1)  # Ξεκινάμε την αναζήτηση από βάθος 0 και ο επόμενος παίκτης είναι το πρώτο φάντασμα
            if newValue > bestValue:
                bestValue = newValue
                bestAction = action
        return bestAction
        
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction """
        
        
        
        # Έλεγχος αν ολοκληρώθηκε η αναζήτηση στο βάθος
        def isTerminalState(gameState, depth):
            return depth == self.depth or gameState.isWin() or gameState.isLose()

        # Αναδρομική συνάρτηση αξιολόγησης με αποκοπή Alpha-Beta
        def value(state, depth, agentIndex, alpha, beta):
            if isTerminalState(state, depth):
                return self.evaluationFunction(state)
            
            # Εάν ο παίκτης είναι ο Pacman (MAX)
            if agentIndex == 0:
                return max_value(state, depth, agentIndex, alpha, beta)
            # Εάν ο παίκτης είναι φάντασμα (MIN)
            else:
                return min_value(state, depth, agentIndex, alpha, beta)

        # Συνάρτηση max-value με αποκοπή Alpha-Beta
        def max_value(state, depth, agentIndex, alpha, beta):
            v = float("-inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                v = max(v, value(successorState, depth, agentIndex + 1, alpha, beta))
                if v > beta:  # Έλεγχος για αποκοπή
                    return v
                alpha = max(alpha, v)
            return v

        # Συνάρτηση min-value με αποκοπή Alpha-Beta
        def min_value(state, depth, agentIndex, alpha, beta):
            v = float("inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                if agentIndex == state.getNumAgents() - 1:  # Αν το τρέχον από τα φαντάσματα είναι το τελευταίο
                    v = min(v, value(successorState, depth + 1, 0, alpha, beta))  # Προχωράμε στον επόμενο βαθμό βάθους και ο επόμενος παίκτης είναι ο Pacman
                else:
                    v = min(v, value(successorState, depth, agentIndex + 1, alpha, beta))  # Παραμένουμε στο ίδιο βάθος αναζήτησης
                if v < alpha:  # Έλεγχος για αποκοπή
                    return v
                beta = min(beta, v)
            return v

        # Βρίσκουμε την καλύτερη ενέργεια για τον Pacman με αποκοπή Alpha-Beta
        bestAction = None
        alpha = float("-inf")
        beta = float("inf")
        legalActions = gameState.getLegalActions(0)  # Ο Pacman έχει agentIndex = 0
        for action in legalActions:
            successorState = gameState.generateSuccessor(0, action)
            newValue = value(successorState, 0, 1, alpha, beta)  # Ξεκινάμε την αναζήτηση από βάθος 0 και ο επόμενος παίκτης είναι το πρώτο φάντασμα
            if newValue > alpha:
                alpha = newValue
                bestAction = action
        return bestAction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        # ελεγχος αν η αναζητηση εχει φτασει στο μεγιστο βαθος 
        def isTerminalState(state, depth):
            return depth == self.depth or state.isWin() or state.isLose()

        # αναδρομικά η συναρτηση αξιολογησηςn
        def value(state, depth, agentIndex):
            if isTerminalState(state, depth):
                return self.evaluationFunction(state)

            # If the player is Pacman (MAX)
            if agentIndex == 0:
                return max_value(state, depth, agentIndex)
            # If the player is a ghost (EXP)
            else:
                return exp_value(state, depth, agentIndex)

        # Max-value 
        def max_value(state, depth, agentIndex):
            v = float("-inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                v = max(v, value(successorState, depth, agentIndex + 1))
            return v

        # Exp-value 
        def exp_value(state, depth, agentIndex):
            v = 0
            legalActions = state.getLegalActions(agentIndex)
            numActions = len(legalActions)
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                # καλειται ετσι ο επομενος παικτης που ειναι ο pacman μετα τα φαντασματα
                v += 1 / numActions * value(successorState, depth + 1 if agentIndex == state.getNumAgents() - 1 else depth, (agentIndex + 1) % state.getNumAgents())
            return v

        # βρισκω το best action για τον Pacman
        bestAction = None
        bestValue = float("-inf")
        legalActions = gameState.getLegalActions(0)  # Pacman εχει agentIndex = 0
        for action in legalActions:
            successorState = gameState.generateSuccessor(0, action)
            newValue = value(successorState, 0, 1)  # ξεκιναω αναζητηση απο depth 0 και επομενος παικτης το πρωτο φαντασμα
            if newValue > bestValue:
                bestValue = newValue
                bestAction = action
        return bestAction


        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    

    pacmanPosition = currentGameState.getPacmanPosition()
    foodPositions = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    #αρχικοποιω το σκορ της αξιολογησης
    evaluationScore = currentGameState.getScore()

    # αξιολογηση της αποστασης απο τις κουκιδες
    if foodPositions:
        minFoodDistance = min([manhattanDistance(pacmanPosition, food) for food in foodPositions])
        evaluationScore += 1.0 / minFoodDistance

    # αξιολογειται ποσο κοντα ειναι τα φαντασματα για καθε φαντασμα
    for ghostState in ghostStates:
        ghostPosition = ghostState.getPosition()
        ghostDistance = manhattanDistance(pacmanPosition, ghostPosition)
        if ghostState.scaredTimer > 0:
            evaluationScore += 10.0 / (ghostDistance + 1)  # προτεραιοτητα να φαει τα φαντασματα οταν ειναι φοβισμενα
        else:
            evaluationScore -= 10.0 / (ghostDistance + 1)  # αποφυγη αν δεν ειναι φοβισμενα

    # αριθμος απο capsulew που εχουν μεινει 
    capsulePositions = currentGameState.getCapsules()
    evaluationScore -= len(capsulePositions) * 100.0  

    return evaluationScore

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
