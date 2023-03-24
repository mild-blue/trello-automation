import datetime
import logging

from actions.copying import copy_cards_with_tagged_members_and_close_due_date_to_list
from actions.moving import move_cards_with_close_due_date_between_lists
from my_settings import (DEFAULT_TARGET_LIST_ID, LIST_IDS_TO_SORT,
                         MOVE_FROM_LIST_IDS,
                         NUMBER_OF_DAYS_TO_CONSIDER_IN_THE_SEARCH)
from actions.sorting import sort_list_by_due_date

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.propagate = False
logger.addHandler(console_handler)


def main():
    latest_due_date = datetime.date.today() + datetime.timedelta(days=NUMBER_OF_DAYS_TO_CONSIDER_IN_THE_SEARCH)
    logger.info('Starting to move cards with close due date...')
    for move_from_list_id in MOVE_FROM_LIST_IDS:
        move_cards_with_close_due_date_between_lists(latest_due_date=latest_due_date,
                                                     source_list_id=move_from_list_id,
                                                     target_list_id=DEFAULT_TARGET_LIST_ID)
    logger.info('Moving cards complete. Starting to copy cards...')
    copy_cards_with_tagged_members_and_close_due_date_to_list(latest_due_date=latest_due_date)
    logger.info('Copying cards complete. Starting to sort lists...')
    for sort_list_id in LIST_IDS_TO_SORT:
        sort_list_by_due_date(sort_list_id)
    logger.info('Sorting lists complete. Finished!')


if __name__ == '__main__':
    # get_name_id_pairs_of_my_boards()
    # get_name_id_pairs_of_board_members(BOARD_IDS[0])
    # get_board_list_name_id_pairs(BOARD_IDS[0])
    main()
