#Imported Modules
import pygame
import time
import copy
import random

#Global Variables / Objects, and Initialization of Pygame
pygame.init()

display_width = 440
display_height = 540
tile_size = 90

gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

Puzzle_Border_IMG = pygame.image.load("puzzle_border.png")
Puzzle_IMG = pygame.image.load("15-Puzzle.png")
Empty_Square_IMG = pygame.image.load("blank_square.png")
Solve_Button_IMG = pygame.image.load("solve_button.png")
Solve_Button_Hover_IMG = pygame.image.load("solve_button_hover.png")

#Board_State stores the current board in a 2-dimensional array.
Board_State = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]

#Open_Tile_Pos is the position of the empty tile on the board in x-y coordinates
#The top-left corner of the board is [0,0], the top-right is [0,3], etc.
Open_Tile_Pos = [3,3]


#-------------------------------------------------------------------------------
#Functions

#Adds a 2-dimensional vector to Open_Tile_Pos
def AddVectors(vector_1,vector_2):
    x_component = vector_1[0] + vector_2[0]
    y_component = vector_1[1] + vector_2[1]

    return [x_component,y_component]


#Returns a 2-dimensional vector that corrseponds to the 'direction' string
def DefineDirectionVector(direction):
    vector_dict = {'left':[-1,0], 'right':[1,0],
                   'up':[0,-1], 'down':[0,1]}
    
    vector = vector_dict[direction]
    return vector


#Returns the oppostie direction as a string.  e.g. f('left') --> 'right'
def OppositeDirection(direction):
    opposite_direction_dict = {'left':'right', 'right':'left',
                      'up':'down', 'down':'up'}

    return opposite_direction_dict[direction]


#Returns a list of possible moves that ensures no backtracking
def FindPossibleMoves(Open_Square,Last_Move):
    possible_moves = ['left','right','up','down']

    if Open_Square[0] == 0:
        possible_moves.remove('left')
    if Open_Square[0] == 3:
        possible_moves.remove('right')
    if Open_Square[1] == 0:
        possible_moves.remove('up')
    if Open_Square[1] == 3:
        possible_moves.remove('down')

    opposite_move = OppositeDirection(Last_Move)
    if opposite_move in possible_moves:
        possible_moves.remove(opposite_move)


    return possible_moves

    
#Creates the starting board
def InitializeBoard():
    gameDisplay.blit(Puzzle_Border_IMG,(0,0))
    
    for tile in range(0,16):
        DisplayTile(tile,tile%4,int(tile/4))


#Shuffles the board using 500 randomly generated moves
#Note that the shuffling algorithm does not backtrack on consectutive moves
#I decided to use a sequence of random moves instead of randomly generating
#   the pieces since this guarantees that the puzzle will be solveable
def ShuffleBoard():
    Last_Move = 'down'
    
    for move in range(0,500):
        possible_moves = FindPossibleMoves(Open_Tile_Pos,Last_Move)

        random_index = random.randrange(len(possible_moves))
        Move(possible_moves[random_index])

        Last_Move = possible_moves[random_index]


#Displays a tile to the screen
#If the bottom-right tile is passed into this function,
#   then a black square will be displayed instead.
def DisplayTile(tile_number,x_pos,y_pos):
    
    top_left_margin = 20
    tile_offset_x = (tile_size+10)*x_pos
    tile_offset_y = (tile_size+10)*y_pos

    x = top_left_margin + tile_offset_x
    y = top_left_margin + tile_offset_y

    tile_sprite_x = 90 * (tile_number % 4)
    tile_sprite_y = 90 * (int(tile_number / 4))

    if tile_number == 15:
        surface = Empty_Square_IMG
        tile_sprite_x = 0
        tile_sprite_y = 0
    else:
        surface = Puzzle_IMG
        
    gameDisplay.blit(surface,(x,y),(tile_sprite_x,tile_sprite_y,90,90))
    pygame.display.update()


