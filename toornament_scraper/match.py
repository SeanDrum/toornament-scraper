class Match(object):
    def __init__(self, date=None, completed=None, team1=None, team2=None, team1score=None, team2score=None,
                 winner=None, is_forfeit=None, url=None, page=None):
        self.date = date
        self.completed = completed
        self.team1 = team1
        self.team2 = team2
        self.team1score = team1score
        self.team2score = team2score
        self.winner = winner
        self.is_forfeit = is_forfeit
        self.url = url
        self.page = page

    def PrintMatch(self):
        print(self.date)
        print(self.completed)
        print(self.team1)
        print(self.team2)
        print(self.team1score)
        print(self.team2score)
        print(self.winner)
        print(self.url)
        print(self.page)
