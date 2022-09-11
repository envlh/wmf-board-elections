import utils


def main():

    votes = utils.load_json_file('data/votes.json')

    for vote in votes:
        if 'securepoll-struck-vote' in vote['options']:
            print('Vote by User:{} on {} is struck.'.format(vote['login'], vote['date']))


if __name__ == '__main__':
    main()
