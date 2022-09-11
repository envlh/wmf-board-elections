import utils


def main():

    login = ''

    votes = utils.load_json_file('data/votes.json')

    found = False

    for vote in votes:
        if vote['login'] == login:
            found = True
            print('User:{} voted on {}'.format(login, vote['date']))
            if vote['options']:
                print('Previous vote is not valid: {}'.format(', '.join(vote['options'])))

    if not found:
        print('No vote found for User:{}'.format(login))


if __name__ == '__main__':
    main()
