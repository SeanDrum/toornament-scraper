from toornament_scraper.parser import Parser
from toornament_scraper.match import Match
from river_mwclient.wiki_time_parser import time_from_str
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials


class MenaScraperCreatePage(object):
    def __init__(self):
        self.sectionTemplate = r'{{{{MatchSchedule/Start|tab=Day {} |bestof=1 |shownname=IAC 2020 Egypt Split 1 }}}}'
        self.baseUrl = 'https://www.toornament.com/en_GB/tournaments/3543821601845821440/matches/schedule?page='
        self.credentials = AuthCredentials(user_file="me")
        self.site = EsportsClient('lol', credentials=self.credentials)

    def run(self):
        parser = Parser(self.baseUrl)
        matchList = parser.run()

        outputList = []
        finalOutput = ''
        day = 0
        previousDate = time_from_str('2020-01-01 18:00:00+00:00')#way before the tourney so it definitely fires the compare on first run

        for match in matchList:
            if match.timestamp.cet_date != previousDate.cet_date:
                day = day + 1
                outputList.append(self.sectionTemplate.format(str(day)))
                previousDate.cet_date = match.timestamp.cet_date

            outputList.append(match.print())

        finalOutput = '\n'.join(outputList)
        self.site.client.pages["User:RheingoldRiver/Toornament Sandbox"].save(finalOutput)

if __name__ == "__main__":
    pageCreate = MenaScraperCreatePage()
    pageCreate.run()



#https://lol.gamepedia.com/User:Chorbadji/Toornament_Sandbox?profile=no
