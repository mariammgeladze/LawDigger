import urllib2
import re
import bs4
from bs4 import BeautifulSoup
from . import models
from . import repos


class LawParser(object):

    def fetch_html(self, url):
        response = urllib2.urlopen(url)
        return response.read()

    def fetch_soup(self, url):
        return BeautifulSoup(self.fetch_html(url))

    def get_soup_text(self, soup_elem):
        text = soup_elem.get_text(' ', strip=True).encode('utf-8')
        return text

    def commit(self, tag_name):
        repos.update(self.laws, tag_name, self.REPO_REL_PATH)


class OrLawParser(LawParser):

    REPO_REL_PATH = 'or'

    sources = [
        {
            'tag': 2011,
            'crawl': [
                'http://www.leg.state.or.us/ors/vol1.html'
            ],
            'crawl_link_pattern': re.compile(r'\d+\.html')
        }
    ]

    def __init__(self):
        self.section_re = re.compile('(\d+\.\d+)\s(\S)')
        self.title_re = re.compile('\d+\.\d+\s([\w|\s|;|,]+\.)')
        self.laws = []

    def run(self):
        # repos.wipe_and_init(self.REPO_REL_PATH)
        # self.create_laws_from_url(
        #     'http://www.leg.state.or.us/ors_archives/1995ORS/007.html')
        # self.commit('1995')

        # self.laws = []
        # self.create_laws_from_url(
        #     'http://www.leg.state.or.us/ors_archives/2009/007.html')
        # self.commit('2009')

        diff = repos.get_tag_diff('7.110', '1995', '2009', self.REPO_REL_PATH)
        print('diff: {v}'.format(v=diff))

    def fetch_urls(self):
        urls = []
        for batch in self.sources:
            for url in batch['crawl']:
                soup = BeautifulSoup(self.fetch_html(url))
                url_base = url[:url.rindex('/')] + '/'
                for link in soup.find_all(href=batch['crawl_link_pattern']):
                    full_link = url_base + link.get('href')
                    urls.append(full_link)
        return urls

    def create_laws_from_url(self, url):
        soup = self.fetch_soup(url)
        for elem in soup.find_all('p'):
            text = self.get_soup_text(elem)
            section_matches = self.section_re.match(text)
            if section_matches:
                section = section_matches.group(1)
                title_matches = self.title_re.match(text)
                if title_matches:
                    title = title_matches.group(1)
                    law_text = text[title_matches.end():]
                    law_text = law_text.strip()
                else:
                    title = ''
                    law_text = text[section_matches.end() - 1:]
                    law_text = ' '.join(law_text.splitlines())

                title = ' '.join(title.splitlines())
                law = models.OregonRevisedStatute(section, title, law_text)
                law.append_text(self.get_law_text(elem))
                self.laws.append(law)

    def get_law_text(self, soup_elem):
        text = ''
        for next in soup_elem.next_siblings:
            if not isinstance(next, bs4.element.Tag):
                continue
            next_text = self.get_soup_text(next)
            if self.section_re.match(next_text):
                break
            if next_text.isupper():
                break
            text += '\n' + next_text.strip()
        return text

p = OrLawParser()
p.run()
