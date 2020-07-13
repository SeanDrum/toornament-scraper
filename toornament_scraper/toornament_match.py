from toornament_scraper.match import Match


class ToornamentMatch(Match):

    def calculate_and_set_winner(self, html):
        winner = html.findAll('div', {'class': 'name'})[0].text.strip()
        self.completed = True
        if winner == self.team1:
            self.team1score = 1
            self.team2score = 0
            self.winner = 1
        else:
            self.team1score = 0
            self.team2score = 1
            self.winner = 2
