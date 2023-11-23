from cmu_graphics import *
import math
import random
import copy
from PIL import Image

'''
Sources + Inspiration
https://www.thinkfun.com/wp-content/uploads/2015/09/RushH-5000-IN02.pdf
https://www.michaelfogleman.com/rush/
https://blog.devgenius.io/mastering-the-rush-hour-puzzle-how-bfs-can-help-you-find-the-shortest-solution-f2107eb6f19
'''
 
# creates a copy of the board
def copy_board(board):
    new_board = []
    for row in board:
        new_row = row[:] # copy of the row
        new_board.append(new_row)
    return new_board
 
def generate_board():
    rows, cols = 6, 6
    red_start_row, red_start_col = 2, 1
 
    # creating a empty board
    board = []
    for _ in range(rows):
        board.append([None] * cols)
 
    # setting the red car inside the board
    board[red_start_row][red_start_col] = board[red_start_row][red_start_col + 1] = 'R'
 
    # list of the other cars and its length (Label, Number)
    cars = [('B1', 3), ('T1', 3), ('T2', 3), ('C1', 2), ('C2', 2), ('C3', 2), ('C4', 2)]
        # One bus, Two truck, Four cars
 
    for car in cars:
        # label and size of the car
        car_name, car_len = car
        car_placement = 0
 
        while True:
            # determines whether the car is vertical or not 
            is_vertical = random.randrange(2)
 
            placement_valid = True
            row = random.randrange(rows - ((car_len - 1) * is_vertical))
            col = random.randrange(cols - ((car_len - 1) * (1 - is_vertical)))
 
            # check if the placement is valid
            for j in range(car_len):
                if row == 2 and is_vertical == 0:
                    placement_valid = False
                if board[row + j * is_vertical][col + j * (1 - is_vertical)] != None:
                    placement_valid = False
                    break
 
            if placement_valid:
                for j in range(car_len):
                    if is_vertical == 0:
                        car_name = car_name[0].lower() + car_name[1]
                    board[row + j * is_vertical][col + j * (1 - is_vertical)] = car_name
                break
 
            # if the placement does not work after a set number of trials, continue
            car_placement += 1
            if car_placement > 100:
                break
 
    return board
 
def storage_board(board):
    # creates the board in a string form, in order for the breadth-first search to be performed
    final = []
    for row in board:
        joined_row = []
        for cell in row:
            if cell is not None:
                joined_row.append(cell)
            else:
                joined_row.append(' ')
        final.append(''.join(joined_row))
    return '\n'.join(final)
 
def red_free(board): # determines whether the problem is solved or not
    for i in range(0, 6)[::-1]:
        if board[2][i] == 'R':
            return True
        elif board[2][i] == None:
            continue
        else:
            return False
 
    return True
 
def generate_next_board(board):
    rows, cols = 6, 6
    shifted_vehicles = set([None])
    next_states = []
    for row in range(rows):
        for col in range(cols):
            vehicle = board[row][col]
            if vehicle not in shifted_vehicles:
                vehicle_label = vehicle[0]
                # if vehicle does not exist or has been changed, continues
                if vehicle == None:
                    continue
                shifted_vehicles.add(vehicle)
                row_change = int(vehicle_label.isupper())
                col_change = 1 - row_change
 
                top_end, bottom_end = row, row
                left_end, right_end = col, col
 
                # determines the ends of the car
                if row_change == 1:
                    while top_end - row_change >= 0 and board[top_end - row_change][col] == vehicle:
                        top_end -= row_change
                    while bottom_end + row_change < 6 and board[bottom_end + row_change][col] == vehicle:
                        bottom_end += row_change
                else:
                    while left_end - col_change >= 0 and board[row][left_end - col_change] == vehicle:
                        left_end -= col_change
                    while right_end + col_change < 6 and board[row][right_end + col_change] == vehicle:
                        right_end += col_change
 
                # for the given endpoints, determines whether a shift is valid for the vehicle
                if top_end - row_change >= 0 and left_end - col_change >= 0 and board[top_end - row_change][left_end - col_change] == None:
                    next_state = copy_board(board)
                    next_state[top_end - row_change][left_end - col_change] = vehicle
                    next_state[bottom_end][right_end] = None
                    # adds to next states if valid
                    next_states.append(next_state)
 
                if bottom_end + row_change < 6 and right_end + col_change < 6 and board[bottom_end + row_change][right_end + col_change] == None:
                    next_state = copy_board(board)
                    next_state[bottom_end + row_change][right_end + col_change] = vehicle
                    next_state[top_end][left_end] = None
                    # adds to next states if valid
                    next_states.append(next_state)
 
    return next_states
 
