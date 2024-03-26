import time
from copy import deepcopy
import game_state as GameState
import random

class AI():
    def __init__(self, maxDepth, moveOrdering, iDS):

        self.time_required = 0
        self.maxDepth = maxDepth
        self.visitedNode = 0
        self.table = [[[random.randint(1, 2 ** 64 - 1) for i in range(3)] for j in range(11)] for k in
                      range(11)]  # initialize a table with random values for the 3 different pieces

        self.TT = dict({})
        self.moveOrdering = moveOrdering
        self.iterativeDeepeningSearch = iDS
        self.timerIDS = 5
        self.control_blue = True
    
    def random_move(self, validMoves):
        return random.choice(validMoves)

    def evaluationFunction(self, gameState, goldToMove):
        """Evaluate the state to decide the most convenient move"""
        evalValue = 0

        #get flag position
        fR, fC = gameState.flagShipPosition
        killScore = 0

        #flagship killed
        if gameState.flagShip == 0:
            killScore = -1000 if goldToMove else -1500
        evalValue += killScore

        #check if flag can escape
        if fR == 0: evalValue += 500
        if fR == 10: evalValue += 500
        if fC == 0: evalValue += 500
        if fC == 10: evalValue += 500

        #check if flag is under attacck
        directions = ((-1, -1), (1, 1), (1,-1), (-1, 1))
        for d in directions:
            row = fR + d[0]
            col = fC + d[1]
            if 0 <= row <= 10 and 0 <= col <= 10:
                if gameState.board[row][col] == "sP": evalValue = 500
        evalValue += 10 * gameState.goldFleet - 6 * gameState.silverFleet

        # flagship under attacck
        return evalValue


    def nextAiMove(self, state):
        start_time = time.time()
        """get the next AI move"""
        self.visitedNode = 0
        print(">>AI calculating next move<<")
        gameState = deepcopy(state)
        if self.iterativeDeepeningSearch:
            score,move = self.IDS(gameState)
        else:
            score, move = self.miniMaxAlphaBeta(self.maxDepth, gameState, gameState.blue_to_move,
                                                             float('-inf'), float('inf'))
        print("Evaluation with score:",score,"visited node:", self.visitedNode)
        timeSpent = time.time() - start_time
        self.timeRequired += timeSpent
        self.timeRequired = round(self.timeRequired, 2) #round to xx.xx seconds
        print(">>Ai spent %s s <<" % (round(timeSpent, 2)))
        if move != "":
            state.performMove(move)
        # return move

    def nextState(self, move, gameState):
        """return the new fake state after executing the test move"""
        nextGameState = deepcopy(gameState)
        nextGameState.DEBUG = False
        nextGameState.perform_move(move, nextGameState.player_simbol[nextGameState.current_player])
        return nextGameState

    def miniMaxAlphaBeta(self, depth, game_state, blue_to_move, alpha, beta):
        hashKey = self.calculateHash(game_state)
        oldA = alpha  # save previous alpha
        oldB = beta
        self.visitedNode += 1
        n = self.retrieve(hashKey)  # check if it's a already seen state, -1 if not found
        if n != -1:
            if n[0] >= depth:
                if n[3] == "eX":
                    return n[1], n[2]
                elif n[3] == "lB":
                    alpha = max(alpha, n[1])
                elif n[3] == "uB":
                    beta = min(beta, n[1])
                if alpha >= beta:
                    return n[1], n[2]
        #leaf node
        if depth == 0:
            return self.evaluationFunction(game_state, game_state.blue_to_move),""

        #getMoves for new state
        allMoves = game_state.get_valid_moves()
        # random.shuffle(allMoves)

        #move ordering
        if self.moveOrdering:
            scoreList = []
            for action in allMoves:
                order_state = self.nextState(action, game_state)
                score = self.evaluationFunction(order_state, order_state.blue_to_move)
                scoreList.append(score)
            sortedMoves = list(zip(scoreList, allMoves))
            if blue_to_move:
                sortedMoves.sort(key=lambda mv: mv[0], reverse=True)
            else:
                sortedMoves.sort(key=lambda mv: mv[0], reverse=False)
            allMoves = [move for _, move in sortedMoves] #removes the score


        best_value = float('-inf') if blue_to_move else float('inf')
        action_target = ""

        #Minimax
        for action in allMoves:
            new_gameState = self.nextState(action, game_state)
            eval_child, action_child = self.miniMaxAlphaBeta(depth - 1, new_gameState, new_gameState.running,
                                                             new_gameState.goldToMove, alpha, beta)

            #alpha-beta
            if blue_to_move and best_value < eval_child:
                best_value = eval_child
                action_target = action
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not blue_to_move) and best_value > eval_child:
                best_value = eval_child
                action_target = action
                beta = min(beta, best_value)
                if beta <= alpha:
                    break


        #TT storage
        if best_value <= oldA:
            flag = "uB"
        elif best_value >= oldB:
            flag = "lB"
        else:
            flag = "eX"
        hashKey = self.calculateHash(game_state)
        info = (depth, best_value, action_target, flag)
        self.store(hashKey, info)
        return best_value, action_target

    def IDS(self, gameState):
        bestS = float("-inf") if gameState.goldToMove else float("inf")
        bestM = ""
        tot_timer = 20
        currentMaxDepth = 1
        while True:
            start_time = time.time()
            self.timerIDS = 10  # 5 secs per depth
            score, move = self.miniMaxAlphaBetaIDS(currentMaxDepth, gameState, gameState.stillPlay,
                                                   gameState.goldToMove,
                                                   float('-inf'), float('inf'))
            end_time = time.time()
            current_time_passed = end_time - start_time
            tot_timer -= current_time_passed
            if gameState.goldToMove:
                if score > bestS:
                    bestS = score
                    bestM = move
            else:
                if score < bestS:
                    bestS = score
                    bestM = move
            currentMaxDepth += 1
            if currentMaxDepth > self.maxDepth:
                break
            if tot_timer < 0:
                break
        return bestS, bestM

    def miniMaxAlphaBetaIDS(self, depth, gameState, stillPlay, goldToMove, alpha, beta):
        start_time = time.time()
        hashKey = self.calculateHash(gameState)
        oldA = alpha  # save previous alpha
        oldB = beta
        self.visitedNode += 1
        n = self.retrieve(hashKey)  # check if it's a already seen state, -1 if not found
        if n != -1:
            if n[0] >= depth:
                if n[3] == "eX":
                    return n[1], n[2]
                elif n[3] == "lB":
                    alpha = max(alpha, n[1])
                elif n[3] == "uB":
                    beta = min(beta, n[1])
                if alpha >= beta:
                    return n[1], n[2]
        # leaf node
        if depth == 0 or not stillPlay or self.timerIDS < 0:
            return self.evaluationFunction(gameState, gameState.goldToMove), ""

        # getMoves for new state
        allMoves, captureMoves = gameState.getValidMoves()
        for move in captureMoves:
            allMoves.append(move)
        # random.shuffle(allMoves)

        # move ordering
        if self.moveOrdering:
            scoreList = []
            for action in allMoves:
                order_state = self.nextState(action, gameState)
                score = self.evaluationFunction(order_state, order_state.goldToMove)
                scoreList.append(score)
            sortedMoves = list(zip(scoreList, allMoves))
            if goldToMove:
                sortedMoves.sort(key=lambda mv: mv[0], reverse=True)
            else:
                sortedMoves.sort(key=lambda mv: mv[0], reverse=False)
            allMoves = [move for _, move in sortedMoves]  # removes the score

        best_value = float('-inf') if goldToMove else float('inf')
        action_target = ""

        # Minimax
        for action in allMoves:
            new_gameState = self.nextState(action, gameState)
            eval_child, action_child = self.miniMaxAlphaBetaIDS(depth - 1, new_gameState, new_gameState.stillPlay,
                                                                new_gameState.goldToMove, alpha, beta)

            # alpha-beta
            if goldToMove and best_value < eval_child:
                best_value = eval_child
                action_target = action
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not goldToMove) and best_value > eval_child:
                best_value = eval_child
                action_target = action
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        # TT storage
        if best_value <= oldA:
            flag = "uB"
        elif best_value >= oldB:
            flag = "lB"
        else:
            flag = "eX"

        end_time = time.time()
        time_spent = end_time - start_time
        self.timerIDS = self.timerIDS - time_spent

        hashKey = self.calculateHash(gameState)
        info = (depth, best_value, action_target, flag)
        self.store(hashKey, info)
        return best_value, action_target

    def calculateHash(self, gameState):
        """calculates the Zobrist hash for the current board"""
        board = gameState.board
        hash = 0
        for r in range(len(board)):  # number of rows
            for c in range(len(board[0])):  # number of columns
                piece = board[r][c]
                if piece != "-":
                    hash ^= self.table[r][c][self.calculateIndex(piece)]
        return hash

    def calculateIndex(self, piece):
        """calculate the index for every piece-> empty = -1, silver = 0, gold=1, flagShip = 2"""
        if piece == "sP":
            return 0
        elif piece == "gP":
            return 1
        else:
            return 2

    def retrieve(self, hashKey):
        """check in the TT if the state already exists"""
        n = self.TT.get(hashKey)
        if n is not None:
            return n
        return -1

    def store(self, hashKey, info):
        """store the state inside the TT"""
        self.TT[hashKey] = info

    """negaMax implementation"""
    def negaMaxAlphaBeta(self, depth, gameState, stillPlay, goldToMove, alpha, beta):
        self.visitedNode += 1
        if depth == self.maxDepth or not stillPlay:
            return self.evaluationFunction(gameState, gameState.goldToMove), ""
        allMoves, captureMoves = gameState.getValidMoves()
        for move in captureMoves:
            allMoves.append(move)
        score = float('-inf')
        action_target = ""
        for action in allMoves:
            previousMove=gameState.goldToMove
            new_gameState = self.nextState(action, gameState)
            if previousMove != new_gameState.goldToMove:

                value, child = self.negaMaxAlphaBeta(depth + 1, new_gameState, new_gameState.stillPlay,
                                                            new_gameState.goldToMove, -beta, -alpha)
                value = value * -1
            else:
                value, child = self.negaMaxAlphaBeta(depth + 1, new_gameState, new_gameState.stillPlay,
                                                            new_gameState.goldToMove, alpha, beta)
                value = value * -1
            if value > 10000:
                gameState.stillPlay = False
            if value < -10000:
                gameState.stillPlay = False
            if value > score:
                score = value
                action_target = action
            if score > alpha: alpha = score
            if score >= beta: break

        return score, action_target
