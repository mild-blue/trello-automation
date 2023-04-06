# Trello-Automation

A tool to streamline Trello workflows.

## Quick Setup

1. Install Python 3.9 or newer.
2. Create a Python environment from `requirements.txt`.
3. Obtain a Trello API key and token from [https://trello.com/app-key](https://trello.com/app-key).
4. Save these values in `my_secrets.py` (refer to `my_secrets_example.py`).
5. Configure the pre-commit hook by running `pre-commit install`.

## Configuration

1. Run `get_name_id_pairs_of_my_boards()` and add desired board IDs to `my_settings.py` (create from `my_settings_example.py` if needed).
2. Run `get_name_id_pairs_of_board_members(BOARD_ID)` and update the necessary member parameters in `my_settings.py`.
3. Run `get_board_list_name_id_pairs(BOARD_ID)` and update the required list parameters in `my_settings.py`.
4. Optional: Add list IDs to exclude in `IDS_OF_LISTS_TO_EXCLUDE` (target ID is excluded by default).

After the initial setup, simply run the `main()` function to execute the tool.