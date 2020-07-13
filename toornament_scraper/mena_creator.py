from toornament_scraper.parser import Parser
from river_mwclient.wiki_time_parser import time_from_str
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from mwparserfromhell.nodes import Template


class MenaCreator(object):
    def __init__(self, site: EsportsClient, title: str, bestof=1):
        self.site = site
        self.event = self.site.target(title).strip()
        self.data_page = self.site.client.pages['Data:' + self.event]
        self.overview_page = self.site.client.pages[self.event]
        self.toornament = self.site.cargo_client.query_one_result(
            tables='Tournaments',
            where='OverviewPage="{}"'.format(self.event),
            fields='ScrapeLink'
        )
        self.summary = "Edit made by web scraping!"
        self.parser = Parser(self.toornament)

        self.intro_template = Template(name="MatchSchedule/Start")
        self.intro_template.add('bestof', str(bestof))
        self.sandbox_page = self.site.client.pages['User:RheingoldRiver/Toornament_Sandbox']

    def run(self):
        matches = self.parser.run()
        output_list = []
        current_day_index = 1
        previousDate = time_from_str('1900-01-01 00:00:00+00:00')
        for match in matches:
            if match.timestamp.cet_date != previousDate.cet_date:
                self.intro_template.add('tab', 'Day {}'.format(current_day_index), before="bestof")
                output_list.append(str(self.intro_template))
                previousDate.cet_date = match.timestamp.cet_date
                current_day_index += 1
            output_list.append(match.print())
        self.site.client.pages[self.sandbox_page].save('\n'.join(output_list))
        return 'https://lol.gamepedia.com/' + self.sandbox_page.name.replace(' ', '_')


if __name__ == "__main__":
    credentials = AuthCredentials(user_file="me")
    site = EsportsClient('lol', credentials=credentials)
    MenaCreator(site, 'Intel Arabian Cup 2020/Egypt/Split 1').run()
