import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or Stand?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object

    def __str__(self):
        ans = ""
        for i in self.cards:
            ans += str(i) + " "
        return ans # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        hand_value = 0
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for i in range(len(self.cards)):
            ranks = self.cards[i].get_rank()
            hand_value += VALUES[ranks]
        if 'A' not in self.cards:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for card in range(len(self.cards)):
            self.cards[card].draw(canvas, pos) # draw a hand on the canvas, use the draw method for cards
            pos[0] += 75
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                CardObj = Card(suit, rank)
                self.deck.append(CardObj) # create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop(0)
         # deal a card object from the deck
    
    def __str__(self):
        ans = ""
        for i in self.deck:
            ans += str(i) + " "
        return ans 	# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, my_deck, my_hand, dealer_hand, score
    my_hand = Hand()
    dealer_hand = Hand()
    my_deck = Deck()
    my_deck.shuffle()
    my_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    
    if in_play:
        score -= 1
        outcome = "You lose. New deal?"
    else:
        outcome = "Hit or Stand?"

    # your code goes here
    
    in_play = True

def hit():
    global outcome, in_play, score	# replace with your code below
 
    # if the hand is in play, hit the player
    if in_play:
        my_hand.add_card(my_deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if my_hand.get_value() > 21:
            score -= 1
            outcome = "You have busted and lost. New deal?"
            in_play = False
        
def stand():
    global outcome, in_play, score	# replace with your code below
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(my_deck.deal_card())
        
    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() > 21:
        score += 1
        outcome = "You win! New deal?"
    else: 
        if dealer_hand.get_value() >= my_hand.get_value() or my_hand.get_value() > 21:
            score -= 1
            outcome = "You lose. New deal?"
        else:
            score += 1
            outcome = "You win! New deal?"
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (50, 100), 40, "White")  
    canvas.draw_text(outcome, (300, 150), 20, "White")
    canvas.draw_text('Score : '+ str(score), (300, 200), 25, "White")  
      
    pos =[50, 300]  
    dealer_hand.draw(canvas, pos)
    canvas.draw_text("Dealer", (50, 285), 25, "White")
    canvas.draw_text("Player", (50, 435), 25, "White")
    my_hand.draw(canvas, [pos[0],pos[1] + 150])  
    if in_play:  
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (200, 350), CARD_BACK_SIZE)  
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
