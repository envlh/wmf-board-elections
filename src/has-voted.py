import utils


def main():

    login = ''

    votes = utils.load_json_file('data/votes.json')

    for vote in votes:
        if vote['login'] == login:
            print('{} voted.'.format(login))
            if vote['options']:
                print('Vote is not valid.')


if __name__ == '__main__':
    main()