def bfs_boardstate(board):
    # performs a bfs for the possible boards
    queue = [(0, [board])]
    seen_board = set()
 
    while queue:
        steps, path = queue.pop(0)
        # if the current board is in a solvable state, returns the number of steps taken
        if red_free(path[-1]):
            return steps
 
        # goes through all possible states for the next step
        for next_state in generate_next_board(path[-1]):
            if storage_board(next_state) not in seen_board:
                seen_board.add(storage_board(next_state))
                queue.append((steps + 1, path + [next_state]))
 
    return 0
 
def setBoard(app, difficulty):
    # generates the board
    while True:
        temp_board = generate_board()
        temp_difficulty = bfs_boardstate(temp_board)
 
        # regenerates until the board has adequate difficulty
        if difficulty - 3 < temp_difficulty < difficulty + 3:
            print(f'difficulty: {temp_difficulty}')
            break
    return temp_board

def restart(app):
    # parameters for the app
    app.difficulty = 6
    app.board = setBoard(app, app.difficulty)
    app.selections = None
    app.gameover = False
    app.win = False
    app.lose = False
    app.move = 0
    app.totalmove = app.difficulty * 3
    app.startScreen = True
    app.instructions = False
 
def onAppStart(app):
    app.rows = 6
    app.cols = 6
    app.boardLeft = app.width/6
    app.boardTop = app.height/6
    app.boardWidth = app.width/1.5
    app.boardHeight = app.height/1.5
    app.cellBorderWidth = 2
    app.cellWidth = app.boardWidth / app.cols
    app.cellHeight = app.boardHeight / app.rows
    # load the PIL image
    app.image = Image.open('images/starterimage.jpeg')
    # convert each PIL image to a CMUImage for drawing
    app.image = CMUImage(app.image)
    app.car1H = CMUImage(Image.open('images/car1H.png'))
    app.car1V = CMUImage(Image.open('images/car1V.png'))
    app.car2H = CMUImage(Image.open('images/car2H.png'))
    app.car2V = CMUImage(Image.open('images/car2V.png'))
    app.car3H = CMUImage(Image.open('images/car3H.png'))
    app.car3V = CMUImage(Image.open('images/car3V.png'))
    app.car4H = CMUImage(Image.open('images/car4H.png'))
    app.car4V = CMUImage(Image.open('images/car4V.png'))
    app.car5H = CMUImage(Image.open('images/car5H.png'))
    app.car5V = CMUImage(Image.open('images/car5V.png'))
    app.car6H = CMUImage(Image.open('images/car6H.png'))
    app.car6V = CMUImage(Image.open('images/car6V.png'))
    app.car7H = CMUImage(Image.open('images/car7H.png'))
    app.car7V = CMUImage(Image.open('images/car7V.png'))
    app.busH = CMUImage(Image.open('images/busH.png'))
    app.busV = CMUImage(Image.open('images/busV.png'))
    app.truckH = CMUImage(Image.open('images/truckH.png'))
    app.truckV = CMUImage(Image.open('images/truckV.png'))
    app.red = CMUImage(Image.open('images/redcar.png'))
    app.ground = CMUImage(Image.open('images/ground.jpg'))
    restart(app)
 
def cellLeftTop(app,row,col):
    return app.boardLeft + col * app.cellWidth, app.boardTop + row * app.cellHeight
 
