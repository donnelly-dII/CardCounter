#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:51:32 2018

@author: David Donnelly II

###############################################################################
This is an interactive card counting assistor. It'll track a game of Blackjack
hand by hand and keep a running count. After each hand, a true count will be 
returned so as to help the player make more educated betting decisions
 
The following are the card keys the user enters for each type of card:  
    
    1- Ace 
    2- 2
    3- 3
    4- 4
    5- 5
    6- 6
    7- 7
    8- 8
    9- 9
    0- 10
    j- jack 
    q- queen 
    k- king
    
Control keys:
    
    s- stick
    x- exit
    n- new hand

###############################################################################
"""

import math


def Main():
    """
    Executes the program upon running the python file
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    """
    
    print("Welcome to the Card Counter. To play, first enter the number of players (including yourself) and enter what position you are out of the players. ")
    
    #Retrieve number of players
    n = raw_input("How many other players are there?")
    check = False
    while check!=True:
        try:
            numPlayers = int(n)
            check = True
        except ValueError:
            n = raw_input("Please enter an integer number of players")
            
    #Retrieve number of players
    d = raw_input("How many decks in a shoe?")
    check = False
    while check!=True:
        try:
            numDecks = int(d)
            check = True
        except ValueError:
            d = raw_input("Please enter an integer number of decks")
            
    #Ask to begin
    startCheck = raw_input('Ready to begin game? (y/n)')
    if startCheck =='y':
        Handle = GameHandler(numPlayers,numDecks)
        Handle.PlayGame()

class GameHandler():
    
    def __init__(self, n, d):
        self.NumPlayers = n
        self.RunningCount = 0
        self.DecksinShoe = d
        self.CardCount = 0;
        self.TrueCount = 0;
        
    def get_RunCount(self):
        return self.RunningCount
    
    def get_cardCount(self):
        return self.CardCount
        
        
    def PlayGame(self):
        """
        Begins a Game of BlackJack. Individual Hands will be continuously played
        while the Running Count is tracked. The true count is returned at the 
        end of each hand, and the game will continue until the user terminates 
        the program. 
        
        Parameters
        ----------
        None
        
        Returns
        ----------
        None
        """
        
        KeepPlaying = True
        while KeepPlaying and math.floor(self.CardCount/52) < self.DecksinShoe: 
            self.PlayHand()
            self.ReportIntel()
            inpt = raw_input('Keep Playing? x-exit / n-new hand')
            if inpt == 'x':
                KeepPlaying =False
        
        if(KeepPlaying):
            print('NEW SHOE, UPDATED TRUE COUNT')
            newHandle = GameHandler(self.NumPlayers, self.DecksinShoe)
            newHandle.PlayGame()
        
        print('Game Concluded')
        
            
        
    def PlayHand(self):
        """
          Plays a single hand of blackjack. This fucntion updates the information 
          in the running count
        
        Parameters
        ----------
        None
        
        Returns
        ----------
        None
        """
        newHand = PlayHandle(self.NumPlayers, self.RunningCount)
        newHand.Deal()
        newHand.Play()
        newHand.DealerCards()
        self.RunningCount = newHand.Running_Count_Calc(self.RunningCount)
        #Update the deck info
        self.CardCount = self.CardCount + newHand.GetCardCount()
        print(self.CardCount)
        
        
    def ReportIntel(self):
        #Find the number of decks used
        DecksRemaining = (self.DecksinShoe - round(self.CardCount/52))
        TrueCount = self.RunningCount/DecksRemaining
        print 'The Current True Count is ', TrueCount
        
             

class PlayHandle:
    
    
    def __init__(self, n, runCount):
        self.DealtList = []
        self.PlayerCount = n
        self.RunningCount = runCount
        self.CardCount = 0
        self.DealerCount = 0
        
    def Deal(self):
        """
        Executes the Deal portion of a hand. The user is requested to input
        the two dealt cards for each player. Each hand is then stored as a 
        string of 2 characters in an array. 
    
        ----------
        Parameters
        ----------
        None
        ----------
        Returns
        ----------
        A list of each player's dealt cards stored in the DealtList
        """
    
        for ii in range(1,self.PlayerCount+1):
            hand = raw_input("Input dealt hand for player " + str(ii) + '  ')
            handCheck = False
            while handCheck == False:
                if(len(hand) == 2):
                    handCheck = True
                else:
                    hand = raw_input("INCORRECT: Only enter two cards")
                
                self.DealtList.append(hand)
        
    
    def Play(self):
        """
        Executes the playing of a single hand of black jack. This function is 
        called after the cards are dealt and the Deal function is called. This
        tracks the cards added through players hitting. All the hands are 
        updated in the DealtList to include additional cards.
    
        Parameters
        ----------
        None
        
        Returns
        ----------
        None
        """
        for ii in range(1,self.PlayerCount+1):
            self.CardCount += 1
            hit=raw_input("NewCard for Player " + str(ii) + ".  Hit s for stick  ")
            while(hit != "s"):
                if(len(hit) > 1):
                    hit = raw_input("INCORRECT INPUT: retry")
                self.DealtList[ii] = self.DealtList[ii] + hit
                self.CardCount += 1
                hit=raw_input("NewCard for Player " + str(ii) + ".  Hit s for stick  ")
        
    def DealerCards(self):
        weight = 0
        hand = raw_input("Input Dealer hand")
        for ch in hand:
            weight += ZenCounting(ch)
        self.DealerCount += weight
        self.CardCount += len(hand)
    
    def Calc_Card_Weight(self, index):
        """
        Calculates the weight of a single final hand
        
        Parameters
        ----------
        index (int) : the index in DealtList of the hand we should calcualte
        
        Returns
        ----------
        weight (int) : the weight of the hand at index spot in DealtList
        """
        
        weight = 0
        for ch in self.DealtList[index]:
            weight += ZenCounting(ch)
        return weight
    
    def Running_Count_Calc(self, runCount):
        """
        Executes the program upon running the python file
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        RunningCount (int) : The current Running Count of the game
        """
        for ii in range(0,self.PlayerCount):
            runCount += self.Calc_Card_Weight(ii)
        return runCount + self.DealerCount
    
    def get_RunningCount(self):
        return self.RunningCount
    def GetCardCount(self):
        return self.CardCount
        
       
def ZenCounting(card):
    if card =='2' or card == '3' or card =='7':
        return 1
    elif card =='4' or card == '5' or card == '6':
        return 2
    elif card == '8' or card == '9':
        return 0
    elif card =='1':
        return -1
    else:
        return -2
        
    
    
        
        
        
        
        

Main()