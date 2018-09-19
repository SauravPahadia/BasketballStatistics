# import libraries
from bs4 import BeautifulSoup
import warnings
import numpy as np
import urllib2
import matplotlib.pyplot as plt

#This function capitalizes the first and last name of the player, and returns the value
def capitalizeName(playerName):
    return playerName[0:playerName.find(" ")+1].capitalize() + playerName[playerName.find(" ")+1:len(playerName)].capitalize()

#This function opens the given url using urllib2, and catches any HTTP Error
def pageOpener(page):
    try:
        newPage = urllib2.urlopen(page) #try opening page
    except urllib2.HTTPError:
        return False
    return newPage

#This function splices the given player's name in order to get the necessary pieces
#for the basketball reference url.
def nameSplicer(playerName):
    split = playerName.find(" ")

    try:
        firstChar = playerName[split+1] # get first letter of last name
        spliceLastName = playerName[split+1:split+6] #get first 5 letters of last name
        spliceFirstName = playerName[0:2] # get first two letters of first name
    except IndexError:# index error occurs if any incorrect name is entered
        return False

    return firstChar, spliceLastName, spliceFirstName

#This function  scrapes the web for a given players season and displays them as a menu.
#It returns a list of the seasons
def getSeasonList(playerName):

    if(nameSplicer(playerName) == False): #if there is an error in splicing the name, exit out of method
        return False

    firstChar, spliceLastName, spliceFirstName = nameSplicer(playerName)

    index = getIndex(playerName)
    page = "https://www.basketball-reference.com/players/%(firstChar)s/%(spliceLastName)s%(spliceFirstName)s0%(index)s.html" % locals()
    homePage = pageOpener(page)

    if(homePage == False):#if there is any error in opening homePage, exit out of method
        return False

    homeSoup = BeautifulSoup(homePage, 'html.parser')

    i=0
    list = [None]*25
    for singleSeason in homeSoup.find_all('th', attrs = {"scope":"row", "class":"left", "data-stat":"season"}):
        list[i] = singleSeason.getText()
        i += 1
        if(singleSeason.getText()=="Career"): #get all the seasons and break out of loop once the Career option is reached
            break

    list = filter(None, list) # delete any empty indexes

    return list

#This functions opens up the page of the given players given season and scrapes the website
#for the given statistic. It returns that list.
def getStatList(playerName, seasonChoice, choice):

    character,last,first = nameSplicer(playerName)

    rightSeason = str(int(str(seasonChoice)[0:4])+1)#modifies season choice to make it work in the url

    index = getIndex(playerName)
    page = "https://www.basketball-reference.com/players/%(character)s/%(last)s%(first)s0%(index)s/gamelog/%(rightSeason)s" % locals()

    dstat = {"Field Goal %": "fg_pct", "3 Pointers Made": "fg3", "Free Throw %":"ft_pct",
        "Rebounds":"trb", "Assists":"ast", "Steals":"stl", "Blocks":"blk", "Turnovers":"tov", "Points":"pts"}# dictionary associating chosen statistic with the appropriate word for the HTML search

    seasonPage = pageOpener(page)
    seasonSoup = BeautifulSoup(seasonPage, 'html.parser')

    list = [stat.getText() for stat in
                seasonSoup.find_all('td', attrs  = {"class":"right", "data-stat":dstat[choice]})]#find stats of given choice and keep in list

    list = filter(None, list) # delete any empty indexes

    return list

#This function calculates the given lists standard deviation.
def calculateStandardDev(list):

    try:
        stdDev = np.std(list)
    except RuntimeWarning:
        print("Hmm... Something went wrong! Try again")
        quit()

    stdDev = '{:.5}'.format(str(stdDev))

    return stdDev

#This function calculates the given lists average.
def calculateAverage(list):

    try:
        avg = np.average(list)
    except RuntimeWarning:
        print("Hmm... Something went wrong! Try again")
        quit()

    avg = '{:.5}'.format(str(avg))

    return avg

def getIndex(playerName):
    index = 1
    firstChar, spliceLastName, spliceFirstName = nameSplicer(playerName)

    while(True):
        page = "https://www.basketball-reference.com/players/%(firstChar)s/%(spliceLastName)s%(spliceFirstName)s0%(index)s.html" % locals()
        indexPage = pageOpener(page)
        indexSoup = BeautifulSoup(indexPage, 'html.parser')

        if(indexSoup.find("h1", attrs = {"itemprop":"name"}).getText().lower() == playerName.lower()):
            return index
        index += 1