def drawCar(app):
    allCars = ['R','T1','t1', 'T2','t2', 'B1','b1', 'C1', 'C2', 'C3','C4','C5','C6','C7',
               'c1','c2','c3','c4','c5','c6','c7']
    carPositions = {}
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col] in allCars:
                allCars.remove(app.board[row][col])
                carPositions[app.board[row][col]] = (row, col)
    # draw red car
    redRow, redCol = carPositions['R'] 
    redLeft, redTop = cellLeftTop(app,redRow,redCol)
    drawImage(app.red, redLeft,redTop, width = 2 * app.cellWidth, height = app.cellHeight)
 
    # draw bus 
    if 'b1' in carPositions:
        busRow, busCol = carPositions['b1']
        busLeft, busTop = cellLeftTop(app,busRow,busCol)
        drawImage(app.busH, busLeft,busTop, width = 3 * app.cellWidth, height = app.cellHeight)
    elif 'B1' in carPositions:
        busRow, busCol = carPositions['B1']
        busLeft, busTop = cellLeftTop(app,busRow,busCol)
        drawImage(app.busV, busLeft,busTop, width = app.cellWidth, height = app.cellHeight*3)
 
    # draw truck
    if 't1' in carPositions:
        truck1Row, truck1Col = carPositions['t1']
        truck1Left, truck1Top = cellLeftTop(app,truck1Row,truck1Col)
        drawImage(app.truckH, truck1Left,truck1Top, width = 3 * app.cellWidth, height = app.cellHeight)
    elif 'T1' in carPositions:
        truck1Row, truck1Col = carPositions['T1']
        truck1Left, truck1Top = cellLeftTop(app,truck1Row,truck1Col)
        drawImage(app.truckV, truck1Left,truck1Top, width = app.cellWidth, height = app.cellHeight*3)
 
    if 't2' in carPositions:
        truck2Row, truck2Col = carPositions['t2']
        truck2Left, truck2Top = cellLeftTop(app,truck2Row,truck2Col)
        drawImage(app.truckH, truck2Left,truck2Top, width = 3 * app.cellWidth, height = app.cellHeight)
    elif 'T2' in carPositions:
        truck2Row, truck2Col = carPositions['T2']
        truck2Left, truck2Top = cellLeftTop(app,truck2Row,truck2Col)
        drawImage(app.truckV, truck2Left,truck2Top, width = app.cellWidth, height = app.cellHeight*3)
 
    # draw cars
    if 'c1' in carPositions:
        car1Row, car1Col = carPositions['c1']
        car1Left, car1Top = cellLeftTop(app,car1Row,car1Col)
        drawImage(app.car1H, car1Left,car1Top, width = 2 * app.cellWidth, height = app.cellHeight)
    elif 'C1' in carPositions:
        car1Row, car1Col = carPositions['C1']
        car1Left, car1Top = cellLeftTop(app,car1Row,car1Col)
        drawImage(app.car1V, car1Left,car1Top, width = app.cellWidth, height = app.cellHeight*2)
 
    if 'c2' in carPositions:
        car2Row, car2Col = carPositions['c2']
        car2Left, car2Top = cellLeftTop(app,car2Row,car2Col)
        drawImage(app.car2H, car2Left,car2Top, width = 2 * app.cellWidth, height = app.cellHeight)
    elif 'C2' in carPositions:
        car2Row, car2Col = carPositions['C2']
        car2Left, car2Top = cellLeftTop(app,car2Row,car2Col)
        drawImage(app.car2V, car2Left,car2Top, width = app.cellWidth, height = app.cellHeight*2)
 
    if 'c3' in carPositions:
        car3Row, car3Col = carPositions['c3']
        car3Left, car3Top = cellLeftTop(app,car3Row,car3Col)
        drawImage(app.car3H, car3Left,car3Top, width = 2 * app.cellWidth, height = app.cellHeight)
    elif 'C3' in carPositions:
        car3Row, car3Col = carPositions['C3']
        car3Left, car3Top = cellLeftTop(app,car3Row,car3Col)
        drawImage(app.car3V, car3Left,car3Top, width = app.cellWidth, height = app.cellHeight*2)
 
    if 'c4' in carPositions:
        car4Row, car4Col = carPositions['c4']
        car4Left, car4Top = cellLeftTop(app,car4Row,car4Col)
        drawImage(app.car4H, car4Left,car4Top, width = 2 * app.cellWidth, height = app.cellHeight)
    elif 'C4' in carPositions:
        car4Row, car4Col = carPositions['C4']
        car4Left, car4Top = cellLeftTop(app,car4Row,car4Col)
        drawImage(app.car4V, car4Left,car4Top, width = app.cellWidth, height = app.cellHeight*2)
 
    if 'c5' in carPositions:
        car5Row, car5Col = carPositions['c5']
        car5Left, car5Top = cellLeftTop(app,car5Row,car5Col)
        drawImage(app.car5H, car5Left,car5Top, width = 2 * app.cellWidth, height = app.cellHeight)
    elif 'C5' in carPositions:
        car5Row, car5Col = carPositions['C5']
        car5Left, car5Top = cellLeftTop(app,car5Row,car5Col)
        drawImage(app.car5V, car5Left,car5Top, width = app.cellWidth, height = app.cellHeight*2)
 
    if 'c6' in carPositions:
        car6Row, car6Col = carPositions['c6']
        car6Left, car6Top = cellLeftTop(app,car6Row,car6Col)
        drawImage(app.car6H, car6Left,car6Top, width = 2 * app.cellWidth, height = app.cellHeight)
    elif 'C6' in carPositions:
        car6Row, car6Col = carPositions['C6']
        car6Left, car6Top = cellLeftTop(app,car6Row,car6Col)
        drawImage(app.car6V, car6Left,car6Top, width = app.cellWidth, height = app.cellHeight*2)
 
    if 'c7' in carPositions:
        car7Row, car7Col = carPositions['c7']
        car7Left, car7Top = cellLeftTop(app,car7Row,car7Col)
        drawImage(app.car7H, car7Left,car7Top, width = 2 * app.cellWidth, height = app.cellHeight)
    elif 'C7' in carPositions:
        car7Row, car7Col = carPositions['C7']
        car7Left, car7Top = cellLeftTop(app,car7Row,car7Col)
        drawImage(app.car7V, car7Left,car7Top, width = app.cellWidth, height = app.cellHeight*2)

