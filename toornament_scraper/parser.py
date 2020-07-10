import requests
from bs4 import BeautifulSoup
import pprint
import re
from match import Match
from datetime import datetime
from river_mwclient.wiki_time_parser import time_from_str


class Parser(object):
    
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
    
    def CalculateWinner(self, html, match):
        winner = html.findAll('div', {'class': 'name'})[0].text.strip()
        
        if winner == match.team1:
            match.team1score = 1
            match.team2score = 0
            match.winner = 1
        else:
            match.team1score = 0
            match.team2score = 1
            match.winner = 2
        
        return match
    
    def run(self):
        
        matchListFinal = []
        for page in range(1, 2):
            getUrl = self.baseUrl + str(page)
            
            pageList = requests.get(getUrl)
            pageSoup = BeautifulSoup(pageList.text, features='html.parser')
            roundList = []
            
            matchListRaw = pageSoup.findAll('div', {'class': 'grid-flex vertical spaceless'})
            matchListDiv = matchListRaw[0].find_all(lambda tag: tag.name == 'div' and
                                                                tag.get('class') == ['size-content'])
            '''
        roundGrid = roundSoup.findAll('div', {'class': 'grid-flex vertical spacing-large'})
        for round in roundGrid:
            for a in round.findAll('a', href=True):
                if a.text:
                    roundList.append(self.baseUrl + (a['href']))

            '''


            for match in matchListDiv:
                new_match = None
                try:
                    m = Match(
                        date=time_from_str(matchListRaw[0].find('datetime-view')['value']),
                        completed=True,
                        team1=match.findAll('div', {'class': 'name'})[0].text.strip(),
                        team2=match.findAll('div', {'class': 'name'})[1].text.strip(),
                        team1score='TBD',
                        team2score='TBD',
                        winner='TBD',
                        url=match.findAll('a', href=True)[0]['href'],
                        page=page
                    )
                    if not match.findAll('div', {'class': 'opponent win'}):
                        m.team1score = 0
                        m.team2score = 0
                        m.winner = 0
                        m.isForfeit = 'BOTH'
                    else:
                        m.isForfeit = 'NO'                                      
                        m = self.CalculateWinner(match.findAll('div', {'class': 'opponent win'})[0], m) 
                    
                    new_match = m
                
                except IndexError:
                    new_match = Match(completed=False)
                
                matchListFinal.append(new_match)
        
        return matchListFinal


if __name__ == '__main__':
    matchList = Parser('https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/schedule?page=').run()

    sectionTemplate = r'{{MatchSchedule/Start|tab=Day {} |bestof=1 |shownname=IAC 2020 Egypt Split 1 }}'
    matchTemplate = r'# {{MatchSchedule|team1={team1} |team2={team2} |team1score={team1score} |team2score={team2score} |winner={winner} |date={date}|time={time} |timezone=CET | dst= {dst} |stream= |direct_link={url} |page={page} }}'

    day = 1
    previousDate = time_from_str('2020-01-01 18:00:00+00:00')#way before the tourney so it definitely fires the compare on first run
    outF = open("myOutFile.txt", "w")
    

    for match in matchList:
        if match.date != previousDate:
            day = day + 1
            outF.write(sectionTemplate.format(str(day)))
    
        outF.write(matchTemplate.format(\
            team1 = match.team1,\
            team2 = match.team2,\                
            team1score = match.team1score,\
            team2score = match.team2score,\
            winner = match.winner,\
            date = match.date.cet_date,\
            time = match.date.cet_time,\
            dst = match.date.dst,\
            url = match.url,\
            page = match.page))

        previousDate = match.date
    outF.close()




#example single ff
#https://www.toornament.com/en_GB/tournaments/3543967453632937984/matches/schedule?page=1
#https://www.toornament.com/en_GB/tournaments/3543967453632937984/matches/3603330036821811312/

#Template examples
# {{MatchSchedule/Start|tab=Day 1 |bestof=1 |shownname=IAC 2020 Egypt Split 1 }}
# {{MatchSchedule|initialorder=1|team1=USG |team2=La Cucaracha |team1score=0 |team2score=1 |winner=2 |date=2020-05-29|time=20:00 |timezone=CET 
# |dst=yes |stream= |direct_link=/en_GB/tournaments/3543821601845821440/matches/3603290114320777433/ |page=1 }}