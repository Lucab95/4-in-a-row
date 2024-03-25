from game_state import GameState
import ai_model
import pygame as p
from move import Move
WIDTH = HEIGHT = 512
INFOWIDTH = 400
ROWS = 6
COLUMNS = 7
SQ_SIZE = HEIGHT // 10
LABEL = SQ_SIZE
MAX_FPS = 15
IMAGES = {}

""" PARAMETER FOR THE AI"""
maxDepth = 3
moveOrdering = False
iDS = False

def drawMenu( screen):
        center = p.display.get_surface().get_size()[0]/2 -LABEL*2
        font = p.font.SysFont("rockwellgrassettocorsivo", 40)
        text = font.render("Vier op een rij", True, p.Color("blue"))
        textRect = text.get_rect()
        textRect.center = (WIDTH-25, SQ_SIZE*1)
        screen.blit(text, textRect)
        font = p.font.SysFont("rockwellgrassettocorsivo", 20)
        pos1 = p.draw.rect(screen, p.Color("white"), p.Rect(center, (2 * SQ_SIZE), 200, 75), 2)
        text = font.render("Player vs Player", True, p.Color("blue"))
        textRect = text.get_rect()
        textRect.center = (pos1[0]+100, pos1[1]+35)
        screen.blit(text, textRect)
        pos2 = p.draw.rect(screen, p.Color("white"), p.Rect(center, (5 * SQ_SIZE), 200, 75), 2)
        text = font.render("AI vs Player", True, p.Color("blue"))
        textRect = text.get_rect()
        textRect.center = (pos2[0]+100, pos2[1]+35)
        screen.blit(text, textRect)
        pos3 = p.draw.rect(screen, p.Color("white"), p.Rect(center, (8 * SQ_SIZE), 200, 75), 2)
        text = font.render("Player vs AI", True, p.Color("blue"))
        textRect = text.get_rect()
        textRect.center = (pos3[0]+100, pos3[1]+35)
        screen.blit(text, textRect)
        return pos1 ,pos2 , pos3

def drawGameState(screen, gameState, validMoves, sqSelected, time):
    """graphics for the game"""
    createBoard(screen)  # draw squares on the board
    addSprites(screen, gameState.board, gameState.letters, gameState.numbers)  # draw pieces on top of squares
    drawHistory(screen, gameState.blue_to_move, gameState.history, time)
    highlightSquares(screen, gameState, validMoves, sqSelected, p.Color("yellow"))

def createBoard(screen):
    """draw squares on the board"""
    color = p.Color("white")
    for r in range(ROWS):
        for c in range(COLUMNS):
            p.draw.rect(screen, color, p.Rect((c * SQ_SIZE) + LABEL, (r * SQ_SIZE) + LABEL, SQ_SIZE, SQ_SIZE), 2)
    p.draw.rect(screen, color, p.Rect((WIDTH + LABEL + 50, SQ_SIZE + LABEL, 300, 512 - SQ_SIZE * 2)))


"""draw pieces on the board"""
def addSprites(screen, board, letters, numbers):
    """draw letters on board"""

    font = p.font.SysFont("rockwellgrassettocorsivo", 28)
    half = SQ_SIZE / 2
    for c in range(1, COLUMNS + 1):
        text = font.render(letters[c - 1], True, p.Color("blue"), p.Color("black"))
        textRect = text.get_rect()
        textRect.center = (c * SQ_SIZE + half, COLUMNS* SQ_SIZE + half)
        screen.blit(text, textRect)
    for r in range(1, ROWS + 1):
        text = font.render(numbers[r - 1], True, p.Color("blue"), p.Color("black"))
        textRect = text.get_rect()
        textRect.center = (half, r * SQ_SIZE + half)
        screen.blit(text, textRect)

    """draw pieces/sprites on board"""
    for r in range(ROWS):
        for c in range(COLUMNS):
            piece = board[r][c]
            if piece != "-":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE + LABEL, r * SQ_SIZE + LABEL, SQ_SIZE, SQ_SIZE))


