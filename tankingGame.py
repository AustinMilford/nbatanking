#import stuff up here
import random
from tkinter import *


#button objects
class Button(object):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.r = 25
        self.fill = "cyan"

    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return (d <= self.r)

    def draw(self, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r,
                           self.x+self.r, self.y+self.r,
                           fill=self.fill)
        canvas.create_text(self.x, self.y, text=str(self.name))

#player object
class Player(object):
    def __init__(self, pickNumber, pickRating):
        self.pickNumber = pickNumber
        self.pickRating = pickRating
        self.status = panOut(pickRating, pickNumber)

#some useful development functions
def becomeAllStar(pickRating, pickNumber):
    #does this player become an all-star?
    if(pickNumber <= 2):
        return (pickRating >= 84)
    elif(pickNumber <= 5):
        return (pickRating >= 90)
    elif(pickNumber <= 14):
        return (pickRating >= 96)
    else:
        return (pickRating >= 99)
    #return False

def becomeStar(pickRating, pickNumber):
    #does this player become a star?
    if(pickNumber <= 3):
        return (pickRating >= 68)
    elif(pickNumber <= 5):
        return (pickRating >= 75)
    elif(pickNumber <= 14):
        return (pickRating >= 86)
    else:
        return (pickRating >= 98)
    #return False

def becomeRolePlayer(pickRating, pickNumber):
    #does this player become a role player?
    if(pickNumber <= 3):
        return (pickRating >= 35)
    elif(pickNumber <= 6):
        return (pickRating >= 50)
    elif(pickNumber <= 14):
        return (pickRating >= 60)
    elif(pickNumber <= 30):
        return (pickRating >= 70)
    else:
        return (pickRating >= 90)
    #return False

def becomeBust(pickRating, pickNumber):
    #does this player become a bust?
    if(pickNumber <= 5):
        return (pickRating <= 20)
    elif(pickNumber <= 14):
        return (pickRating <= 35)
    elif(pickNumber <= 30):
        return (pickRating <= 50)
    else:
        return (pickRating <= 65)
    #return False

def panOut(pickRating, pickNumber):
    #does this prospect pan out?
    prospect = ""
    if(becomeAllStar(pickRating, pickNumber)):
        prospect = "all-star"
    elif(becomeStar(pickRating, pickNumber)):
        prospect = "star"
    elif(becomeRolePlayer(pickRating, pickNumber)):
        prospect = "role player"
    elif(becomeBust(pickRating, pickNumber)):
        prospect = "bust"
    else:
        prospect = "scrub"
    print("You got a " + prospect + " with the no " + str(pickNumber) + " pick")
    return prospect

def init(data):
    data.team = [ ]
    data.picks = [ ]
    #genPicks(data, 1, 0, 2)
    data.buttons = [ ]
    data.GMscore = 85
    data.draftCol = data.width/2
    genButtons(data)
    data.scoreTime = False
    data.win = False
    data.gameover = False

def genButtons(data):
    data.buttons.append(Button(data.draftCol, data.width/4, "draft"))
    data.buttons.append(Button(data.width/5, data.width/4, "new year"))

def genPicks(data, lotteryNo, firstRoundNo, secondRoundNo):
    #generates a list of draft picks
    #let the ping pong balls bounce!
    while(lotteryNo > 0):
        data.picks.append(random.randint(1,14))
        lotteryNo = lotteryNo - 1

    normalPickNo = random.randint(0,30)
    firstPick = (normalPickNo%15) + 15
    secondPick = normalPickNo + 30
    #get the rest of the 1st round picks
    while(firstRoundNo > 0):
        data.picks.append(firstPick)
        firstPick = ((firstPick + 2)%15) + 15
        firstRoundNo = firstRoundNo - 1
    #do the second round picks
    while(secondRoundNo):
        data.picks.append(secondPick)
        secondPick = ((secondPick + 2)%30) + 30
        secondRoundNo = secondRoundNo - 1

def lotteryPick(data, pickNumber):
    #let's create a player!
    potential = random.randint(0,99)
    data.team.append(Player(pickNumber, potential))

def stayEmployed(data, defaultScore):
    #do you stay on as GM?
    newScore = defaultScore
    starCount = 0
    for player in data.team:
        if(player.status == "star" or player.status == "all-star"):
            starCount = starCount + 1
        if((player.pickNumber == 1) and (player.status == "bust")):
            newScore = newScore - 40
        if(player.pickNumber <= 3):
            if(player.status == "role player"): #later make this factor in tenure
                newScore = newScore - 5
        elif(player.pickNumber < 6):
            if(player.status == "bust"):
                newScore = newScore - 15
            elif(player.status == "star"):
                newScore = newScore + 2 
            elif(player.status == "all-star"):
                newScore = newScore + 4
            elif(player.status == "role player"):
                newScore = newScore + 0
            elif(player.status == "scrub"):
                newScore = newScore - 15
        elif(player.pickNumber < 15):
            if(player.status == "bust"):
                newScore = newScore - 10
            elif(player.status == "star"):
                newScore = newScore + 3 
            elif(player.status == "all-star"):
                newScore = newScore + 5
            elif(player.status == "role player"):
                newScore = newScore + 1
            elif(player.status == "scrub"):
                newScore = newScore - 3
        elif(player.pickNumber <= 30):
            if(player.status == "bust"):
                newScore = newScore - 4
            elif(player.status == "star"):
                newScore = newScore + 4 
            elif(player.status == "all-star"):
                newScore = newScore + 6
            elif(player.status == "role player"):
                newScore = newScore + 2
            elif(player.status == "scrub"):
                newScore = newScore - 2
        elif(player.pickNumber > 30):
            if(player.status == "bust"):
                newScore = newScore - 1
            elif(player.status == "star"):
                newScore = newScore + 6 
            elif(player.status == "all-star"):
                newScore = newScore + 8
            elif(player.status == "role player"):
                newScore = newScore + 3
            elif(player.status == "scrub"):
                newScore = newScore

    data.GMscore = newScore
    if(starCount > 2):
        print("Congrats! You won!")
        data.win = True

def mousePressed(event, data):
    #do mouse stuff
    #if(data.gameover == False):
    for butt in data.buttons:
        if(butt.containsPoint(event.x, event.y)):
            if((butt.name == "draft") and (len(data.picks) > 0)):
                lotteryPick(data, data.picks.pop(0))
            if(butt.name == "new year"):
                genPicks(data, 1, 0, 1)

def redrawAll(canvas, data):
    for butt in data.buttons:
        butt.draw(canvas)
    canvas.create_text(data.draftCol, data.width/9, text="picks left: " + str(len(data.picks)))
    canvas.create_text((data.width/4)*3, data.width/4, text="GM Score: " + str(data.GMscore))
    if(data.gameover):
        canvas.create_text(data.width/2, (data.height/4)*3, text="GAME OVER")

def keyPressed(event, data):
    pass

def timerFired(data):
    if(len(data.picks) > 0):
        data.scoreTime = True
    if(len(data.picks) == 0 and data.scoreTime == True):
        stayEmployed(data, 85)
        data.scoreTime = False
    if(data.GMscore < 70):
        data.gameover = True

##################

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)