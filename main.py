'''
initialorder=1 <what is this?
team1=USG (Egyptian Team) 
team2=La Cucaracha 
team1score=0 
team2score=1 <this could be more than one if it was a best of five?
winner=2 
date=2020-05-29
time=20:00 
timezone=CET <will look at later
dst=yes <what's this? daylight savings time?
stream= <obviously can be NULL because we won't have any

https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/3603290114354332214/
https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/3603290114320777496/
'''

import requests
from bs4 import BeautifulSoup
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Match():
    def __init__(self,date, completed, group, tournamentRound, team1, team2, team1score, team2score, winner):
        self.date = date
        self.completed = completed
        self.group = group
        self.tournamentRound = tournamentRound
        self.team1 = team1
        self.team2 = team2
        self.team1score = team1score
        self.team2score = team2score
        self.winner = winner

    def PrintMatch(self):
        print(self.date)
        print(self.completed)
        print(self.group)
        print(self.tournamentRound)
        print(self.team1)
        print(self.team2)
        print(self.team1score)
        print(self.team2score)
        print(self.winner)


def Main():
    baseUrl = 'https://www.toornament.com'
    groupPage = requests.get('https://www.toornament.com/en_GB/tournaments/3543821601845821440/stages/3603290113079263232/')
    groupSoup = BeautifulSoup(groupPage.text, features="html.parser")

    matchList = []
    finalOutput = []

    for x in range(16):
        groupBlock = groupSoup.select("#main-container > div.layout-section.content > section > div > div:nth-child(2) > div > div:nth-child({})".format(x+1))
        for tag in groupBlock:
            matchList.extend(getGroupRounds(baseUrl + tag.find('a', href=True)['href'], baseUrl))
    
    for match in matchList:
        try:
            getMatchData(match).PrintMatch()
        except:
            print('todo')
    

def getGroupRounds(url, baseUrl):
    roundPage = requests.get(url)
    roundSoup = BeautifulSoup(roundPage.text, features='html.parser')
    roundList = []

    roundGrid = roundSoup.findAll('div', {'class':'grid-flex vertical spacing-large'})
    for round in roundGrid:
        for a in round.findAll('a', href=True):
            if a.text:
                roundList.append(baseUrl + (a['href']))
                
    return roundList


def CalculateWinner(match, matchProperties):
    for divs in matchProperties:
        teams = divs.findAll('div', {'class': 'opponent'})
        for team in teams:
            if team.find('div', class_='result win'):
                if team.find('div', {'class': 'name'}).text.strip() == match.team1:
                    match.winner = 1
                    match.team1score = 1
                    match.team2score = 0
                else: 
                    match.winner = 2
                    match.team1score = 0
                    match.team2score = 1
    
    return match


def getMatchData(url):

    matchPage = requests.get(url)
    matchSoup = BeautifulSoup(matchPage.text, features="html.parser")

    matchProperties = matchSoup.findAll('div', {'class': 'match format-info'})

    if matchProperties[0].findAll('div', {'class': 'value'})[1].text == 'completed':

        match = Match(\
            date=matchProperties[0].find('datetime-view')['value'],\
            completed=True,\
            group=matchProperties[0].findAll('div', {'class': 'value'})[5].text.strip(),\
            tournamentRound=matchProperties[0].findAll('div', {'class': 'value'})[6].text.strip(),\
            team1=matchProperties[1].findAll('div', {'class': 'name'})[1].text.strip(),\
            team2=matchProperties[1].findAll('div', {'class': 'name'})[2].text.strip(),\
            team1score='matchProperties[1]',\
            team2score='matchProperties[1]',\
            winner='null'\
            )
        
        match = CalculateWinner(match, matchProperties[1])

    else: 
        return 'TO DO'

    return match

Main()



