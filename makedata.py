#!/usr/bin/env python3

#tesseraction net
#copyright - clayton thomas baber 2019

from tkinter import *
import time
import random

color_state = ["#333333","red","orange","yellow","green","blue","cyan","purple","#ffffff"]

cHeight=600
cellSize=cHeight/28

tk = Tk()
tk.title("tesseraction.net")
tk.aspect(1,1,1,1)
canvas = Canvas(tk, width=cHeight, height=cHeight, bg="#424242")
canvas.pack(fill=BOTH, expand=1)


#all positions are relative to a 32x30 grid on the canvas
#first 0:15 pairs represent board posistions. 15:22 player one starting positions, 22:29 player two.
positions = (14,1),(9,4),(19,4),(14,7),(9,10),(19,10),(4,13),(14,13),(24,13),(9,16),(19,16),(14,19),(9,22),(19,22),(14,25),(4,4),(3,7),(2,10),(1,13),(2,16),(3,19),(4,22),(24,4),(25,7),(26,10),(27,13),(26,16),(25,19),(24,22)

#lines connecting board positions
lines = (0,1),(0,2),(0,4),(0,5),(1,6),(1,7),(1,3),(2,3),(2,7),(2,8),(3,9),(3,10),(4,6),(4,7),(4,11),(5,7),(5,8),(5,11),(6,12),(6,9),(7,9),(7,10),(7,12),(7,13),(8,10),(8,13),(9,14),(10,14),(11,12),(11,13),(12,14),(13,14)

#index here represents a board position, the value represent board positions that are neighbors
neighbors = (1,2,4,5),(0,3,6,7),(0,3,7,8),(1,2,9,10),(0,6,7,11),(0,7,8,11),(1,4,9,12),(1,2,4,5,9,10,12,13),(2,5,10,13),(3,6,7,14),(3,7,8,14),(4,5,12,13),(6,7,11,14),(7,8,11,14),(9,10,12,13)

t_space = [0,0,0,1,4,6,0,2,0,7,5,3,0,0,0]
#this indicates who is occupying a positions
#first 15 elements represent the positions on the board.
#the next 7 are player one starting positions;
#the next 7, player two.
#a value of 0 indicates the position in empty; 1 is player one occupation; -1 is player two occupation
occupations = [(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1,1,1,0),(1,1,1,-1),(1,0,0,1),(1,1,0,0),(1,-1,0,1),(1,1,-1,0),(1,0,0,0),(-1,-1,-1,0),(-1,-1,-1,1),(-1,0,0,-1),(-1,-1,0,0),(-1,1,0,-1),(-1,-1,1,0),(-1,0,0,0)]

#the selected list represents which piece has been selected to be moved... should only have one nonzero value at a time, sometimes none
selected = [0] * 29

#this contains all pertinent drawing locations for board stuff (positions, lines)
#should be recalculated each time the playing surface changes size
pixels = [(0,0,0,0)] * 75

expected_play = 0
turn = 1

def calculate_pixels(event):
    global cHeight, cellSize
    cHeight=min(event.width, event.height)
    cellSize = cHeight / 29

    #positions
    for i in range(29):
        pixels[i] = (positions[i][0]*cellSize+cellSize/4, positions[i][1]*cellSize+cellSize/4, (positions[i][0]+1)*cellSize-cellSize/4, (positions[i][1]+1)*cellSize-cellSize/4)

    #lines
    for i in range(32):
        pixels[i+29] = (positions[lines[i][0]][0]*cellSize+(cellSize/2), positions[lines[i][0]][1]*cellSize+(cellSize/2),positions[lines[i][1]][0]*cellSize+(cellSize/2), positions[lines[i][1]][1]*cellSize+(cellSize/2))

    #misc
    pixels[74] = cellSize/4, cellSize/8, cellSize, cellSize/2

    draw()


#if we decide we dont want to update grafics, set drawing to False
#this shouldn't prevent the game from running, just updating the view
drawing = True


def draw_t_space(posx, posy, transformer):
    if transformer == 0:
        return
    
    number = cellSize/2
    number2 = cellSize/3
    number3 = cellSize/2.5
    number4 = cellSize/12
    number5 = cellSize/4
    
    if transformer == 1:
        canvas.create_arc(posx - number3, posy - number3, posx + number3, posy + number3, start=0, extent=-180, width=number4, style=ARC)
    elif transformer == 2:
        canvas.create_arc(posx - number5, posy, posx + number5 + 3, posy + number5*2, start=90, extent=180, width=number4, style=ARC)
        canvas.create_arc(posx - number5, posy - number5*2, posx + number5, posy, start=90, extent=-180, width=number4, style=ARC)
    elif transformer == 3:
        canvas.create_arc(posx - number3, posy - number3, posx + number3, posy + number3, start=0, extent=180, width=number4, style=ARC)
    elif transformer == 4:
       canvas.create_line(posx, posy - number, posx, posy + number, width=number4)
    elif transformer == 5:
        canvas.create_line(posx - number, posy, posx + number, posy, width=number4)
    elif transformer == 6:
        canvas.create_line(posx - number2, posy + number2, posx + number2, posy - number2, width=number4)
    elif transformer == 7:
        canvas.create_line(posx - number2, posy - number2, posx + number2, posy + number2, width=number4)
    

