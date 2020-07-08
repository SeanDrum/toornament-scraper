import requests
from bs4 import BeautifulSoup
import pprint
from toornament_scraper.match import Match
# from match import Match

pp = pprint.PrettyPrinter(indent=4)


class Parser(object):
    baseUrl = 'https://www.toornament.com'
    
    def GetGroupRounds(self, url):
        roundPage = requests.get(self.baseUrl + url)
        roundSoup = BeautifulSoup(roundPage.text, features='html.parser')
        roundList = []
        
        roundGrid = roundSoup.findAll('div', {'class': 'grid-flex vertical spacing-large'})
        for round in roundGrid:
            for a in round.findAll('a', href=True):
                if a.text:
                    roundList.append(self.baseUrl + (a['href']))
        
        return roundList
        
    def CalculateWinner(self, match, matchProperties):
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

    def GetMatchData(self, url):
        matchPage = requests.get(url)
        matchSoup = BeautifulSoup(matchPage.text, features="html.parser")
        
        matchProperties = matchSoup.findAll('div', {'class': 'match format-info'})
        
        if matchProperties[0].findAll('div', {'class': 'value'})[1].text == 'completed':
            if matchSoup.select(
                            '#main-container > div.layout-section.header > div > div.layout-block.header.mobile-hide.tablet-hide > div > div > div.state > div > div.result-1.forfeit.text'):
                match = Match( \
                    date=matchProperties[0].find('datetime-view')['value'], \
                    completed=True, \
                    group=matchProperties[0].findAll('div', {'class': 'value'})[5].text.strip(), \
                    tournamentRound=matchProperties[0].findAll('div', {'class': 'value'})[6].text.strip(), \
                    team1=matchProperties[1].findAll('div', {'class': 'name'})[1].text.strip(), \
                    team2=matchProperties[1].findAll('div', {'class': 'name'})[2].text.strip(), \
                    team1score='FORFEIT', \
                    team2score='FORFEIT', \
                    winner='FORFEIT', \
                    url=url \
                    )  # designate these as MISSING because they should be populated if status == completed
            
            else:
                match = Match( \
                    date=matchProperties[0].find('datetime-view')['value'], \
                    completed=True, \
                    group=matchProperties[0].findAll('div', {'class': 'value'})[5].text.strip(), \
                    tournamentRound=matchProperties[0].findAll('div', {'class': 'value'})[6].text.strip(), \
                    team1=matchProperties[1].findAll('div', {'class': 'name'})[1].text.strip(), \
                    team2=matchProperties[1].findAll('div', {'class': 'name'})[2].text.strip(), \
                    team1score='MISSING', \
                    team2score='MISSING', \
                    winner='MISSING', \
                    url=url \
                    )  # designate these as MISSING because they should be populated if status == completed
                
                match = self.CalculateWinner(match, matchProperties[1])
        
        else:
            match = Match( \
                date=matchProperties[0].find('datetime-view')['value'], \
                completed=False, \
                group=matchProperties[0].findAll('div', {'class': 'value'})[4].text.strip(), \
                tournamentRound=matchProperties[0].findAll('div', {'class': 'value'})[5].text.strip(), \
                team1=matchProperties[1].findAll('div', {'class': 'name'})[1].text.strip(), \
                team2=matchProperties[1].findAll('div', {'class': 'name'})[2].text.strip(), \
                team1score='NULL', \
                team2score='NULL', \
                winner='NULL', \
                url=url \
                )  # these are NULL because a match yet to happen has no winner...
        
        return match

    def run(self, url):
        groupPage = requests.get(url)
        groupSoup = BeautifulSoup(groupPage.text, features="html.parser")
        
        matchList = []
        finalOutput = []
        
        for x in range(16):
            groupBlock = groupSoup.select(
                "#main-container > div.layout-section.content > section > div > div:nth-child(2) > div > div:nth-child({})".format(
                    x + 1))
            for tag in groupBlock:
                matchList.extend(self.GetGroupRounds(tag.find('a', href=True)['href']))
        
        print('Total Matches to be scraped: ' + str(len(matchList)))
        
        returnList = []
        
        # returnList.append(self.GetMatchData(matchList[0]))
        # return returnList
        # matchList = ['https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/3603290114320777594/']
        
        round1List = []
        round2List = []
        round3List = []
        round4List = []
        round5List = []
        round6List = []
        round7List = []

        
        for match in matchList:
            try:
                game = self.GetMatchData(match)
                # game.PrintMatch()
                if game.tournamentRound == "Round 1":
                    round1List.append(game)
                elif game.tournamentRound == "Round 2":
                    round2List.append(game)
                elif game.tournamentRound == "Round 3":
                    round3List.append(game)
                elif game.tournamentRound == "Round 4":
                    round4List.append(game)
                elif game.tournamentRound == "Round 5":
                    round5List.append(game)
                elif game.tournamentRound == "Round 6":
                    round6List.append(game)
                elif game.tournamentRound == "Round 7":
                    round7List.append(game)
                else: 
                    print('round not found')
            except:
                print('ERROR WITH MATCH - Contact Chorbadji at Leaguepedia API Discord')
        

        returnList = [round1List, round2List, round3List, round4List, round5List, round6List, round7List]

        return returnList


if __name__ == '__main__':
    Parser().run('https://www.toornament.com/en_GB/tournaments/3543821601845821440/stages/3603290113079263232/')

# RTL for Arabic teams needed?
# logging? number inserted (completed/forfeited/still to play)
# need totally different script likely for knockout stage

# url='https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/3603290114320777594/'
# result = Parser().GetMatchData(url)
# result.PrintMatch()