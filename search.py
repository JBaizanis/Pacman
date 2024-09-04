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
    "*** YOUR CODE HERE ***"
    visited = set() # Δημιουργώ ένα set ώστε να γνωρίζω τις επισκεφθείσες καταστάσεις.
    front = util.Stack() # Αρχικοποιώ το μέτωπο της αναζήτησης. Το μέτωπο αναπαρίσταται από μια στοίβα. Η στοίβα θα περιέχει tupples όπου κάθε tupple θα περιέχει
                         # το state (την κατάσταση) και τις ενέργειες(actions) που οδηγούν σε αυτό(το state).

    # Βάζω στη στοίβα την αρχική κατάσταση(state) μαζί με ένα άδειο action list καθώς η αρχική κατάσταση δεν έχει ενέργειες που οδηγούν σε αυτήν αφού είναι η
    # αρχική.
    front.push((problem.getStartState(), []))

    while not front.isEmpty(): # Όσο το μέτωπο δεν είναι άδειο συνεχίζω την αναζήτηση.

        currentState, currentActions = front.pop()

        # Αν η τρέχουσα κατάσταση είναι η κατάσταση στόχος(goal state), επιστρέφω τις ενέργειες που οδηγούν σε αυτήν.
        if problem.isGoalState(currentState):
            return currentActions

        # Σε περίπτωση που η τρέχουσα κατάσταση δεν είναι η κατάσταση στόχος(goal state) την προσθέτω στο set (είναι πλέον "visited"), ώστε να μην την επαναεπεξεργαστώ
        # στην συνέχεια.
        visited.add(currentState)

        # Ψάχνω τους απογόνους της τρέχουσας κατάστασης.
        successors = problem.getSuccessors(currentState)
        for successor in successors:
            successorState = successor[0]
            successorActions = successor[1]

            # Δεν ψάχνω states που τα έχω ήδη επισκεφτεί.
            if successorState not in visited:
                # Προσθέτω το successor state και τα updated actions στη στοίβα ώστε να τα ελέγξω στη συνέχεια.
                front.push((successorState, currentActions + [successorActions]))

    # Σε περίπτωση που δε βρεθεί λύση επιστρέφω μια κενή λίστα από ενέργειες.
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    front = util.Queue() # Δημιουργώ μια ουρά για την αποθήκευση των κόμβων κατά την αναζήτηση BFS.
    visited = set() # Δημιουργώ ένα set ώστε να γνωρίζω τις επισκεφθείσες καταστάσεις.

    initialState = problem.getStartState() # Παίρνω το initial state.
    initialNode = (initialState, [], 0) # Ο αρχικός κόμβος περιλαμβάνει την αρχική κατάσταση, μια άδεια λίστα από ενέργειες και κόστος 0.
    front.push(initialNode) # Προσθέτω τον πρώτο κόμβο στο μέτωπο.

    while not front.isEmpty(): # Όσο το μέτωπο δεν είναι άδειο συνεχίζω την αναζήτηση.

        currentState, currentActions, currentCost = front.pop()

        # Σε περίπτωση που έχω επισκεφτεί την τρέχουσα κατάσταση, συνεχίζω το loop στην επόμενη επανάληψη χωρίς να επεξεργαστώ αυτό το state, αφού θέλω
        # να επεξεργαστώ κάθε state μια φορά.
        if currentState in visited:
            continue

        visited.add(currentState) # Εφόσον δεν έχω επισκεφτεί την τρέχουσα κατάσταση και είναι η πρώτη φορά που την συναντώ, τότε την προσθέτω πλέον στο σύνολο
                                  # των επισκεφθέντων καταστάσεων,ώστε να μην την επαναεπεξεργαστώ στην συνέχεια.

        # Αν η τρέχουσα κατάσταση είναι η κατάσταση στόχος(goal state), επιστρέφω τις ενέργειες που οδηγούν σε αυτήν.
        if problem.isGoalState(currentState):
            return currentActions

        # Ψάχνω τους απογόνους της τρέχουσας κατάστασης.
        successors = problem.getSuccessors(currentState)
        # Κάθε απόγονος είναι ένα tupple που αποτελείται από την κατάσταση του(state), τις ενέργειες για να μεταβώ σε αυτόν(actions) και το κόστος
        # αυτών των ενεργειών.
        for successorState, successorAction, successorCost in successors:
            # Το newAction αντιπροσωπεύει μια λίστα από ενέργειες που απαιτούνται για την μετάβαση στην τρέχουσα κατατάσταση(currentState) μαζί με μια λίστα από
            # ενέργειες(successorAction) που οδηγούν από την τρέχουσα κατάσταση(currentState) στην successor κατάσταση(successorState).
            newAction = currentActions + [successorAction]
            # Το newCost είναι το άθροισμα του κόστους που απαιτείται για να μεταβώ στην τρέχουσα κατάσταση(currentState) και του κόστους μετάβασης από την τρέχουσα
            # κατάσταση στη successor κατάσταση(successorState).
            newCost = currentCost + successorCost
            newNode = (successorState, newAction, newCost)
            front.push(newNode) # Προσθέτω τον κόμβο newNode (διάδοχο) στην ουρά, ώστε να τον επεξεργαστώ στις επόμενες επαναλήψεις διατηρώντας την σειρά BFS.

    return currentActions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    front = util.PriorityQueue() # Δημιουργώ μια λίστα προτεραιότητας για την αποθήκευση των κόμβων κατά την αναζήτηση UCS.
    visited = {} # Δημιουργώ ένα λεξικό ώστε να γνωρίζω τις επισκεφθείσες καταστάσεις και τα αντίστοιχα κόστη.

    initialState = problem.getStartState() # Παίρνω το initial state.
    initalNode = (initialState,[], 0) # Ο αρχικός κόμβος περιλαμβάνει την αρχική κατάσταση, μια άδεια λίστα από ενέργειες και κόστος 0.
    front.push(initalNode,0) # Προσθέτω τον πρώτο κόμβο στο μέτωπο.

    while not front.isEmpty(): # Όσο το μέτωπο δεν είναι άδειο συνεχίζω την αναζήτηση.

        currentState, currentActions, currentCost = front.pop()

        # Σε περίπτωση που έχω επισκεφθεί την τρέχουσα κατάσταση(state) και το κόστος για να φτάσω σε αυτήν είναι >= από αυτό που γνωρίζω ήδη για αυτήν(υπάρχει
        # στο visited λεξικό), τότε συνεχίζω στην επόμενη επανάληψη, χωρίς να επεξεργαστώ το τρέχων state καθώς στον UCS στόχος είναι, να φτάνω σε κάθε κόμβο
        # με το λιγότερο δυνατό κόστος.
        if currentState in visited and currentCost >= visited[currentState]:
            continue

        visited[currentState] = currentCost # Εφόσον δεν έχω επισκεφτεί την τρέχουσα κατάσταση και είναι η πρώτη φορά που την συναντώ, τότε την προσθέτω πλέον στο λεξικό
                                            # των επισκεφθέντων καταστάσεων. Για αυτήν την κατάσταση αντιστοιχεί
                                            # και ένα κόστος. Αφού έχω λεξικό το κόστος είναι η τιμή (value) του κλειδιού, δηλαδή της κατάστασης. Άρα, μαζί
                                            # με το key που είναι η κατάσταση, αντιστοιχώ και το αντίστοιχο κόστος της.

        # Αν η τρέχουσα κατάσταση είναι η κατάσταση στόχος(goal state), επιστρέφω τις ενέργειες που οδηγούν σε αυτήν.
        if problem.isGoalState(currentState):
            return currentActions

        # Ψάχνω τους απογόνους της τρέχουσας κατάστασης.
        successors = problem.getSuccessors(currentState)
        # Κάθε απόγονος είναι ένα tupple που αποτελείται από την κατάσταση του(state), τις ενέργειες για να μεταβώ σε αυτή(actions) και το κόστος
        # αυτών των ενεργειών. Τέλος, προσθέτω αυτόν τον κόμβο στην priority queue για further exploration.
        for successorState, successorAction, successorCost in successors:
            # Το newAction αντιπροσωπεύει μια λίστα από ενέργειες που απαιτούνται για την μετάβαση στην τρέχουσα κατατάσταση(currentState) μαζί με μια λίστα από
            # ενέργειες(successorAction) που οδηγούν από την τρέχουσα κατάσταση(currentState) στην successor κατάσταση(successorState).
            newAction = currentActions + [successorAction]
            # Το newCost είναι το άθροισμα του κόστους που απαιτείται για να μεταβώ στην τρέχουσα κατάσταση(currentState) και του κόστους μετάβασης από την τρέχουσα
            # κατάσταση στη successor κατάσταση(successorState).
            newCost = currentCost + successorCost
            newNode = (successorState, newAction, newCost)
            front.push(newNode, newCost) # Προσθέτω τον κόμβο newNode (διάδοχο) στην ουρά προτεραιότητας με το αντίστοιχο κόστος σαν προτεραιότητα. Αυτό διασφαλίζει,
                                         # ότι ο κόμβος με το μικρότερο κόστος θα εξετάζεται κάθε φορά στην συνέχεια, διασφαλίζοντας την σωστή σειρά για τον UCS.

    return currentActions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    front = util.PriorityQueue() # Δημιουργώ μια λίστα προτεραιότητας για την αποθήκευση των κόμβων κατά την αναζήτηση A*.
    visited = set() # Δημιουργώ ένα set ώστε να γνωρίζω τις επισκεφθείσες καταστάσεις.

    initial_state = problem.getStartState() # Παίρνω το initial state.
    initial_node = (initial_state, [], 0) # Ο αρχικός κόμβος περιλαμβάνει την αρχική κατάσταση, μια άδεια λίστα από ενέργειες και κόστος 0.
    front.push(initial_node, 0) # Προσθέτω τον πρώτο κόμβο στο μέτωπο.

    while not front.isEmpty(): # Όσο το μέτωπο δεν είναι άδειο συνεχίζω την αναζήτηση.

        currentState, currentActions, currentCost = front.pop()

        # Σε περίπτωση που έχω επισκεφτεί την τρέχουσα κατάσταση, συνεχίζω το loop στην επόμενη επανάληψη χωρίς να επεξεργαστώ αυτό το state, καθώς όπως στον
        # BFS στον A*, θέλω να αποφύγω την επαναεπεξεργασία κόμβων που έχω ήδη επεξεργαστεί. Αυτό, αποτρέπει τον αλγόριθμο από το να χάνει χρόνο σε καταστάσεις
        # που έχω ήδη επισκεφτεί, κάτι το οποίο είναι ιδιαίτερα σημαντικό στον Α*, όπου το κόστος είναι σημαντικός παράγοντας.
        if currentState in visited:
            continue

        visited.add(currentState) # Εφόσον δεν έχω επισκεφτεί την τρέχουσα κατάσταση και είναι η πρώτη φορά που την συναντώ, τότε την προσθέτω πλέον στο σύνολο
                                  # των επισκεφθέντων καταστάσεων,ώστε να μην την επαναεπεξεργαστώ στην συνέχεια.

        # Αν η τρέχουσα κατάσταση είναι η κατάσταση στόχος(goal state), επιστρέφω τις ενέργειες που οδηγούν σε αυτήν.
        if problem.isGoalState(currentState):
            return currentActions

        # Ψάχνω τους απογόνους της τρέχουσας κατάστασης.
        successors = problem.getSuccessors(currentState)
        # Κάθε απόγονος είναι ένα tupple που αποτελείται από την κατάσταση του(state), τις ενέργειες για να μεταβώ σε αυτή(actions) και το κόστος
        # αυτών των ενεργειών. Τέλος, προσθέτω αυτόν τον κόμβο στην priority queue για further exploration.
        for successorState, successorAction, successorCost in successors:
            # Το newAction αντιπροσωπεύει μια λίστα από ενέργειες που απαιτούνται για την μετάβαση στην τρέχουσα κατατάσταση(currentState) μαζί με μια λίστα από
            # ενέργειες(successorAction) που οδηγούν από την τρέχουσα κατάσταση(currentState) στην successor κατάσταση(successorState).
            newAction = currentActions + [successorAction]
            # Το newCost είναι το άθροισμα του κόστους που απαιτείται για να μεταβώ στην τρέχουσα κατάσταση(currentState) και του κόστους μετάβασης από την τρέχουσα
            # κατάσταση στην successor κατάσταση(successorState).
            newCost = currentCost + successorCost
            newNode = (successorState, newAction, newCost)

            # Υπολογίζω την προτεραιότητα του κόμβου(newNode) η οποία είναι το άθροισμα του newCost και της τιμής που επιστρέφει η ευρετική συνάρτηση.
            priority = newCost + heuristic(successorState, problem)
            front.push(newNode, priority) # Προσθέτω τον κόμβο στο μέτωπο μαζί με την αντίστοιχη προτεραιότητα, όπου η προτεραιότητα χρησιμοποείται για την σειρά
                                          # με την οποία οι κόμβοι του μετώπου θα γίνουν expand.

    return currentActions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