def allSelectedCells(app,selectedCell):
    # returns the list that has the same cell content
    answer = [selectedCell] 
    row, col = selectedCell
    cellcontent = app.board[row][col]
    length = 0
    # determines if the car is vertical
    isVertical = cellcontent[0].isupper()
 
    if cellcontent == 'R':
        length = 2
        isVertical = False

    if cellcontent != None:
        if cellcontent[0].upper() == 'T' or cellcontent[0].upper() == 'B':
            length = 3
        else:
            length = 2

    if isVertical:
        for drow in range(-1*length+1,length):
            if drow == 0:
                continue
            if 0 <= row+drow < app.rows:
 
                if app.board[row + drow][col] == cellcontent:
                    answer.append((row + drow, col))
    else:
        for dcol in range(-1 * length + 1,length):
            if dcol == 0:
                continue
            if 0 <= col+dcol < app.cols:
                if app.board[row][col + dcol] == cellcontent:
                    answer.append((row, col + dcol))

    return answer
 
def onMousePress(app, mouseX, mouseY):
 
    cx, cy = app.width*15/16, app.height*15/16
    distance = ((mouseX - cx) ** 2 + (mouseY - cy) ** 2) ** 0.5
 
    if distance <= 20:
 
        app.instructions = not app.instructions
 
 
    selectedCell = getCell(app, mouseX, mouseY) # selectedCell = (row,col)
 
    if selectedCell != None:
        row,col = selectedCell
        if app.board[row][col]!= None:
            if app.selections != None and selectedCell in app.selections:
                app.selections = None
            else:
                app.selections = allSelectedCells(app,selectedCell)

    buttonPressed(app,mouseX,mouseY)
 
def onKeyPress(app,key):
    # restart if r pressed
    if app.gameover:
        if key == 'r':
            restart(app)
        return
    # if instructions pressed, shows instructions
    if app.instructions:
        if key == 'escape':
            app.instructions = False
    if app.selections != None:
        row, col = app.selections[0]
        isVertical = app.board[row][col].isupper()
        if app.board[row][col] == 'R':
            isVertical = False
 
        if key == 'left' and not isVertical: moveCar(app,0,-1)
        if key == 'right'and not isVertical: moveCar(app,0,1)
        if key == 'up' and isVertical: moveCar(app,-1,0)
        if key == 'down'and isVertical: moveCar(app,1,0)
 
