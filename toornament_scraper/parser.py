import requests
from bs4 import BeautifulSoup
import pprint
from match import Match


class Parser(object):

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

    def run(self, baseUrl):

        for page in range(1, 5):
            getUrl = baseUrl + str(page)

            pageList = requests.get(getUrl)
            pageSoup = BeautifulSoup(pageList.text, features='html.parser')
            roundList = []

            matchListRaw = pageSoup.findAll('div', {'class': 'grid-flex vertical spaceless'})
            matchListDiv = matchListRaw[0].findAll('div', {'class': 'size-content'})
            matchListFinal = []

            for match in matchListDiv:
                try:
                    m = Match( \
                        date=matchListRaw[0].find('datetime-view')['value'], \
                        completed=True, \
                        team1=match.findAll('div', {'class': 'name'})[0].text.strip(), \
                        team2=match.findAll('div', {'class': 'name'})[1].text.strip(), \
                        team1score='TBD', \
                        team2score='TBD', \
                        winner='TBD')
                    m = CalculateWinner(match.findAll('div', {'class': 'opponent win'})[0], m)
                    matchListFinal.append(m)

                except:  # every other row is going to have something worthwhile because of align-stretch divider
                    pass

            return matchListFinal


if __name__ == '__main__':
    Parser().run('https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/schedule?page=')