#Calls the appropriate DisplayTile() functions in accordance
#   with the movement vector
def DisplayMove(Direction_Vector):
    old_tile_pos = Open_Tile_Pos
    new_tile_pos = AddVectors(Open_Tile_Pos,Direction_Vector)

    old_tile_id = 15
    new_tile_id = Board_State[new_tile_pos[1]][new_tile_pos[0]]

    DisplayTile(old_tile_id, new_tile_pos[0],new_tile_pos[1])
    DisplayTile(new_tile_id, old_tile_pos[0],old_tile_pos[1])

    pygame.display.update()


#Updates the BoardState variable in accordance with a move
def UpdateBoardState(Direction_Vector):
    global Board_State
    
    origin = Open_Tile_Pos
    target = AddVectors(Open_Tile_Pos,Direction_Vector)

    origin_id = 15
    target_id = Board_State[target[1]][target[0]]
   
    Board_State[origin[1]][origin[0]] = target_id
    Board_State[target[1]][target[0]] = origin_id


#Updates the location of Open_Tile_Pos in accordance with the movement vector
def UpdateOpenTilePos(Direction_Vector):
    global Open_Tile_Pos
    x_component = Open_Tile_Pos[0] + Direction_Vector[0]
    y_component = Open_Tile_Pos[1] + Direction_Vector[1]

    Open_Tile_Pos = [x_component,y_component]
    

#Calls the appropriate functions to perform any of the four possible moves
def Move(direction):
    Direction_Vector = DefineDirectionVector(direction)
    DisplayMove(Direction_Vector)
    UpdateBoardState(Direction_Vector)
    UpdateOpenTilePos(Direction_Vector)


#Allows the player to control the game board
#If you're reading this, give yourself a high five.
def PlayerControlLoop():

    hover = False
    puzzle_is_solved = False
    moves = 0
    
    while puzzle_is_solved == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if 110 < mouse[0] < 330 and 452 < mouse[1] < 527:
                hover = True
                if click[0] == 1:
                    RobotSolver()
            else:
                hover = False

            
            if Board_State == [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]:
                gameDisplay.fill((0,0,0))

                gameDisplay.blit(Puzzle_Border_IMG,(0,0))
                gameDisplay.blit(Puzzle_IMG,(35,35))
                pygame.display.update()

                print()
                print('Puzzle Complete')
                print(moves, "player moves")

                time.sleep(1)
                return


            if event.type == pygame.KEYDOWN:
                x_pos = Open_Tile_Pos[0]
                y_pos = Open_Tile_Pos[1]
                
                if event.key == pygame.K_LEFT and x_pos != 0:
                    Move('left')
                    moves += 1
                if event.key == pygame.K_RIGHT and x_pos != 3:
                    Move('right')
                    moves += 1
                if event.key == pygame.K_UP and y_pos != 0:
                    Move('up')
                    moves += 1
                if event.key == pygame.K_DOWN and y_pos != 3:
                    Move('down')
                    moves += 1
                if event.key == pygame.K_SPACE:
                    print('Heuristic:',CalculateHeuristicValue(Board_State))
                    print('Moves:',moves)

        if hover == False:
            gameDisplay.blit(Solve_Button_IMG,(110,452))
        else:
            gameDisplay.blit(Solve_Button_Hover_IMG,(110,452))

        pygame.display.update()







#-------------------------------------------------------------------------------
#Algorithm-Dependent Functions

#Updates the position of the empty tile in accordance with a set of moves: Path
def OpenHypotheticalUpdate(Open_Hypothetical,Path):
    for direction in Path:
        vector2 = DefineDirectionVector(direction)
        Open_Hypothetical = AddVectors(Open_Hypothetical,vector2)

    return Open_Hypothetical


#Updates the hypothetical board state in accordance with a set of moves: Path
def HypotheticalBoardUpdate(Hypothetical_Board,Path):
    
    target = Open_Tile_Pos

    for entry in Path:
        
        vector2 = DefineDirectionVector(entry)

        origin = target
        target = AddVectors(origin,vector2)

        origin_id = Hypothetical_Board[origin[1]][origin[0]]
        target_id = Hypothetical_Board[target[1]][target[0]]

        Hypothetical_Board[target[1]][target[0]] = origin_id
        Hypothetical_Board[origin[1]][origin[0]] = target_id

    return Hypothetical_Board


