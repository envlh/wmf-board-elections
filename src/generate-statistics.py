import utils


def main():

    votes = utils.load_json_file('data/votes.json')

    years = dict()
    homes = dict()
    most_edited_wikis = dict()

    for vote in votes:
        if not vote['options']:
            if vote['registration'] in years:
                years[vote['registration']] += 1
            else:
                years[vote['registration']] = 1
            # home wiki
            if vote['home'] in homes:
                homes[vote['home']] += 1
            else:
                homes[vote['home']] = 1
            # most edited wiki
            most_edited_wiki = None
            most_edits = 0
            for wiki in vote['wikis']:
                if most_edits < wiki['edits']:
                    most_edited_wiki = wiki['url']
                    most_edits = wiki['edits']
            if most_edits > 0:
                if most_edited_wiki in most_edited_wikis:
                    most_edited_wikis[most_edited_wiki] += 1
                else:
                    most_edited_wikis[most_edited_wiki] = 1

    print('\nNumber of votes per year of registration:')
    for year in {k: v for k, v in sorted(years.items(), key=lambda item: item[0])}:
        print('{};{}'.format(year, years[year]))

    print('\nHome wikis:')
    for home in {k: v for k, v in sorted(homes.items(), key=lambda item: item[1], reverse=True)}:
        print('{};{}'.format(home, homes[home]))

    print('\nMost edited wikis:')
    for wiki in {k: v for k, v in sorted(most_edited_wikis.items(), key=lambda item: item[1], reverse=True)}:
        print('{};{}'.format(wiki, most_edited_wikis[wiki]))


if __name__ == '__main__':
    main()
