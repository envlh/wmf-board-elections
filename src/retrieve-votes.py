import html
import json
import re

import utils


def main():
    active_votes_count = 0
    votes = []
    url = 'https://vote.wikimedia.org/w/index.php?title=Special:SecurePoll/list/1364&limit=500'
    while url:
        print(url)
        vote_data = utils.fetch_url(url)
        # next page
        url_match = set(re.findall("<a role='button' tabindex='0' href='([^']+)' rel='nofollow' class='oo-ui-buttonElement-button'><span class='oo-ui-iconElement-icon oo-ui-icon-next oo-ui-image-progressive'></span><span class='oo-ui-labelElement-label'>Next page</span>", vote_data))
        if url_match:
            url = 'https://vote.wikimedia.org{}'.format(html.unescape(url_match.pop()))
        else:
            url = None
        # votes data
        vote_matches = re.findall('<tr(?: class="([^<>]+)")?>\n<td class="TablePager_col_vote_id">([^<]+)</td>\n<td class="TablePager_col_vote_voter_name">([^<]+)</td>\n<td class="TablePager_col_vote_voter_domain">([^<]+)</td>\n</tr>', vote_data)
        for vote_match in vote_matches:
            vote = {'login': html.unescape(vote_match[2]), 'home': vote_match[3], 'vote_date': vote_match[1], 'options': sorted(set(vote_match[0].split())), 'wikis': []}
            if not vote['options']:
                active_votes_count += 1
            wikis = []
            wiki_data = utils.fetch_url('https://meta.wikimedia.org/wiki/Special:CentralAuth/{}'.format(vote['login'].replace(' ', '_')))
            # year of registration
            match = re.findall('<strong>Registered:</strong> [^(]+ ([0-9]{4}) \\(', wiki_data)
            if match:
                vote['registration'] = match.pop()
            else:
                vote['registration'] = 'N/A'
            # wikis
            wiki_matches = re.findall('<tr><td><a[^<>]+>([^<>]+)</a></td><td data-sort-value="([0-9]+)">[^<>]+</td><td style="text-align: center;"><img[^<>]+/><span[^<>]+>\\(\\?\\)</span></td><td><a[^<>]+>.*?</a></td><td style="text-align: right;"><a[^<>]+>([0-9,]+)</a></td><td>(.*?)</td></tr>', wiki_data)
            for wiki_match in wiki_matches:
                wiki = {'url': wiki_match[0], 'sub_date': wiki_match[1], 'edits': int(wiki_match[2].replace(',', '')), 'groups': sorted(set(filter(None, wiki_match[3].split(', '))))}
                wikis.append(wiki)
                if 'bot' in wiki['groups'] or 'copyviobot' in wiki['groups']:
                    print('{} has a bot flag on {}'.format(vote['login'], wiki['url']))
            vote['wikis'] = wikis
            votes.append(vote)
    utils.file_put_contents('data/votes.json', json.dumps(votes))
    print('{} votes, {} active.'.format(len(votes), active_votes_count))


if __name__ == '__main__':
    main()