def drawHistory(screen, turn, history, time):
    """draw the last 12 moves on the right label"""
    font = p.font.SysFont("rockwellgrassettocorsivo", 15)
    turn = 'Gold' if turn else 'Silver'
    text = font.render("TURN: " + str(turn), True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (WIDTH + LABEL + 50, SQ_SIZE / 2 * 3)
    screen.blit(text, textRect)
    text = font.render("AI time spent: " + str(time), True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (WIDTH + LABEL * 3 + INFOWIDTH / 2, SQ_SIZE / 2 * 3)
    screen.blit(text, textRect)

    #if there is history, print it
    if len(history) != 0:
        for i in range(len(history)):
            text = font.render(history[len(history) - i - 1], True, p.Color("black"), p.Color("white"))
            textRect = text.get_rect()
            textRect.center = (WIDTH + LABEL + INFOWIDTH / 2, 512 - (i + 1) * 30)
            screen.blit(text, textRect)
            if i > 11:
                break

def loadImages():
    pieces = ["o", "x"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gameState, moves, sqSelected, color):
    """higlights selected piece possible moves"""
    if sqSelected != ():
        r, c, = sqSelected
        if gameState.board[r][c][0] == (
                'g' if gameState.blue_to_move else 's'):  # selected Square is a piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            screen.blit(s, (c * SQ_SIZE + LABEL, r * SQ_SIZE + LABEL))
            s.fill(color)
            for move in moves:
                if move.startRow == r and move.startCol == c:  # all the moves that belong to the pawn in r,c
                    screen.blit(s, (move.endCol * SQ_SIZE + LABEL, move.endRow * SQ_SIZE + LABEL))
                    
def main():

    p.init()
    print("***Welcome to Connect Four!***")
    screen = p.display.set_mode((WIDTH + LABEL + INFOWIDTH, HEIGHT + LABEL))  # Initializing screen
    clock = p.time.Clock()
    # gameState = GameState.GameState()
    # validMoves, captureMoves = gameState.getValidMoves()
    loadImages()
    running = True
    runningMenu = True
    clickedSQ = ()  # tracks the last user's click (row,col)
    playerClicks = []  # track the clicks [(x,y),(x',y')]
    while runningMenu:
        pos = drawMenu(screen)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                # sys.exit()
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # get x,y location of mouse
                print(location) # print x,y coords
                print(pos[0].collidepoint(location))
                if pos[0].collidepoint(location):
                    # AI.ControlGold = 0
                    players_number = 2
                    runningMenu = False
                elif pos[1].collidepoint(location):
                    players_number = 1
                    AI.ControlBlue = 1
                    runningMenu =False
                elif pos[2].collidepoint(location):
                    AI.ControlBlue = 2
                    runningMenu =False
        screen.fill(p.Color("black"))
        drawMenu(screen)
        clock.tick(MAX_FPS)
        p.display.flip()
    game_state = GameState(ROWS, COLUMNS, int(players_number))
    game_state.get_valid_moves()
    AI = ai_model.AI(maxDepth,moveOrdering, iDS)
    AI.ControlGold = 0
    AITurn = False
    while game_state.running:
        requiredTime = AI.time_required
        validMoves = game_state.get_valid_moves()
        drawGameState(screen, game_state, validMoves, clickedSQ, requiredTime)
        if game_state.running:
            moveMade = False
            if game_state.turn_counter != 0:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif game_state.blue_to_move and AI.control_blue == 1 and AITurn:
                        AITurn = False
                        AI.nextAiMove(game_state)
                        drawGameState(screen, game_state, validMoves, clickedSQ, requiredTime)
                        moveMade = True
                        clickedSQ = ()  # reset
                        playerClicks = []
                    elif not game_state.blue_to_move and AI.ControlGold == 2 and AITurn:
                        AITurn = False
                        AI.nextAiMove(game_state)
                        drawGameState(screen, game_state, validMoves, clickedSQ, requiredTime)
                        moveMade = True
                        clickedSQ = ()  # reset
                        playerClicks = []
                    elif e.type == p.MOUSEBUTTONDOWN and AITurn:
                        location = p.mouse.get_pos()  # get x,y location of mouse
                        col = (location[0] - LABEL) // SQ_SIZE
                        row = (location[1] - LABEL) // SQ_SIZE
                        
                        if col >= 0 and col < COLUMNS and row >= 0 and row < ROWS:
                            clickedSQ = ()
                            playerClicks = []
                            break

                        move = Move(playerClicks[1], game_state.board)
                        if move in validMoves:
                            game_state.performMove(move)
                            moveMade = True
                            clickedSQ = ()  # reset
                            playerClicks = []
                        else:
                            playerClicks = [clickedSQ]  # second click and avoid problem when i click black squares

                    #perform the undo of the move
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_z:
                            game_state.undoMove()
                            moveMade = True

                if moveMade:  # calculate new moves only after a move was made
                    validMoves =  game_state.get_valid_moves()
                    AITurn = True #used to align
                    moveMade = False
            screen.fill(p.Color("black"))
            drawGameState(screen, game_state, validMoves, clickedSQ, requiredTime)
            clock.tick(MAX_FPS)
            p.display.flip()
            if game_state.turn_counter == 0:
                game_state.turn_counter = 1
        else:
            font = p.font.SysFont("calibri", 32)
            text = font.render(game_state.win + " player won", True, p.Color("red"), p.Color("black"))
            textRect = text.get_rect()
            textRect.center = ((WIDTH + LABEL + INFOWIDTH) / 2, HEIGHT / 2)
            drawGameState(screen, game_state, validMoves, clickedSQ, requiredTime)
            screen.blit(text, textRect)
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
    p.quit()
    
if "__main__" == __name__:
    main()