class Card:
    def __init__(self, card_id, due_date, member_ids, completed, name):
        self.id = card_id
        self.due_date = due_date
        self.member_IDs = member_ids
        self.completed = completed
        self.name = name
