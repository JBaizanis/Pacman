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
        """
        pacman_index = 0
        def max_value(state, depth):
            # Εάν η τρέχουσα κατάσταση είναι η τερματική (είτε νίκη είτε ήτα) επιστρέφω το score αυτής της κατάστασης.
            if state.isWin() or state.isLose():
                return state.getScore()

            v = float("-inf") # Όπως στον αλγόριθμο (ψευδοκώδικα), αρχικοποιώ το v σε -oo, όπου το v αντιπροσωπεύει την τιμή
                              # της καλύτερης ενέργειας, δηλαδή εφόσον είμαστε στον max τότε η καλύτερη ενέργεια είναι ο πράκτορας (Pacman) να επιλέξει
                              # την μεγαλύτερη τιμή ανάμεσα στα min.
            best_action = None

            # Δεδομένης της τρέχουσας κατάστασης (του Pacman) διατρέχω όλες τις νόμιμες ενέργειες που μπορεί να κάνει.
            # Για κάθε ενέργεια δημιουργώ (κάνω generate), το successor state και καλώ τη min_value για να υπολογίσω την τιμή αυτής της κατάστασης.
            # Το min_value αφορά τα φαντάσματα. Ενημερώνω το v και τη μεταβλητή best action αντίστοιχα, που περιέχει την καλύτερη ενέργεια που έχει βρει ο πράκτορας
            # (Pacman) μέχρι στιγμής.
            for action in state.getLegalActions(pacman_index):

                score = min_value(state.generateSuccessor(pacman_index, action), depth, 1)

                if score > v: # Σε περίπτωση που το score για μια ενέργεια είναι καλύτερο από ένα score μιας προηγούμενης ενέργειας, τότε ενημερώνω το v και
                              # την best_action αντίστοιχα. Ειδικότερα, για τον max, δηλαδή τον Pacman, ελέγχω την τιμή για κάθε min ενέργεια(score), βρίσκω
                              # δηλαδή αυτή με την μεγαλύτερη τιμή και αναθέτω στις μεταβλητές v, την τιμή της καλύτερης ενέργειας και στην μεταβλητή best_action
                              # την αντίστοιχη καλύτερη ενέργεια.
                    v = score
                    best_action = action

            return best_action if depth == 0 else v

        def min_value(state, depth, ghost):
            # Εάν η τρέχουσα κατάσταση είναι η τερματική (είτε νίκη είτε ήτα) επιστρέφω το score αυτής της κατάστασης.
            if state.isLose() or state.isWin():
                return state.getScore()

            # Υπολογίζω το index του επόμενου πράκτορα. Εάν ο τρέχων πράκτορας είναι ο τελευταίος, τότε αναθέτω στη μεταβλητή nextAgent το index του Pacman.
            nextΑgent = ghost + 1 if ghost < state.getNumAgents() - 1 else pacman_index

            v = float("inf") # Όπως στον αλγόριθμο (ψευδοκώδικα), αρχικοποιώ το v σε oo, όπου το v αντιπροσωπεύει την
                             # τιμή της καλύτερης ενέργειας, δηλαδή την καλύτερη ενέργεια για το φάντασμα, το οποίο προσπαθεί κάθε
                             # φορά να επιλέξει τη μικρότερη τιμή, δηλαδή αυτή που θα έχει σαν αποτέλεσμα να πληγεί ο πράκτορας (Pacman) όσο περισσότερο γίνεται,
                             # καθώς ο Pacman μετά θα έχει να επιλέξει την καλύτερη (μέγιστη) ενέργεια ανάμεσα σε όσο το δυνατό μικρότερες τιμές-ενέργειες.

            # Δεδομένης της τρέχουσας κατάστασης (του φαντάσματος) διατρέχω όλες τις νόμιμες ενέργειες που μπορεί να κάνει
            # και για κάθε ενέργεια υπολογίζω το αντίστοιχο score.
            for action in state.getLegalActions(ghost):
                # Αν ο επόμενος πράκτορας είναι ο Pacman(είμαστε στο τελευταίο φάντασμα), τότε αν το βάθος είναι το μέγιστο δυνατό φτάσαμε δηλαδή στο depth limit,
                # υπολογίζω καλώντας την evaluationFunction το score για το successor state σταματώντας να εξευρευνώ το δέντρο παραπάνω.
                # Διαφορετικά καλώ τη max_value για να συνεχίσω σε βάθος αφού δεν έχω φτάσει στο τέλος.
                if nextΑgent == pacman_index:
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                    else:
                        score = max_value(state.generateSuccessor(ghost, action), depth + 1)

                else: # Εάν ο επόμενος πράκτορας είναι επίσης φάντασμα, τότε καλώ αναδρομικά min_value.
                    score = min_value(state.generateSuccessor(ghost, action), depth, nextΑgent)

                v = min(v, score)

            return v # Επιστρέφω το v που είναι το καλύτερο δυνατό score για το φάντασμα τη δεδομένη στιγμή, δηλαδή στη δεδομένη κατάσταση και βάθος.

        return max_value(gameState, 0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Ο κώδικας είναι ίδιος με την κλάση MinimaxAgent, το μόνο που προστίθεται είναι οι μεταβλητές α και β που απαιτούνται για το pruning.
        pacman_index = 0
        def max_value(state, depth, alpha, beta):
            # Εάν η τρέχουσα κατάσταση είναι η τερματική (είτε νίκη είτε ήτα) επιστρέφω το score αυτής της κατάστασης.
            if state.isWin() or state.isLose():
                return state.getScore()

            v = float("-inf") # Όπως στον αλγόριθμο (ψευδοκώδικα), αρχικοποιώ το v σε -oo, όπου το v αντιπροσωπεύει την
                              # τιμή της καλύτερης ενέργειας, δηλαδή εφόσον είμαστε στον max τότε η καλύτερη ενέργεια είναι ο πράκτορας (Pacman) να επιλέξει
                              # την μεγαλύτερη τιμή ανάμεσα στα min.
            best_action = None

            # Δεδομένης της τρέχουσας κατάστασης (του Pacman) διατρέχω όλες τις νόμιμες ενέργειες που μπορεί να κάνει.
            # Για κάθε ενέργεια δημιουργώ (κάνω generate), το successor state και καλώ τη min_value για να υπολογίσω την τιμή αυτής της κατάστασης.
            # Το min_value αφορά τα φαντάσματα. Ενημερώνω το v και τη μεταβλητή best action αντίστοιχα, που περιέχει την καλύτερη ενέργεια που έχει βρει ο πράκτορας
            # (Pacman) μέχρι στιγμής.
            for action in state.getLegalActions(pacman_index):

                score = min_value(state.generateSuccessor(pacman_index, action), depth, 1, alpha, beta)

                if score > v: # Σε περίπτωση που το score για μια ενέργεια είναι καλύτερο από ένα score μιας προηγούμενης ενέργειας, τότε ενημερώνω το v και
                              # την best_action αντίστοιχα. Ειδικότερα, για τον max, δηλαδή τον Pacman, ελέγχω την τιμή για κάθε min ενέργεια(score), βρίσκω
                              # δηλαδή αυτή με την μεγαλύτερη τιμή και αναθέτω στις μεταβλητές v, την τιμή της καλύτερης ενέργειας και στην μεταβλητή best_action
                              # την αντίστοιχη καλύτερη ενέργεια.
                    v = score
                    best_action = action
                alpha = max(alpha, v) # Υπολογίζω το α αφού βρίσκομαι σε max state, το οποίο αναπαριστά την καλύτερη ενέργεια που έχει βρεθεί μέχρι στιγμής για
                                      # τον maximizing player, δηλαδή τον Pacman.

                if v > beta: # Όπως ορίζει ο αλγόριθμος αν ν>β κάνω "prune", επιστρέφω δηλαδή το v και σταματώ την αναζήτηση. Πιο συγκεκριμένα, αν v>beta τότε
                    return v # το "κλαδί" αυτό έχει παράξει μια τιμή μεγαλύτερη από αυτήν που θα "επέτρεπαν" τα φαντάσματα (Minimizer). Άρα, δεν χρειάζεται να
                             # συνεχίσω να εξευρευνώ αυτό το "κλαδί", καθώς ο minimizer (φαντάσματα) δεν θα επιλέξουν αυτό το "κλαδί".

            return best_action if depth == 0 else v

        def min_value(state, depth, ghost, alpha, beta):
            # Εάν η τρέχουσα κατάσταση είναι η τερματική (είτε νίκη είτε ήτα) επιστρέφω το score αυτής της κατάστασης.
            if state.isLose() or state.isWin():
                return state.getScore()

            # Υπολογίζω το index του επόμενου πράκτορα. Εάν ο τρέχων πράκτορας είναι ο τελευταίος, τότε αναθέτω στη μεταβλητή next_agent το index του Pacman.
            next_agent = ghost + 1 if ghost < state.getNumAgents() - 1 else pacman_index

            v = float("inf") # Όπως στον αλγόριθμο (ψευδοκώδικα), αρχικοποιώ το v σε oo, όπου το v αντιπροσωπεύει την
                             # τιμή της καλύτερης ενέργειας, δηλαδή την καλύτερη ενέργεια για το φάντασμα, το οποίο προσπαθεί κάθε
                             # φορά να επιλέξει τη μικρότερη τιμή, δηλαδή αυτή που θα έχει σαν αποτέλεσμα να πληγεί ο πράκτορας (Pacman) όσο περισσότερο γίνεται,
                             # καθώς θα έχει να επιλέξει μετά την καλύτερη (μέγιστη) ενέργεια ανάμεσα σε όσο το δυνατό μικρότερες τιμές-ενέργειες.

            # Δεδομένης της τρέχουσας κατάστασης (του φαντάσματος) διατρέχω όλες τις νόμιμες ενέργειες που μπορεί να κάνει
            # και για κάθε ενέργεια υπολογίζω το αντίστοιχο score.
            for action in state.getLegalActions(ghost):
                # Αν ο επόμενος πράκτορας είναι ο Pacman(είμαστε στο τελευταίο φάντασμα), τότε αν το βάθος είναι το μέγιστο δυνατό φτάσαμε δηλαδή στο depth limit,
                # υπολογίζω καλώντας την evaluationFunction το score για το successor state σταματώντας να εξευρευνώ το δέντρο παραπάνω.
                # Διαφορετικά καλώ τη max_value για να συνεχίσω σε βάθος αφού δεν έχω φτάσει στο τέλος.
                if next_agent == pacman_index:
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                    else:
                        score = max_value(state.generateSuccessor(ghost, action), depth + 1, alpha, beta)

                else: # Εάν ο επόμενος πράκτορας είναι επίσης φάντασμα, τότε καλώ αναδρομικά min_value.

                    score = min_value(state.generateSuccessor(ghost, action), depth, next_agent, alpha, beta)

                v=min(v, score)
                beta = min(beta, v) # Υπολογίζω το β αφού βρίσκομαι σε min state, το οποίο αναπαριστά την καλύτερη ενέργεια που έχει βρεθεί μέχρι στιγμής για
                                    # τον minimizing player, δηλαδή το φάντασμα.

                if v < alpha: # Όπως ορίζει ο αλγόριθμος αν ν<α κάνω "prune", επιστρέφω δηλαδή το v και σταματώ την αναζήτηση. Πιο συγκεκριμένα, αν v<alpha τότε
                    return v  # το "κλαδί" αυτό έχει παράξει μια τιμή μικρότερη από αυτήν που θα "επέτρεπε" ο Pacman (Maximizer). Άρα, δεν χρειάζεται να
                              # συνεχίσω να εξευρευνώ αυτό το "κλαδί", καθώς ο maximizer (Pacman) ψάχνει για τιμές >=alpha, άρα αφού η τιμή του v είναι
                              # μικρότερη του alpha δεν χρειάζεται να συνεχίσω να εξερευνώ αυτό το "κλαδί".
            return v

        return max_value(gameState, 0, float("-inf"), float("inf"))

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman_index = 0
        def max_value(state, depth):
            # Εάν η τρέχουσα κατάσταση είναι η τερματική (είτε νίκη είτε ήτα) ή φτάσαμε στο depth limit επιστρέφω την αξιολόγηση αυτής της κατάστασης.
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = float("-inf") # Όπως στον αλγόριθμο (ψευδοκώδικα), αρχικοποιώ το v σε -oo, όπου το v αντιπροσωπεύει την
                              # τιμή της καλύτερης ενέργειας, δηλαδή εφόσον είμαστε στον max, ο max θέλει να μεγιστοποιήσει την αναμενόμενη (expected) ωφέλεια του.
            best_action = None

            # Δεδομένης της τρέχουσας κατάστασης (του Pacman) διατρέχω όλες τις νόμιμες ενέργειες που μπορεί να κάνει.
            # Για κάθε ενέργεια δημιουργώ (κάνω generate), το successor state και καλώ τη exp_value για να υπολογίσω την τιμή αυτής της κατάστασης.
            # Το exp_value αφορά τα φαντάσματα. Ενημερώνω το v και τη μεταβλητή best action αντίστοιχα, που περιέχει την καλύτερη ενέργεια που έχει βρει ο πράκτορας
            # (Pacman) μέχρι στιγμής.
            for action in state.getLegalActions(pacman_index):

                score = exp_value(state.generateSuccessor(pacman_index, action), depth, 1)

                if score > v: # Σε περίπτωση που το score για μια ενέργεια είναι καλύτερο από ένα score μιας προηγούμενης ενέργειας, τότε ενημερώνω το v και
                              # την best_action αντίστοιχα. Ειδικότερα, για τον max, δηλαδή τον Pacman, ελέγχω την τιμή για κάθε exp ενέργεια, βρίσκω
                              # δηλαδή αυτή με την μεγαλύτερη τιμή και αναθέτω στις μεταβλητές v, την τιμή της καλύτερης ενέργειας και στην μεταβλητή best_action
                              # την αντίστοιχη καλύτερη ενέργεια.
                    v = score
                    best_action = action

            return best_action if depth == 0 else v # Αν το depth είναι 0, έφτασα στην κορυφή άρα επιστρέφω την καλύτερη ενέργεια, αλλιώς επιστρέφω το v.

        def exp_value(state, depth, ghost):
            # Εάν η τρέχουσα κατάσταση είναι η τερματική (είτε νίκη είτε ήτα) ή φτάσαμε στο depth limit επιστρέφω την αξιολόγηση αυτής της κατάστασης.
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            v = 0 # Όπως στον αλγόριθμο (ψευδοκώδικα), αρχικοποιώ το v σε 0. Αρχικά δεν έχω υπολογίσει expected values για τα successor states που προκύπτουν από
                  # τις ενέργειες του τρέχοντος φαντάσματος. Καθώς διατρέχω όλες τις νόμιμες ενέργειες του φαντάσματος υπολογίζω την αναμενόμενη τιμή κάθε διαδόχου
                  # και την αναθέτω στο v.

            # Δεδομένης της τρέχουσας κατάστασης (του φαντάσματος) διατρέχω όλες τις νόμιμες ενέργειες που μπορεί να κάνει
            # και για κάθε ενέργεια υπολογίζω το αντίστοιχο score.
            for action in state.getLegalActions(ghost):
                prob = 1.0 / len(state.getLegalActions(ghost)) # Η πιθανότητα για κάθε ενέργεια, είναι ίδια όπως αναφέρεται στην εκφώνηση.
                if ghost == state.getNumAgents() - 1: # Αν είμαστε στο τελευταίο φάντασμα τότε μετά είναι η σειρά του Pacman να παίξει, άρα καλώ την max_value.
                    v += prob * max_value(state.generateSuccessor(ghost, action), depth + 1)
                else: # Εάν ο επόμενος πράκτορας είναι επίσης φάντασμα, τότε καλώ αναδρομικά min_value.
                    v += prob * exp_value(state.generateSuccessor(ghost, action), depth, ghost + 1)

            return v

        return max_value(gameState, 0)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    """
    # Παίρνω πληροφορίες για το τρέχων state.
    pacman_position = currentGameState.getPacmanPosition() # Παίρνω τη θέση του pacman.
    currentScore = currentGameState.getScore() # Παίρνω το τρέχων score του pacman.
    foodList = currentGameState.getFood().asList() # Λίστα των κουκίδων που είναι διαθέσιμες.
    capsulesLeft = len(currentGameState.getCapsules()) # Λίστα των μεγάλων καψουλών (power pellets) που είναι διαθέσιμες.
    foodLeft = len(foodList) # Αριθμός των κουκίδων φαγητού που έχουν απομείνει
    alive_ghosts = [ghost for ghost in currentGameState.getGhostStates() if not ghost.scaredTimer] # Λίστα από τα φαντάσματα που δεν είναι φοβισμένα.
    scared_ghosts = [ghost for ghost in currentGameState.getGhostStates() if ghost.scaredTimer] # Λίστα από τα φοβισμένα φαντάσματα.

    # Υπολογίζω την ελάχιστη απόσταση Manhattan από τον pacman στην κοντινότερη κουκίδα.
    distanceToClosestFood = min(util.manhattanDistance(pacman_position, food) for food in foodList) if foodList else 0
    # Υπολογίζω την ελάχιστη απόσταση Manhattan από τον pacman στο κοντινότερο μη φοβισμένο φάντασμα. Αν δεν υπάρχουν active ghosts τότε αναθέτω την τιμή της
    # μεταβλητής σε oo.
    distanceToClosestActiveGhost = min(util.manhattanDistance(pacman_position, ghost.getPosition()) for ghost in alive_ghosts) if alive_ghosts else float("inf")
    distanceToClosestActiveGhost = max(distanceToClosestActiveGhost, 5)  # Αυτό διασφαλίζει ότι η απόσταση από το κοντινότερο φάντασμα είναι το πολύ 5. Είναι ένα είδους threshold, διασφαλίζοντας ότι η ποινή που σχετίζεται με την απόσταση από το πλησιέστερο ενεργό φάντασμα δεν γίνεται πολύ ακραία.
    # Υπολογίζω την ελάχιστη απόσταση Manhattan από τον pacman στο κοντινότερο φοβισμένο φάντασμα. Αν δεν υπάρχουν scared ghosts τότε αναθέτω την τιμή της
    # μεταβλητής σε oo.
    distanceToClosestScaredGhost = min(util.manhattanDistance(pacman_position, ghost.getPosition()) for ghost in scared_ghosts) if scared_ghosts else 0

    # Υπολογίζω το score (τιμή της συνάρτησης αξιολόγησης) με βάση τις παραπάνω παραμέτρους.
    score = currentScore - 0.2 * distanceToClosestFood - 16 * (1. / distanceToClosestActiveGhost) - 0.2 * distanceToClosestScaredGhost - 20 * capsulesLeft - 4 * foodLeft

    # Το distanceToClosestFood δίνει penalty στον pacman, βάση της απόστασης του από το κοντινότερο food pellet. Το penalty μικραίνει όσο ο pacman πηγαίνει πιο κοντά
    # στο φαγητό κάνοντας έτσι τον pacman να πηγαίνει πιο κοντά στα food pellets.

    # Το distanceToClosestActiveGhost δίνει penalty στον pacman, με βάση την απόσταση από το κοντινότερο μη φοβισμένο φάντασμα. Η ποινή είναι αντιστρόφως ανάλογη
    # της απόστασης, δηλαδή όσο πιο κοντά είναι ο pacman σε ένα ενεργό φάντασμα τόσο πιο μεγάλη ποινή έχει.

    # Το distanceToClosestScaredGhost δίνει penalty στον pacman με βάση την απόσταση από το κοντινότερο φοβισμένο φάντασμα. Ωθείται, δηλαδή στο να βρίσκεται
    # κοντά σε φοβισμένα φαντάσματα. Το penalty ωστόσο είναι σχετικά χαμηλό σε σχέση με το penalty όταν είναι κοντά σε μη φοβισμένο φάντασμα. Όσο πιο κοντά είναι
    # σε φοβισμένο φάντασμα τόσο μικρότερο είναι και το πέναλτι και το αντίστροφο.

    # Το capsulesLeft δίνει penalty στον pacman με βάση τα power pellets που έχουν απομείνει στο παιχνίδι. Το penalty
    # είναι μικρότερο όσο υπάρχουν λίγες κάψουλες(power pellets), δίνοντας κίνητρο στον pacman να καταναλώνει κάψουλες για να αποκτήσει την ικανότητα να τρώει φαντάσματα.

    # Το foodLeft δίνει penalty στον pacman με βάση τον αριθμό των food pellets που έχουν απομείνει στο παιχνίδι.
    # Η ποινή είναι μικρή αν δεν έχουν απομείνει πολλά food pellets,
    # ενθαρρύνοντας τον pacman να φάει όσο το δυνατόν περισσότερο φαγητό για να προχωρήσει προς τη νίκη στο παιχνίδι.
    return score

# Abbreviation
better = betterEvaluationFunction