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

https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/3603290114354332214/ --- Completed 
https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/3603290114320777496/ --- Not completed yet
https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/3603290114387887185/ --- Forfeit
'''

import requests
from bs4 import BeautifulSoup
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Match():
    def __init__(self,date, completed, group, tournamentRound, team1, team2, team1score, team2score, winner, url):
        self.date = date
        self.completed = completed
        self.group = group
        self.tournamentRound = tournamentRound
        self.team1 = team1
        self.team2 = team2
        self.team1score = team1score
        self.team2score = team2score
        self.winner = winner
        self.url = url

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
        print(self.url)
    

def GetGroupRounds(url, baseUrl):
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


def GetMatchData(url):

    matchPage = requests.get(url)
    matchSoup = BeautifulSoup(matchPage.text, features="html.parser")

    matchProperties = matchSoup.findAll('div', {'class': 'match format-info'})

    if matchProperties[0].findAll('div', {'class': 'value'})[1].text == 'completed':
        if matchSoup.select('#main-container > div.layout-section.header > div > div.layout-block.header.mobile-hide.tablet-hide > div > div > div.state > div > div.result-1.forfeit.text'):
            match = Match(\
                date=matchProperties[0].find('datetime-view')['value'],\
                completed=True,\
                group=matchProperties[0].findAll('div', {'class': 'value'})[5].text.strip(),\
                tournamentRound=matchProperties[0].findAll('div', {'class': 'value'})[6].text.strip(),\
                team1=matchProperties[1].findAll('div', {'class': 'name'})[1].text.strip(),\
                team2=matchProperties[1].findAll('div', {'class': 'name'})[2].text.strip(),\
                team1score='FORFEIT',\
                team2score='FORFEIT',\
                winner='FORFEIT',\
                url=url\
                )#designate these as MISSING because they should be populated if status == completed
            
        else:        
            match = Match(\
                date=matchProperties[0].find('datetime-view')['value'],\
                completed=True,\
                group=matchProperties[0].findAll('div', {'class': 'value'})[5].text.strip(),\
                tournamentRound=matchProperties[0].findAll('div', {'class': 'value'})[6].text.strip(),\
                team1=matchProperties[1].findAll('div', {'class': 'name'})[1].text.strip(),\
                team2=matchProperties[1].findAll('div', {'class': 'name'})[2].text.strip(),\
                team1score='MISSING',\
                team2score='MISSING',\
                winner='MISSING',\
                url=url\
                )#designate these as MISSING because they should be populated if status == completed
            
            match = CalculateWinner(match, matchProperties[1])

    else: 
        match = Match(\
            date=matchProperties[0].find('datetime-view')['value'],\
            completed=False,\
            group=matchProperties[0].findAll('div', {'class': 'value'})[4].text.strip(),\
            tournamentRound=matchProperties[0].findAll('div', {'class': 'value'})[5].text.strip(),\
            team1=matchProperties[1].findAll('div', {'class': 'name'})[1].text.strip(),\
            team2=matchProperties[1].findAll('div', {'class': 'name'})[2].text.strip(),\
            team1score='NULL',\
            team2score='NULL',\
            winner='NULL',\
            url=url\
            )#these are NULL because a match yet to happen has no winner...

    return match

def Main():
    baseUrl = 'https://www.toornament.com'
    groupPage = requests.get('https://www.toornament.com/en_GB/tournaments/3543821601845821440/stages/3603290113079263232/')
    groupSoup = BeautifulSoup(groupPage.text, features="html.parser")

    matchList = []
    finalOutput = []

    for x in range(16):
        groupBlock = groupSoup.select("#main-container > div.layout-section.content > section > div > div:nth-child(2) > div > div:nth-child({})".format(x+1))
        for tag in groupBlock:
            matchList.extend(GetGroupRounds(baseUrl + tag.find('a', href=True)['href'], baseUrl))
    
    print('Total Matches to be scraped: ' + str(len(matchList)))
    for match in matchList:
        try:
            GetMatchData(match).PrintMatch()
        except:
            print('ERROR WITH MATCH - Contact Chorbadji at Leaguepedia API Discord')

Main()
#RTL for Arabic teams needed?
#logging? number inserted (completed/forfeited/still to play)
#need totally different script likely for knockout stage