def draw_st(posx, posy, state):
    color = color_state[4+sum(state)]
    number = cellSize/2
    number2 = number * 1.75
    number3 = number / 4
    number4 = number/6
    canvas.create_rectangle(posx - number, posy - number,posx + number, posy + number,  fill=color, outline="black", width=number4)
    
    #draw the four statelettes
    if state[0] != 0:
        if state[0] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx - number2, posy - number2,posx - number3, posy - number3, fill=color, width=number4)
    if state[1] != 0:
        if state[1] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx + number3, posy - number2,posx + number2, posy - number3, fill=color, width=number4)

    if state[2] != 0:
        if state[2] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx - number2, posy + number2,posx - number3, posy + number3, fill=color, width=number4)

    if state[3] != 0:
        if state[3] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx + number3, posy + number2,posx + number2, posy + number3, fill=color, width=number4)


#this function will draw the current gamestate on the canvas.
def draw():

    if not drawing: return
    
    #wipe the canvas clean
    canvas.delete(ALL)

    color = "#adadad"

   #draw the connecting lines
    for i in pixels[29:61]:
        canvas.create_line(i[0], i[1], i[2], i[3], fill=color, width=pixels[74][0])

    #draw each of the board positions
    for i,p in enumerate(pixels[:15]):
        canvas.create_oval(p[0], p[1], p[2], p[3], outline=color, fill=color, width=pixels[74][2])
        draw_t_space(p[0]+pixels[74][0], p[1]+pixels[74][0], t_space[i])

    #draw a player piece on the position it is occupying
    for i in range(29):
        if occupations[i] != (0,0,0,0):
            draw_st(pixels[i][0]+pixels[74][0], pixels[i][1]+pixels[74][0], occupations[i])
    
    if 1 in selected:
        if turn == 1:
            color = "white"
        else:
            color = "black"
        selected_posisiton = selected.index(1)
        canvas.create_oval(pixels[selected_posisiton][0]-pixels[74][2], pixels[selected_posisiton][1]-pixels[74][2], pixels[selected_posisiton][2]+pixels[74][2], pixels[selected_posisiton][3]+pixels[74][2], outline=color, width=pixels[74][1])
    #update the canvas holder
    tk.update()
    
    #maybe slow down the animation to a visually pleasing speed
    #time.sleep(.1)
################################
#loop through the positions and see if mouse click was on a board position
def click(event):
    for i in range(0, 29):
        if event.x > pixels[i][0]-pixels[74][0] and event.x < pixels[i][2]+pixels[74][0] and event.y > pixels[i][1]-pixels[74][0] and event.y < pixels[i][3]+pixels[74][0]:
            #clicked registered on the i'th position, process it
            clicked(i)
            break

def valid_moves():
    #returns a list of vaild moves based on gamestate
    valid_sofar = [0] * 29

    #set easy lookup for board positions depending on whose turn it is
    a, b, c = 15, 22, 1
    if(turn == -1):
        a, b, c = 22, 29, -1
        
    #if the current player is expected to choose a piece of their own to be moved
    if(expected_play == 0):
        #if the current player has more than zero pieces in their starting posistions (opening)
        if occupations[a:b].count((0,0,0,0)) < 7:
            
            #find where the pieces are            
            for i in range(a,b):
                #and if they are our pieces, add them to to valid moves
                if(occupations[i] != (0,0,0,0)):
                    valid_sofar[i] = 1
        #else the current player may choose any of their own pieces in the playing field,
        else:
            for i in range(0,18):
                if occupations[i] != (0,0,0,0) and sum(occupations[i])*c >=0:
                    valid_sofar[i] = 1
    #if the current player is placing a piece that the have previously selected
    elif(expected_play == 1):
        #if the current player has more than zero pieces in their starting posistions (opening)
        if occupations[a:b].count((0,0,0,0)) < 7:
            #look at all of the playing field positions
            for i in range(0,15):
                #and if it is empty, add it to the list
                if occupations[i] == (0,0,0,0):
                    valid_sofar[i] = 1
        #else you may only move the selected piece to a neighboring spot
        else:
            for i in neighbors[selected.index(1)]:
                valid_sofar[i] = 1
    #return our list of valid moves
    return valid_sofar
##end def valid_moves