def moveCar(app, drow, dcol):
    # moves the car depending on each key move
    app.selections.sort()
    row, col = app.selections[0]
    isVertical = app.board[row][col].isupper()
    if app.board[row][col] == 'R':
        isVertical = False
 
    check = False
    if drow == -1 or dcol == -1:
        selectedCarX,selectedCarY = app.selections[0]
        check = True
    else:
        selectedCarX,selectedCarY = app.selections[-1]
    
    selectedCarX += drow
    selectedCarY += dcol
    if 0 <= selectedCarX < app.rows and 0 <= selectedCarY < app.cols:
        if app.board[selectedCarX][selectedCarY] == None and not app.gameover:
            if app.totalmove - app.move > 0:
                app.move+=1
            if not check:
                for i in range(len(app.selections)-1,-1,-1):
                    row,col = app.selections[i]
                    app.selections[i] = (row + drow, col + dcol)
                    app.board[row + drow][col + dcol],app.board[row][col] = app.board[row][col],app.board[row + drow][col + dcol]
 
            else:
                for i in range(len(app.selections)):
                    row,col = app.selections[i]
                    app.selections[i] = (row + drow, col + dcol)
                    app.board[row + drow][col + dcol],app.board[row][col] = app.board[row][col],app.board[row + drow][col + dcol]
 
    if (app.totalmove - app.move) == 0:
        app.gameover = True
        app.lose = True
    elif isSolved(app):
        app.gameover = True
        app.win = True
 
def redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='grey')
    drawRect(700,355, 45,90,align = 'center',fill = 'red', border = 'white')
    drawLabel('Exit',700,355,fill='white',font='monospace',size=20,rotateAngle=90,bold=True)
 
    drawImage(app.ground,app.boardLeft,app.boardTop,width = app.boardWidth,height = app.boardHeight)
    drawBoard(app)
    drawBoardBorder(app)
    drawCar(app)
    if not app.gameover:
        drawLabel(f'Moves Left: {app.totalmove - app.move}', app.width/2, app.height*9/10, size=30, bold=True, font='monospace')
 
    drawRect(app.width/2, app.height/12, app.width/2+30, 50, align='center', opacity=70, fill='white')
    drawLabel('AVOID THE RUSH', app.width/2, app.height/12, font='monospace', align='center', size=50, bold=True, fill='maroon')
 
    if app.startScreen:
        drawRect(0,0,app.width,app.height)
        # image
        pilImage = app.image.image
        drawImage(app.image, app.width/2, app.height/2.65, align='center', width=pilImage.width,
                height=pilImage.height)
 
        # heading
        drawRect(app.width/2, app.height/15, app.width/2 + 30, 50, align='center', opacity=70, fill='white')
        drawLabel('AVOID THE RUSH', app.width/2, app.height/15, font='monospace', align='center', size=50, bold=True, fill='maroon')
        # instructions
        instructions1 = 'HELP!! Pat and Mike are stuck in the traffic!!'
        instructions2 = 'Move other cars out of the way for the Red Car to exit the board.'
        instructions3 = '15-112 students are crying...'
        drawLabel(instructions1, app.width/2, app.height/1.47, fill='white', bold=True, size = 18, font='monospace')
        drawLabel(instructions2, app.width/2, app.height/1.47 + 40, fill='white', bold=True, size = 18, font='monospace')
        drawLabel(instructions3, app.width/2,  app.height/1.47 + 80, fill='white', bold=True, size = 18, font='monospace')
 
        # buttons
        drawRect(app.width/4, app.height*7/8, 100, 50, fill='springGreen',align = 'center')
        drawLabel('Easy', app.width/4, app.height*7/8, bold=True,size=18, font='monospace')
        drawRect(app.width/2, app.height*7/8, 100, 50, fill='yellow',align = 'center')
        drawLabel('Medium', app.width/2, app.height*7/8, bold=True,size=18, font='monospace')
        drawRect(app.width*3/4, app.height*7/8, 100, 50, fill='crimson',align = 'center')
        drawLabel('Hard', app.width*3/4, app.height*7/8, bold=True,size=18, font='monospace')
        drawCircle(app.width*15/16, app.height*15/16,20,fill = "white")
        drawLabel('?', app.width*15/16, app.height*15/16, bold=True,size=22, font='monospace')
        if app.instructions:
            drawRect(app.width/2, app.height/2, app.width/2, app.height/2, align='center', fill = 'white')
            drawLabel('Instructions',app.width/2,app.height/3 - 20, size = 25, fill = 'grey',  font='monospace',bold = True)
            info0 = 'Heyyyyy'
            info1 = "Welcome to Avoid The Rush!!" 
            info2 = 'Click the cars to select' 
            info3 = 'and use arrow keys to move.'
            info4 = "If you move, sis,"
            info5 = "I'm sorry but you're DONE."
            info6 = 'Complete within the given moves!'
            info7 = 'Good luck girly ;)'
            info8 = 'Press escape to turn me off.'
            drawLabel(info0,app.width/2,app.height/3 + 10 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info1,app.width/2,app.height/3 + 40 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info2,app.width/2,app.height/3 + 70 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info3,app.width/2,app.height/3 + 100 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info4,app.width/2,app.height/3 + 130 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info5,app.width/2,app.height/3 + 160 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info6,app.width/2,app.height/3 + 190 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info7,app.width/2,app.height/3 + 220 , size = 19, fill = 'black',  font='monospace')
            drawLabel(info8,app.width/2,app.height/3 + 250 , size = 19, fill = 'black',  font='monospace')
 
    # checks game over status, app.lose meaning lose, app.win meaning win
    if app.gameover == True and app.lose == True:
        drawRect(0, 0, app.width, app.height, fill='red', opacity=30)
        drawRect(app.width/2,app.height/2, 280, 50, fill='white', opacity=50, align='center')
        drawLabel("YOU LOST!", app.width/2, app.height/2, size=50, bold=True)
        drawLabel("Press r to restart!",app.width/2,app.height*14.5/16,size = 30, font='monospace')
    elif app.gameover == True and app.win == True:
        drawRect(0, 0, app.width, app.height, fill='green', opacity=30)
        drawRect(app.width/2,app.height/2, 280, 50, fill='white', opacity=50, align='center')
        drawLabel("YOU WIN!", app.width/2, app.height/2, size=50, bold=True, font='monospace')
        drawLabel("Press r to restart!",app.width/2,app.height*14.5/16,size = 30, font='monospace')
 
