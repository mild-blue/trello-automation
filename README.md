# trello-automation
A tool to improve Trello.

# Setup:
For the application to work you need a Trello API key and token. Both can be generated on this site:
https://trello.com/app-key

Save those values in 'my_secrets.py' as shown in 'my_secrets_example.py'

## Setup
1. Create python environment from `requirements.txt`
2. For the application to work you need a Trello API key and token. Both can be generated on this site:
https://trello.com/app-key
3. Save those values in 'my_secrets.py' as shown in 'my_secrets_example.py'
4. Set up the pre-commit hook running `pre-commit install`, then it will run automatically on `git commit` or use `pre-commit run --all-files`


# IDs:
You also need the IDs of boards you want to search, members you want to search for and ID of the list you want to copy the cards in.
The easiest way to get these is directly through the Trello website:
1. Go to the board you want to search.
2. Click on a card in the list that you want to place the new cards in. (If it doesn't exist yet then create one.)
3. On the bottom right click on 'Share' and then 'Export JSON'.
4. In the JSON file you can easily search for 'idBoard', 'idList' and 'idMembers'.
5. Optionally paste ID's of lists you want to exclude from search to IDS_OF_LISTS_TO_EXCLUDE . (The target ID is excluded automatically.)

These ID's then need to be saved in 'my_settings.py' as shown in 'my_settings_example.py' .
