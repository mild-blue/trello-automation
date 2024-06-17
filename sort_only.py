from main import logger, sort_list_by_due_date
from my_settings import LIST_IDS_TO_SORT


def main():
    logger.info('Sorting lists...')

    for sort_list_id in LIST_IDS_TO_SORT:
        sort_list_by_due_date(sort_list_id)
    logger.info('Sorting lists complete. Finished!')


if __name__ == '__main__':
    main()
