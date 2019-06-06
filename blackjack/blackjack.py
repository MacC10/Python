import tkinter
import random


def load_images(card_images):
    suits = ["heart", "club", "diamond", "spade"]
    face_cards = ["jack", "queen", "king"]

    if tkinter.TkVersion >= 8.6:
        extension = "png"
    else:
        extension = "ppm"

    # for each suit , retrieve the image for the cards
    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))
        # next the face cards
        for card in face_cards:
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def _deal_card(frame):
    # pop the next card of the top of the deck
    next_card = deck.pop(0)
    # and add it to the back of the pack
    deck.append(next_card)
    # add the image to a label and display the label
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side="left")
    # now return the card's face value
    return next_card


def score_hand(hand):
    # Calc the total score of all cards in the list.
    # Only 1 ace can have the value 11, and this will be reduce to 1 if the hand would bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust, check if there's an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins")
    elif dealer_score > player_score:
        result_text.set("Dealer score")
    else:
        result_text.set("Draw")


# When you try to assign a new value to a global variable python creates
# a local one for the function and it shadows the global variable


def deal_player():
    player_hand.append(_deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer Wins")

    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     card_value = 11
    # player_score += card_value
    # # if we would bust, check if there is an ace and subtract 10
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer wins!")
    # print(locals())


i = 0


def initial_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def new_game():
    global i
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)
    # embedded frame to hold the card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

    result_text.set("")
    # Create a list to store the deals and players hand
    dealer_hand = []
    player_hand = []
    initial_deal()
    i += 1

    print("You had ", i,  "games")


def shuffle():
    random.shuffle(deck)


def play():
    initial_deal()
    mainWindow.mainloop()


mainWindow = tkinter.Tk()
# Set up the screen and frames for the dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background="green")
result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky="ew", columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)

# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)

# player_score = 0
# player_ace = False
player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)

# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky="w")

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

reset_button = tkinter.Button(button_frame, text="New Game", background="red", command=new_game)
reset_button.grid(row=1, column=0, columnspan=4, sticky="nesw")

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=2)

# load cards
cards = []
load_images(cards)
print(cards)
# Create a new deck of cards and shuffle them
deck = list(cards)
random.shuffle(deck)

# Create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []

if __name__ == "__main__":
    play()
# ok so moving on now the challenge and its going to be quite a simple one the challenges is to add a new button to the
# program with the text new game now the button should call a function that clears the cards from the screen it resets
#  the players and dealers hands and then starts a new game now the easiest way to clear the contents of a frame is to
#  destroy the frame and create a new one with the same name and in fact that's why the program has a player_card_frame
#  and dealer_card_frame inside the card frame itself so that's it go away and create a new button with the text new
#  game and again the functionality clear the cards from the Screen reset the player and dealers hands and then start
# a new game so pause the video go away and see if you can come up with a solution and when you're ready to see our
# version of it come back and and I'll go through that with you pause the video now.....
