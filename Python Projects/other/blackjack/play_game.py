"""
Oct, 2022
A project built for one of the Python courses I took at USU. This was my first experience with Python Classes, and object-oriented
programming in general. As the name suggests, the program allows the user to play a very simple version of Blackjack.
"""

from DeckOfCards import DeckOfCards
import random

# logic to generate dealer score and compare it to the user's and return result
def calculate_score():
    dealer_score = random.randint(17,23)
    if dealer_score > 21:
        return "\nDealer busts with " + str(dealer_score) + ". You win."
    elif score > dealer_score:
        return "\nDealer score: " + str(dealer_score) + ". You win!"
    else:
        return "\nDealer score: " + str(dealer_score) + ". You lose."

# welcome message
print("Welcome to Jason's Blackjack. May the odds be ever in your favor.")
print()

# generate a deck using DeckOfCards class
deck = DeckOfCards()

# print deck
print("Deck:")
deck.print_deck()

# create replay loop
replay = 'y'
while replay == 'y':
    # shuffle
    deck.shuffle_deck()
    
    # reprint shuffled deck
    print("Deck Size:", len(deck.deck))
    print("Shuffled Deck:")
    deck.print_deck()
    print()
    
    # deal two cards to the user
    card_number = 1
    card = deck.get_card()
    print("Card number", card_number, "is: ", card)
    card_number += 1
    card2 = deck.get_card()
    print("Card number", card_number, "is: ", card2)
    card_number +=1
    print()
    
    score = 0
    # calculate the user's hand score
    score += card.val
    score += card2.val
    print("Your score is: ", score)
    
    
    # ask user if they would like a "hit" (another card)
    hit = input("would you like a hit? (y/n):")
    
    # continue to give cards and add new value to score until user stops
    while hit == 'y':
        next_card = deck.get_card()
        print()
        print("Card number", card_number, "is: ", next_card)
        card_number += 1
        score += next_card.val
        print("new score: ", score)
        print()
        if score <= 21:
            hit = input("would you like a hit? (y/n):")
        else: # if score becomes greater than 21, exit loop and print bust message to user
            hit = 'bust'
            print("bust. you lose.")
            
    # if user did not bust, calculate score and print result
    if hit != 'bust':
        print(calculate_score())
        
    replay = input("play again? (y/n):")
    print()
    
print("Thanks for playing.")
