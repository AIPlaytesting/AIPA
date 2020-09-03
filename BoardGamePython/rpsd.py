import random

# one card
class Card():
    def __init__(self, suit):
        # from 0 to 3. 0: Rock, 1: Paper, 2: Scissors, 3: Dragon
        self.suit = suit
    
    # show card string
    def getString(self):
        cards_str = ['Rock', 'Paper', 'Scissors', 'Dragon']
        return cards_str[self.suit]

# collections of cards on a player's hand
class Hand():
    def __init__(self, cards):
        self.hand = cards

class Deck():
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for _ in range(13):
                self.cards.append(Card(suit))
        random.shuffle(self.cards)

    # number of cards left in deck
    def cardsLeft(self):
        return len(self.cards)

    # draw 1 card from deck
    def draw(self):
        return None if (self.cards == []) else self.cards.pop()

    # draw 4 cards from deck
    def drawFour(self):
        if self.cards == []:
            return None
        res = []
        for _ in range(4):
            res.append(self.cards.pop())
        return res

# the game class
class RPSD():
    def play(self):
        self.handsWon = 0
        self.handsTie = 0
        self.handsLose = 0
        self.handsPlayed = 0
        self.deck = Deck()
        self.printWelcomeMessage()
        while True:
            self.playTurn()
            if (not self.askYesOrNo('Keep playing?')):
                break
        self.printGoodbyeMessage()
    
    def printWelcomeMessage(self):
        print('''
Welcome to Rock, Paper, Scissors, Dragon(RPSD) game.
Rule:
Rock < Paper, Paper < Scissors, Scissors < Rock, Dragon wins all the others
If each player plays the same card, then tie.
Good luck!
''')

    def printGoodbyeMessage(self):
        print(f'Final score: {self.handsWon} out of {self.handsPlayed} hands.')
        print('Goodbye!')

    def askYesOrNo(self, prompt):
        while True:
            result = input(prompt + ' [y]es or [n]o --> ').lower()
            if (result == 'y'): return True
            elif (result == 'n'): return False
            else: print('Please enter y or n!')

    def getHandString(self, hand):
        return ', '.join([card.getString() for card in hand])

    def whoWin(self, card1, card2):
        if card1.getString() == 'Rock':
            if card2.getString() == 'Rock': # tie
                return 2
            elif card2.getString() == 'Paper' or card2.getString() == 'Dragon': # lose
                return 1
            else:
                return 0 # win
        elif card1.getString() == 'Paper':
            if card2.getString() == 'Paper':
                return 2
            elif card2.getString() == 'Scissors' or card2.getString() == 'Dragon':
                return 1
            else:
                return 0
        elif card1.getString() == 'Scissors':
            if card2.getString() == 'Scissors':
                return 2
            elif card2.getString() == 'Rock' or card2.getString() == 'Dragon':
                return 1
            else:
                return 0
        else: # dragon
            if card2.getString() == 'Dragon':
                return 2
            else:
                return 0
        return -1

    def playTurn(self):
        # print(f'You have won {self.handsWon} out of {self.handsPlayed} hands.')
        self.handsPlayed += 1
        if (self.deck.cardsLeft() < 18):
            print('\n*** New Deck! ***\n')
            self.deck = Deck()
        # draw cards stage
        p1Hand = self.deck.drawFour()
        p2Hand = self.deck.drawFour()
        print(f'player1 hand: {self.getHandString(p1Hand)}')
        print(f'player2 hand: {self.getHandString(p2Hand)}')
        # play card stage, randomly choose 1 card to play
        p1rand = random.randint(0, 3)
        p2rand = random.randint(0, 3)
        p1PlayCard = p1Hand[p1rand]
        p2PlayCard = p2Hand[p2rand]
        print(f'player1 decides to play {p1rand}th card: {p1PlayCard.getString()}')
        print(f'player2 decides to play {p2rand}th card: {p2PlayCard.getString()}')
        # decide and record who wins
        whowin = self.whoWin(p1PlayCard, p2PlayCard) # p1 wins: 0, p2 wins: 1, tie: 2
        if whowin == 0:
            self.handsWon += 1
            print('player 1 wins in this round.')
        elif whowin == 1:
            self.handsLose += 1
            print('player 2 wins in this round.')
        else:
            self.handsTie += 1
            print('tie in this round')
        print(f'player1 statistics --> win: {self.handsWon}, lose: {self.handsLose}, tie: {self.handsTie}, total rounds: {self.handsPlayed}')


game = RPSD()
game.play()