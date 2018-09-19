import Tkinter as tk
import BasketballStatistics as bs
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import time

def nameRun():
    chosenName = name.get().lower()

    menu = seasonDropdown['menu']
    menu.delete(0, 'end')

    seasonList = bs.getSeasonList(chosenName)

    if(seasonList == False):
        nameLabel.config(text = chosenName + " is not a valid NBA player- please try again", fg = "red")
        return

    nameLabel.config(text = "Enter full name of player here:", fg = "black")

    for possibleSeason in seasonList:
        menu.add_command(label=possibleSeason, command=lambda value= possibleSeason: season.set(value))

def run():
    global first
    global bars

    chosenSeason = season.get()
    chosenStatistic = statistic.get()
    chosenName = name.get().lower()
    statList = []

    if(chosenName == ''):
        nameLabel.config(text = "Please enter a valid NBA player name", fg = "red")
        return False
    else:
        nameLabel.config(text = "Enter full name of player here:", fg = "black")

    if(chosenSeason == ''):
        seasonLabel.config(text = "Please choose a valid season", fg = "red")
        return False
    else:
        seasonLabel.config(text = "Choose season or player, or total career:", fg = "black")

    if(chosenStatistic == ''):
        statisticLabel.config(text = "Please choose a valid statistic", fg = "red")
        return False
    else:
        statisticLabel.config(text = "Choose a statistic:", fg = "black")

    if(chosenSeason == "Career"):
        menu = seasonDropdown["menu"]
        last = menu.index("end")
        allSeasons = []
        for index in range(last):
            allSeasons.append(menu.entrycget(index, "label"))

        for currentSeason in allSeasons:
            statList += bs.getStatList(chosenName, currentSeason, chosenStatistic)
    else:
        statList = bs.getStatList(chosenName.lower(), chosenSeason, chosenStatistic)

    for i in range(len(statList)):
        statList[i] = float(str(statList[i]))

    stdDev = bs.calculateStandardDev(statList)
    average = bs.calculateAverage(statList)

    chosenName = bs.capitalizeName(name.get())

    resultLabel.config(text = "The consistency for " + chosenName + " for " + chosenStatistic +
                        " in " + chosenSeason + " is " + stdDev + "." + "\nIn 95% of games, " + chosenName +
                        " will be " + stdDev + " " + chosenStatistic +" within their\n average of " + average + " " + chosenStatistic+ ".")
    if(first == False):
        t = [b.remove() for b in bars]

    p=f.gca()
    counts, bins, bars = p.hist(statList)
    p.relim()
    p.autoscale(axis = 'x')

    p.set_xlabel(chosenStatistic + " Count")
    p.set_ylabel("Number of Games")
    first = False

    canvas.show()

global first
global bars

first = True

root = tk.Tk()
root.title("Fantasy Basketball Application by Saurav Pahadia")

frame = tk.Frame(root, background = "#ecf0f1")

title = tk.Label(root, text = "Consistency Calculator")
title.pack(pady = 10)

nameLabel = tk.Label(root, text = "Enter full name of player here:")
nameLabel.pack(pady = 10)

name = tk.StringVar()

nameEntry = tk.Entry(root, textvariable = name)
nameEntry.pack()

nameButton = tk.Button(root, text = "Enter Name", command = nameRun)
nameButton.pack()

seasonLabel = tk.Label(root, text = "Choose season of player, or total career:")
seasonLabel.pack(pady = 10, padx = 50)

season = tk.StringVar(root)

seasonDropdown = tk.OptionMenu(root, season, "Enter a Season")
seasonDropdown.config(width = "50")
seasonDropdown.pack(padx = 10)

statisticLabel = tk.Label(root, text = "Choose a statistic:")
statisticLabel.pack(pady = 10)

statistic = tk.StringVar(root)

statisticDropdown = tk.OptionMenu(root, statistic, "Field Goal %", "3 Pointers Made", "Free Throw %", "Rebounds", "Assists", "Steals", "Blocks", "Turnovers", "Points")
statisticDropdown.config(width = "50")
statisticDropdown.pack(padx=10)

goButton = tk.Button(root, text = "Go", command = run)
goButton.pack(pady = 10)

resultLabel = tk.Label(root, text = "\n\n\n")
resultLabel.pack(pady = 20)

f = Figure()
canvas = FigureCanvasTkAgg(f, master=frame)
canvas.get_tk_widget().pack()

frame.pack()
root.mainloop()
