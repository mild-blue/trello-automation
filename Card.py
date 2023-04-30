class Card:
    def __init__(self, card_id, name, due_date, member_ids, completed):
        self.id = card_id
        self.name = name
        self.due_date = due_date
        self.member_IDs = member_ids
        self.completed = completed
