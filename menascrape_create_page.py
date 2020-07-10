from toornament_scraper.parser import Parser
from toornament_scraper.match import Match


class MenaScraperCreatePage(object):
    
    def run(self):
        matches = self.parser.run()
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

if __name__ == "__main__":
    pageCreate = MenaScraperCreatePage()
    pageCreate.run()

#Template examples
# {{MatchSchedule/Start|tab=Day 1 |bestof=1 |shownname=IAC 2020 Egypt Split 1 }}
# {{MatchSchedule|initialorder=1|team1=USG |team2=La Cucaracha |team1score=0 |team2score=1 |winner=2 |date=2020-05-29|time=20:00 |timezone=CET 
# |dst=yes |stream= |direct_link=/en_GB/tournaments/3543821601845821440/matches/3603290114320777433/ |page=1 }}