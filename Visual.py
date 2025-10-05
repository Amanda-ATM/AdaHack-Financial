import sqlite3 as sql
import pygame as pg
import tkinter as tk
import re


class Cat(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("Images/Cat/Black cat/blacksit.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def changeCat(self,filePath):
        self.image = pg.image.load(filePath).convert_alpha()

class TowerPiece(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def changePiece(self,filePath):
        self.image = pg.image.load(filePath).convert_alpha()


def OpeningScreen():
    width = 400
    height = 300
    intro = pg.display.set_mode((width, height))
    pg.display.set_caption("Welcome to FinCat")


    while True:
        pg.display.flip()


def finCat():
    width = 720
    height = 720
    playing = pg.display.set_mode((width, height))
    pg.display.set_caption("FinCat")
    bg_colour = (0,220,0)
    playing.fill(bg_colour)
    all_sprites = pg.sprite.Group()
    cat = Cat(50, 100)
    all_sprites.add(cat)

    pg.init()

    hunger,happy,clean = checkStatus()

    if hunger >= 75:
        cat.changeCat("Images/Cat/Black cat/blackfat.png")
        state = "fat"
    elif hunger <=25:
        cat.changeCat("Images/Cat/Black cat/blackskinny.png")
        state = "skinny"

    if clean <= 30:
        cat.changeCat("Images/Cat/Black cat/blackstinky.png")
        state = "stinky"
    elif clean <= 45 and hunger <=40:
        cat.changeCat("Images/Cat/Black cat/blacksick.png")
        state = "sick"

    if happy <=45:
        cat.changeCat("Images/Cat/Black cat/blacksad.png")
        state = "sad"
    elif happy <=25:
        cat.changeCat("Images/Cat/Black cat/blackangry.png")
        state = "angry"
    elif happy >=90 and (hunger > 25 and hunger < 75) and clean > 31:
        cat.changeCat("Images/Cat/Black cat/blackspoiled.png")
        state = "spoiled"
    elif happy >=70 and (hunger > 25 and hunger < 75) and clean > 31:
        cat.changecat("Images/Cat/Black cat/blackloaf.png")
        state="happy"

    if happy > 45 and (hunger > 25 and hunger < 75) and clean >31:
        state="neutral"

    #Text
    font = pg.font.SysFont('freesansbold.ttf', 48)
    match state:
        case "spoiled":
            statusTx = font.render('Your cat is spoiled. Well done!', True,'black')
        case "happy":
            statusTx = font.render('Your cat is happy. Good job.', True,'black')
        case "stinky":
            statusTx = font.render('Your cat is stinky! Buy litter', True,'black')
        case "sick":
            statusTx = font.render('Your cat is sick! Buy food and litter', True,'black')
        case "angry":
            statusTx = font.render('Your cat is angry. Your cat needs toys now', True,'black')
        case "sad":
            statusTx = font.render('No toys made your cat cry. Buy toys', True,'black')
        case "skinny":
            statusTx = font.render('Your cat is starving! Feed it!', True,'black')
        case "fat":
            statusTx = font.render('Your cat is obese, please feed him less', True,'black')
        case "neutral":
            statusTx = font.render('Your cat is doing well. Keep it up!', True,'black')

    statusRect = statusTx.get_rect()
    statusRect.center = (275,180)

    # shopping button
    smallfont = pg.font.SysFont('Corbel',35)
    quit = smallfont.render('quit' , True , 'white')
    invest = smallfont.render('cat tower' , True , 'white')
    shop = smallfont.render('shop' , True , 'white')

    while True:
        color_light = (170,170,170)
        color_dark = (100,100,100)
        all_sprites.draw(playing)
        playing.blit(statusTx, statusRect)
        pg.display.flip()
        for ev in pg.event.get():

            if ev.type == pg.QUIT:
                pg.quit()

            #checks if a mouse is clicked
            if ev.type == pg.MOUSEBUTTONDOWN:

                #if the mouse is clicked on the
                # button the game is terminated
                if width-200 <= mouse[0] <= width-60 and height-300 <= mouse[1] <= height-260:
                    pg.quit()
                if width-200 <= mouse[0] <= width-60 and height-350 <= mouse[1] <= height-310:
                    pg.quit()
                    investTower()
                if width-200 <= mouse[0] <= width-60 and height-400 <= mouse[1] <= height-360:
                    pg.quit()
                    shop()


        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pg.mouse.get_pos()

        # if mouse is hovered on a button it
           # changes to lighter shade
        if width-200 <= mouse[0] <= width-60 and height-300 <= mouse[1] <= height-260:
            pg.draw.rect(playing,color_light,[width-200,height-300,140,40])
        else:
           pg.draw.rect(playing,color_dark,[width-200,height-300,140,40])

        if width-200 <= mouse[0] <= width-60 and height-350 <= mouse[1] <= height-310:
            pg.draw.rect(playing,color_light,[width-200,height-350,140,40])
        else:
            pg.draw.rect(playing,color_dark,[width-200,height-350,140,40])

        if width-200 <= mouse[0] <= width-60 and height-400 <= mouse[1] <= height-360:
            pg.draw.rect(playing,color_light,[width-200,height-400,140,40])
        else:
            pg.draw.rect(playing,color_dark,[width-200,height-400,140,40])

        # superimposing the text onto our button
        playing.blit(quit ,(width-160,height-300))
        playing.blit(invest ,(width-195,height-350))
        playing.blit(shop ,(width-160,height-400))

        # updates the frames of the game
        pg.display.update()

def investTower():
    width = 720
    height = 720
    tower = pg.display.set_mode((width, height))
    pg.display.set_caption("FinCat's Tower")
    bg_colour = (0,50,200)
    tower.fill(bg_colour)
    all_sprites = pg.sprite.Group()
    pg.init()

    con = sql.connect('catStats.db')
    cursor = con.cursor()

    cursor.execute("UPDATE Tower SET Acquired = TRUE WHERE Parts = 'Base' or Parts = 'Leg One';")
    con.commit()

    cursor.execute("SELECT Parts FROM Tower WHERE Acquired = TRUE")
    towerPiecesAll = cursor.fetchall()

    towers = [row[0] for row in towerPiecesAll]
    result = ",".join(towers)
    pieces = result.split(",")
    towerPiecesArray = []
    for i in range(len(result.split(","))):
        towerPiecesArray.append(pieces[i])
        towerPiecesArray[i] = re.sub(r'[^a-zA-Z0-9]', '', towerPiecesArray[i])

    for i in range(len(towerPiecesArray)):
        if towerPiecesArray[i] == "Base":
            base = TowerPiece.changePiece("Images/Base.png")
        elif towerPiecesArray[i] == "LegOne":
            leg1 = TowerPiece.changePiece("Images/Leg One.png")
        elif towerPiecesArray[i] == "LegTwo":
            leg2 = TowerPiece.changePiece("Images/Leg Two.png")
        elif towerPiecesArray[i] == "LegThree":
            leg3 = TowerPiece.changePiece("Images/Leg Three.png")
        elif towerPiecesArray[i] == "Box":
            box = TowerPiece.changePiece("Images/Box.png")
        elif towerPiecesArray[i] == "Hammock":
            hammock = TowerPiece.changePiece("Images/Hammock.png")
        elif towerPiecesArray[i] == "Top":
            top = TowerPiece.changePiece("Images/Top.png")
        elif towerPiecesArray[i] == "Toy":
            toy = TowerPiece.changePiece("Images/Toy.png")

    font = pg.font.SysFont('freesansbold.ttf',35)
    quit = font.render('quit' , True , 'white')
    cat = font.render('cat',True,'white')
    shop = font.render('shop' , True , 'white')

    while True:
        color_light = (170,170,170)
        color_dark = (100,100,100)
        pg.display.flip()
        for ev in pg.event.get():

            if ev.type == pg.QUIT:
                pg.quit()

            #checks if a mouse is clicked
            if ev.type == pg.MOUSEBUTTONDOWN:

                #if the mouse is clicked on the
                # button the game is terminated
                if width-200 <= mouse[0] <= width-60 and height-300 <= mouse[1] <= height-260:
                    pg.quit()
                if width-200 <= mouse[0] <= width-60 and height-350 <= mouse[1] <= height-310:
                    pg.quit()
                    finCat()
                if width-200 <= mouse[0] <= width-60 and height-400 <= mouse[1] <= height-360:
                    pg.quit()
                    shop()

        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pg.mouse.get_pos()

        if width-200 <= mouse[0] <= width-60 and height-300 <= mouse[1] <= height-260:
            pg.draw.rect(tower,color_light,[width-200,height-300,140,40])
        else:
            pg.draw.rect(tower,color_dark,[width-200,height-300,140,40])
        if width-200 <= mouse[0] <= width-60 and height-350 <= mouse[1] <= height-310:
            pg.draw.rect(tower,color_light,[width-200,height-350,140,40])
        else:
            pg.draw.rect(tower,color_dark,[width-200,height-350,140,40])

        if width-200 <= mouse[0] <= width-60 and height-400 <= mouse[1] <= height-360:
            pg.draw.rect(tower,color_light,[width-200,height-400,140,40])
        else:
            pg.draw.rect(tower,color_dark,[width-200,height-400,140,40])

            # superimposing the text onto our button
        tower.blit(quit ,(width-160,height-300))
        tower.blit(cat ,(width-160,height-350))
        tower.blit(shop ,(width-160,height-400))


def createdb():
    con = sql.connect('catStats.db')
    cursor = con.cursor()

    # Drop the table if it already exists

    # SQL query to create the table
    tableCreate = """
        CREATE TABLE CatStats(
            Hunger INT NOT NULL,
            Happiness INT NOT NULL,
            Clean INT NOT NULL
        );
    """

    towerCreate = """
        CREATE TABLE Tower(
            Parts VARCHAR(255) NOT NULL,
            Acquired BOOLEAN NOT NULL
            );
        """

     #Execute the table creation query and add stats
    cursor.execute(tableCreate)
    cursor.execute(towerCreate)
    cursor.execute("INSERT INTO CatStats VALUES (50,50,50)")
    cursor.execute("INSERT INTO Tower VALUES ('Base',FALSE)")
    cursor.execute("INSERT INTO Tower VALUES ('Leg One',FALSE)")
    cursor.execute("INSERT INTO Tower VALUES ('Leg Two',FALSE)")
    cursor.execute("INSERT INTO Tower VALUES ('Leg Three',FALSE)")
    cursor.execute("INSERT INTO Tower VALUES ('Box',FALSE)")
    cursor.execute("INSERT INTO Tower VALUES ('Hammock',FALSE)")
    cursor.execute("INSERT INTO Tower VALUES ('Top',FALSE)")
    cursor.execute("INSERT INTO Tower VALUES ('Toy',FALSE)")

    cursor.execute("SELECT * FROM Tower")
    results = cursor.fetchall()
    print(results)

    con.commit()

def editDB(value,stat):
    con = sql.connect('catStats.db')
    cursor = con.cursor()

    if stat == "hunger":
        updateQuery = ("UPDATE CatStats WHERE Hunger = Hunger + ?",value)
    elif stat == "happiness":
        updateQuery = ("UPDATE CatStats WHERE Happiness = Happines + ?",value)
    else:
        updateQuery = ("UPDATE CatStats WHERE Clean = Clean + ?",value)

    cursor.execute(updateQuery)
    con.commit()

def checkStatus():
    con = sql.connect('catStats.db')
    cursor = con.cursor()

    checkHunger = ("SELECT Hunger FROM CatStats")
    checkHappiness = ("SELECT Happiness FROM CatStats")
    checkClean = ("SELECT Clean FROM CatStats")

    hungerLevel = cursor.execute(checkHunger).fetchone()
    hungerLevel = int(hungerLevel[1-2])

    happyLevel = cursor.execute(checkHappiness).fetchone()
    happyLevel = int(happyLevel[1-2])

    cleanLevel = cursor.execute(checkClean).fetchone()
    cleanLevel = int(cleanLevel[1-2])

    return hungerLevel,happyLevel,cleanLevel

finCat()