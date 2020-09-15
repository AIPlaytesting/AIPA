# A collection of cards saved in pile
# Game flow: 
    # draw card from drawPile (an instance of Pile class) function required: draw
    # play out card and consume energy, card playing out will be moved in the discardPile (an instance of Pile class) function required: addCards
# extaust pile is another thing to do // later
# other useful functions: 
    # cardsLeft: number of cards left
    # resetPile: reset pile to initial state
    # display: display all the cards in this pile

class Pile:
    def __init__(self):
        self.cards = []

    # number of cards left in pile
    # return: number 
    def cardsLeft(self):
        return len(self.cards)

    # reset pile to initial state
    def resetPile(self):
        self.cards = []

    # draw num of cards from pile
    # params: number num, number of cards that you want to draw
    # return: List res, a list of cards
    def draw(self, num):
        if self.cards == []:
            self.resetPile()
        res = []
        for _ in range(num):
            res.append(self.cards.pop())
        return res

    # extends card.
    # params: List[Card] cards, 
    # return: None
    def addCards(self, cards):
        self.cards.extend(cards)
    
    # display cards
    # return: List[Card]
    def display(self):
        return self.cards

# drawPile = Pile()
# discardPile = Pile()

# drawPile.addCards([1])
# drawPile.addCards([1,2,3])
# print(drawPile.display())

# print(drawPile.draw(2))
# print(drawPile.display())