#Calculates the Heuristic Value of a hypothetical board state.
#This Heuristic is known as The Manhattan Distance
#Board_State is the real board state, whereas Path describes the alteration
def CalculateHeuristicValue(Hypothetical_Board):

    Heuristic_Value = 0

    for tile_location in range(0,16):
        tile_number = Hypothetical_Board[int(tile_location/4)][tile_location%4]
        
        intended_x_pos = tile_number%4
        intended_y_pos = int(tile_number/4)

        Heuristic_Value += abs(intended_x_pos - tile_location%4)
        Heuristic_Value += abs(intended_y_pos - int(tile_location/4))
        
    return Heuristic_Value


def RemoveWorstElement(Path_List):
    value_list = []
    
    for Path in Path_List:
        Hypothetical_Board = copy.deepcopy(Board_State)
        Hypothetical_Board = HypotheticalBoardUpdate(Hypothetical_Board,Path)

        score = CalculateHeuristicValue(Hypothetical_Board)
        value_list.append(score)

    maximum = max(value_list)
    
    for entry_no in range(len(value_list)):
        if value_list[entry_no] == maximum:
            index = entry_no
            break

    Path_List.remove(Path_List[index])

    return Path_List


#Determines the shortest path that can solve the puzzle
#That's the hope anyways
#This is the meat of the program
def CalculateBestPath():

    Best_Path = []
    Path_List = []
    maximum_nodes = 70


    if Open_Tile_Pos[0] != 0:
        Path_List.append(['left'])
    if Open_Tile_Pos[0] != 3:
        Path_List.append(['right'])
    if Open_Tile_Pos[1] != 0:
        Path_List.append(['up'])
    if Open_Tile_Pos[1] != 3:
        Path_List.append(['down'])

    solved = False
    
    while solved == False:
        for entry in range(len(Path_List)):
            Open_Hypothetical = copy.deepcopy(Open_Tile_Pos)
            Hypothetical_Board = copy.deepcopy(Board_State)

            Open_Hypothetical = OpenHypotheticalUpdate(Open_Hypothetical,Path_List[entry])
            Hypothetical_Board = HypotheticalBoardUpdate(Hypothetical_Board,Path_List[entry])

            last_move = Path_List[entry][len(Path_List[entry])-1]
            possible_moves = FindPossibleMoves(Open_Hypothetical,last_move)
            possible_moves = [[entry] for entry in possible_moves]


            for possibility in range(len(possible_moves)):
                Path_List.append(Path_List[entry] + possible_moves[possibility])

            Path_List.remove(Path_List[entry])

        value_list = []
        for Path in Path_List:
            Hypothetical_Board = copy.deepcopy(Board_State)
            Hypothetical_Board = HypotheticalBoardUpdate(Hypothetical_Board,Path)
            
            value = CalculateHeuristicValue(Hypothetical_Board)
            value_list.append(value)

            if value <= 0:
                for entry in Path:
                    Best_Path.append(entry)
                print(len(Best_Path),'robot moves')
                    
                solved = True
                break

        if len(Path_List) > maximum_nodes:
            for i in range(len(Path_List)-maximum_nodes):
                Path_List = RemoveWorstElement(Path_List)

    return Best_Path
    

#Executes the series of moves passed into the function.
#'Path' is an array of strings with elements 'left', 'right', 'up', 'down'
def ExecutePath(Path):
    for step in range(len(Path)):
        Move(Path[step])
        time.sleep(0.25)


#Calls the appropriate functions to enable the robot to solve the puzzle
def RobotSolver():
    Path = CalculateBestPath()
    ExecutePath(Path)
    return

    
InitializeBoard()
ShuffleBoard()
PlayerControlLoop()
pygame.quit()
quit()
