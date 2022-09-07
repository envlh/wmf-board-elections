## Description

The script `retrieve-votes.py` checks that voters of the 2022 Wikimedia Foundation board elections comply with some of the [rules for voting eligibility](https://meta.wikimedia.org/wiki/Wikimedia_Foundation_elections/2022/Voter_eligibility_guidelines).

The script `generate-statistics.py` generates various aggregated statistics about voters. It must be run after `retrieve-votes.py`.

## Run

This project requires Python 3.

After downloading or cloning the project with your favorite git client, run the following command:

    python3 src/retrieve-votes.py

Optionally, you can generate statistics:

    python3 src/generate-statistics.py

## Copyright

This project, by [Envel Le Hir](https://www.lehir.net/) (@envlh), is under [CC0](https://creativecommons.org/publicdomain/zero/1.0/) license (public domain dedication).
