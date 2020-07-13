import mwparserfromhell
from river_mwclient.esports_client import EsportsClient
import requests
from bs4 import BeautifulSoup
from mwparserfromhell.nodes import Template


class FFChecker(object):
    domain = 'https://toornament.com'

    def __init__(self, site: EsportsClient, title: str):
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

    def run(self):
        text = self.data_page.text()
        wikitext = mwparserfromhell.parse(text)
        for template in wikitext.filter_templates():
            template: Template
            if not template.name.matches('MatchSchedule'):
                continue
            if template.has('checked_ff'):
                continue
            if not template.has('direct_link'):
                continue
            if not template.has('winner'):
                continue
            winner = int(template.get('winner').value.strip())
            if not winner:
                continue
            direct_link = template.get('direct_link').value.strip()
            url = self.domain + direct_link
            page_soup = BeautifulSoup(requests.get(url).text, features='html.parser')
            forfeit_text = page_soup.find_all('div', {'class': 'result forfeit'})
            if len(forfeit_text) > 0:
                if winner == 1:
                    template.add('ff', '2', before='winner')
                elif winner == 2:
                    template.add('ff', '1', before='winner')
            template.add('checked_ff', 'Yes')
        self.data_page.save(str(wikitext), summary=self.summary)
        return 'https://lol.gamepedia.com/' + self.data_page.name.replace(' ', '_')
