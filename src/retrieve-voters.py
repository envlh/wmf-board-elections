import hashlib
import html
import re
import requests
import time
from os.path import exists


def file_get_contents(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        s = f.read()
    return s


def file_put_contents(filename, content):
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write(content)


def fetch_url(url):
    urlhash = hashlib.sha1(url.encode()).hexdigest()
    filepath = 'cache/{}.html'.format(urlhash)
    if exists(filepath):
        return file_get_contents(filepath)
    response = requests.get(url, headers={'User-Agent': 'github.com/envlh/wmf-board-elections'}, allow_redirects=False)
    if response.status_code != 200:
        print('Failure while processing URL {} (HTTP code {}).'.format(url, response.status_code))
        exit(1)
    file_put_contents(filepath, response.text)
    time.sleep(5)
    return response.text


class User:

    def __init__(self, login, home, vote_date, options, wikis):
        self.login = login
        self.home = home
        self.vote_date = vote_date
        self.options = options
        self.wikis = wikis

    def __repr__(self):
        return 'User({}, {}, {}, {}, {})'.format(self.login, self.home, self.vote_date, self.options, self.wikis)


class Wiki:

    def __init__(self, url, sub_date, edits, groups):
        self.url = url
        self.sub_date = sub_date
        self.edits = edits
        self.groups = groups

    def __repr__(self):
        return 'Wiki({}, {}, {}, {})'.format(self.url, self.sub_date, self.edits, self.groups)


def main():
    users = set()
    url = 'https://vote.wikimedia.org/w/index.php?title=Special:SecurePoll/list/1364&limit=500'
    while url:
        print(url)
        user_data = fetch_url(url)
        # next page
        url_match = set(re.findall("<a role='button' tabindex='0' href='([^']+)' rel='nofollow' class='oo-ui-buttonElement-button'><span class='oo-ui-iconElement-icon oo-ui-icon-next oo-ui-image-progressive'></span><span class='oo-ui-labelElement-label'>Next page</span>", user_data))
        if url_match:
            url = 'https://vote.wikimedia.org{}'.format(html.unescape(url_match.pop()))
        else:
            url = None
        # users data
        user_matches = re.findall('<tr(?: class="([^<>]+)")?>\n<td class="TablePager_col_vote_id">([^<]+)</td>\n<td class="TablePager_col_vote_voter_name">([^<]+)</td>\n<td class="TablePager_col_vote_voter_domain">([^<]+)</td>\n</tr>', user_data)
        for user_match in user_matches:
            user = User(user_match[2], user_match[3], user_match[1], set(user_match[0].split()), set())
            wikis = set()
            wiki_data = fetch_url('https://meta.wikimedia.org/wiki/Special:CentralAuth/{}'.format(user.login.replace(' ', '_')))
            wiki_matches = re.findall('<tr><td><a[^<>]+>([^<>]+)</a></td><td data-sort-value="([0-9]+)">[^<>]+</td><td style="text-align: center;"><img[^<>]+/><span[^<>]+>\\(\\?\\)</span></td><td><a[^<>]+>.*?</a></td><td style="text-align: right;"><a[^<>]+>([0-9,]+)</a></td><td>(.*?)</td></tr>', wiki_data)
            for wiki_match in wiki_matches:
                wiki = Wiki(wiki_match[0], wiki_match[1], int(wiki_match[2].replace(',', '')), set(filter(None, wiki_match[3].split(', '))))
                wikis.add(wiki)
                if 'bot' in wiki.groups:
                    print('{} is a bot on {}'.format(user.login, wiki.url))
            user.wikis = wikis
            users.add(user)


if __name__ == '__main__':
    main()
