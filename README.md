# Trello-automation

A tool to improve Trello.

# General setup:

For the application to work you need a Trello API key and token. Both can be generated on this site:
https://trello.com/app-key

Save those values in 'my_secrets.py' as shown in 'my_secrets_example.py'

## Setup

1. Create python environment from `requirements.txt`
2. For the application to work you need a Trello API key and token. Both can be generated on this site:
   https://trello.com/app-key
3. Save those values in 'my_secrets.py' as shown in 'my_secrets_example.py'
4. Set up the pre-commit hook running `pre-commit install`, then it will run automatically on `git commit` or
   use `pre-commit run --all-files`

# IDs:

You also need the IDs of boards you want to search, members you want to search for and ID of the list you want to copy
the cards in:

1. Run `get_name_id_pairs_of_my_boards()`, then select boards you want to search and paste their ids to `BOARD_IDS`
   variable in `my_settings.py`. If you don't have this file create it according to `my_settings_example.py`.
2. Run `get_name_id_pairs_of_board_members(BOARD_ID)` to get the IDs of members on a given board and fill required
   parameters in `my_settings.py`.
3. Run `get_board_list_name_id_pairs(BOARD_ID)` to get IDs of lists on a given board and fill required parameters
   in `my_settings.py`.
4. Optionally, paste ID's of lists you want to exclude and don't copy from, to IDS_OF_LISTS_TO_EXCLUDE . (The target ID
   is excluded
   automatically.)
5. After this initial setup only the `main()` function should be run to perform the functionality.