def buttonPressed(app, mouseX, mouseY):
    yTop = app.height*7/8 - 25
    yBot = app.height*7/8 + 25
    if mouseY >= yTop and mouseY <= yBot:
        if app.width/4 - 50 <= mouseX <= app.width/4 + 50: 
            app.difficulty = 6
            app.board = setBoard(app, app.difficulty)
            app.totalmove = app.difficulty * 2
            app.startScreen = False
            return True
        elif app.width/2 - 50 <= mouseX <= app.width/2 + 50:
            app.difficulty = 12
            app.board = setBoard(app, app.difficulty)
            app.totalmove = app.difficulty * 2
            app.startScreen = False 
            return True
        elif app.width*3/4 - 50 <= mouseX <= app.width*3/4 + 50:

            app.difficulty = 15
            app.board = setBoard(app, app.difficulty)
            app.totalmove = app.difficulty * 2
            app.startScreen = False 
            return True
    return False
 
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
 
def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='white',
           borderWidth=2*app.cellBorderWidth)
 
def drawCell(app, row, col):
    cellLeft, cellTop = app.boardLeft + col * app.cellWidth, app.boardTop + row * app.cellHeight
    color = None
    if app.selections != None:
        if (row, col) in app.selections:
            color = 'cyan'
    drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
             fill=color, border='white',
             borderWidth=app.cellBorderWidth)
 
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    row = math.floor(dy / app.cellHeight)
    col = math.floor(dx / app.cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None
 
def isSolved(app):
    if app.board[2][4] == 'R' and app.board[2][5] == 'R':
        return True
    return False
 
def main():
    runApp(800,800)
 
main()