def clicked(value):
    global expected_play, turn, selected

    #this is just a helper for humans... allows you to change your mind about which piece you're selecting
    if selected[value] == 1:
        selected[value] = 0
        expected_play = 0
        draw()
        return
    #if you are trying to do something that isn't a valid move, do nothing
    if valid_moves()[value] == 0:
        return
    #from this point on, we can assume any action being taken is a valid move


    #select a piece and switch expected to place
    if expected_play == 0:
        selected[value] = 1
        expected_play = 1
    #place a piece, clear the selection list, check if the piece we just placed created a new mill
    elif expected_play == 1:
        if occupations[value] == (0,0,0,0):
            occupations[selected.index(1)], occupations[value] = (0,0,0,0), transform(occupations[selected.index(1)], t_space[value])
        else:
            occupations[selected.index(1)], occupations[value] = (0,0,0,0), combine(occupations[value], occupations[selected.index(1)])
        selected[:] = [0] * 29
        turn = -turn
        expected_play = 0
       
    #we've made changes to the gamestate, so lets update board view
    draw()
    
     
def combine(s1, s2):
    return (min(1, max(-1, s1[0]+s2[0])),min(1, max(-1, s1[1]+s2[1])),min(1, max(-1, s1[2]+s2[2])),min(1, max(-1, s1[3]+s2[3])))
def transform(s, t):
    if t == 0:
        return s
    elif t == 1:
        return(s[2], s[0], s[3], s[1])
    elif t == 2:
        return(s[3], s[2], s[1], s[0])
    elif t == 3:
        return(s[1], s[3], s[0], s[2])
    elif t == 4:
        return(s[1], s[0], s[3], s[2])
    elif t == 5:
        return(s[2], s[3], s[0], s[1])
    elif t == 6:
        return(s[3], s[1], s[2], s[0])
    elif t == 7:
        return(s[0], s[2], s[1], s[3])

#
#this will set the gamestate back to start
def clear_board():
    global turn, expected_play
    occupations[0:15] = [(0,0,0,0)] * 15
    occupations[15:22] = [(1,1,1,0),(1,1,1,-1),(1,0,0,1),(1,1,0,0),(1,-1,0,1),(1,1,-1,0),(1,0,0,0)]
    occupations[22:] = [(-1,-1,-1,0),(-1,-1,-1,1),(-1,0,0,-1),(-1,-1,0,0),(-1,1,0,-1),(-1,-1,1,0),(-1,0,0,0)]
    selected[:] = [0] * 29
    turn = 1
    expected_play = 0
    draw()

#we need to recalculate the pixels list anytime the window is resized
tk.bind("<Configure>", calculate_pixels)
################################

#initialize board
round = 0

draw()
drawing = False

def play(rounds, save_path):
    f = open(save_path, "w")
    for round in range(rounds):
        print(round, end="\r")
        while(True):
            good_choices = []
            bad_choices = []
            moves = valid_moves()

            #split moves into good and bad
            for i in range(29):
                if moves[i] == 1:
                    good_choices.append(i)
                else:
                    bad_choices.append(i)

            #assemble the old state
            play_type = [0] * 2
            play_type[expected_play] = 1
            whos = []
            whos.append(turn)
            old_state = whos + play_type + [item for t in occupations for item in t] + selected

            #if at least one bad choice exists, select a bad choice at random, convert to bad action, and
            #show that that action results in the same state
            if(len(bad_choices) > 0):
                bad_action = [0] * 29
                bad_action[random.choice(bad_choices)] = 1
                f.write(re.sub("[\[\]]", "", str(old_state + bad_action + old_state) + "\n"))

            #select a good choice at random, convert to good action, apply action to state
            good_choice = random.choice(good_choices)
            good_action = [0] * 29
            good_action[good_choice] = 1
            
            clicked(good_choice)

            #if someone lost, the next state should be a cleared board
            #otherwise record new example of old + good + new

            moves = valid_moves()

            #this flag signals the end of a round (someone lost)
            end_of_round = False

            #make a list of choices from available moves with black magic; 
            choices = [i for i,x in enumerate(moves) if x==1]



            #reset the board and start a new round if no choices
            if valid_moves().count(1) == 0 or occupations.count((0,0,0,0)) >= 28:
                end_of_round = True 
                clear_board()

            #assemble new state
            new_play_type = [0] * 2
            new_play_type[expected_play] = 1
            whos = []
            whos.append(turn)
            new_state = whos + new_play_type + [item for t in occupations for item in t] + selected

            
            f.write(re.sub("[\[\]]", "", str(old_state + good_action + new_state) + "\n"))

            if(end_of_round):
                break
    f.close()
    print("done\n")


random.seed(1)
play(100, "data/trainingdata.csv")
random.seed(2)
play(10, "data/testingdata.csv")

#tk.mainloop()                          
