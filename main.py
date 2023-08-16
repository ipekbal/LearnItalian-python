from kivy.app import App #base for kivy application
from kivy.core.window import Window #to create windows in the app
from kivy.uix.screenmanager import ScreenManager, Screen #to manage transitions between windows
from kivy.core.text import LabelBase

from kivy.properties import StringProperty
from phrases import phrases #imports the italian phrases dictionary from the python file

import sqlite3
from random import choice

conn = sqlite3.connect('tests.db') #connecting to the test database
c = conn.cursor() #cursor to execute sql queries


# test to see if the table is working
c.execute("""SELECT * FROM test;""")

conn.commit()

rows = c.fetchall()

for row in rows:
    print(row)


Window.clearcolor = (1,1,1,1)
LabelBase.register(name= "Quicksand",
                   fn_regular= '/Users/ipekbal/PycharmProjects/kivy-thelab/venv/Quicksand-Regular.otf'
)

class MainMenu(Screen):
    pass

class TopicMenu(Screen):

    pass

class Instructions(Screen):
    def __init__(self, **kwargs):
        super(Instructions, self).__init__(**kwargs)
        self.instructions = """Instructions:
               Left mouse click/tap on the buttons in order to navigate the app.
               You can revise by using the flashcards.
                Select flashcards on the topic menu.
                Click the rounded button in order to flip the cards, 
                    and use the arrows below the flashcard to change the flashcard.
               You can test your knowledge by doing tests.
                Select tests on the topic menu.
                Click the button you believe has the right answer.
                If the button turns green, congrats! You have got the right answer.
                If the button turns red, unlucky, you have got the wrong answer."""


class Flashcards(Screen):
    front_card_label = StringProperty("Basic Phrases") #placeholder
    back_card_label = StringProperty("Flashcards") #placeholder

    italian_phrase_list = list(phrases.keys())
    i = 0
    def __init__(self, **kwargs):
        super(Flashcards, self).__init__(**kwargs)


    def next_card(self):
        self.i += 1
        flashcard_number = self.i % len(self.italian_phrase_list) #to go back to the start of the list
        print(self.i)
        current_card = self.italian_phrase_list[flashcard_number]
        self.front_card_label = current_card
        self.back_card_label = phrases[current_card]

        print(current_card)

    def previous_card(self):
        self.i -= 1
        flashcard_number = self.i % len(self.italian_phrase_list)  # to go back to the start of the list
        print(self.i)
        current_card = self.italian_phrase_list[flashcard_number]
        self.front_card_label = current_card
        self.back_card_label = phrases[current_card]

        print(current_card)


class Grammar(Screen):
    pass

class Tests(Screen):
    def __init__(self, **kwargs):
        super(Tests, self).__init__(**kwargs)
        self.answer = ''
        self.generate_test()


    def generate_test(self):
        # selects the least asked word from the test table
        self.chosen_question = c.execute("""SELECT italian_word, english_word 
                    FROM test 
                    ORDER BY times_asked ASC
                    LIMIT 1;""")
        conn.commit()

        self.chosen_question = self.chosen_question.fetchall()[0] #returns the selected italian word and english word as a tuple
        print(self.chosen_question)
        self.question = self.chosen_question[0] #assigns the italian word to the question
        self.answer = self.chosen_question[1] #assigns the english word to answer

        print("chosen question: ", self.question)
        print(self.answer)

        # incremenets the times_asked column of the word that is being asked
        c.execute("""UPDATE test SET times_asked = times_asked + 1 WHERE italian_word = '%s'""" %self.question)
        conn.commit()

        # testing if the times_asked column has been updated
        c.execute("""SELECT * FROM test;""")

        conn.commit()

        rows = c.fetchall()

        for row in rows:
            print(row)
        # Randomly selects 3 english words for the multiple choice
        self.choices = c.execute("""SELECT english_word 
                            FROM test 
                            WHERE italian_word != '%s'
                            ORDER BY RANDOM()
                            LIMIT 3;""" %(self.question))
        conn.commit()

        self.choices = self.choices.fetchall()  # turns the selected words to an array

        self.multiple_choice = [self.answer] # initially only value in the multiple choice is the answer

        for i in range(3):
            # takes the random words chosen from the db from the tuple and adds them to the multiple_choice list
            self.multiple_choice.append(self.choices[i][0])

        # the right choice will be assigned to this variable when all the choices have been randomly assigned
        self.right_choice = ''

        # assigns choices randomly using the assign_random_words function
        self.choice_a = 'A: ' + self.assign_random_words(self.multiple_choice)
        self.choice_b = 'B: ' + self.assign_random_words(self.multiple_choice)
        self.choice_c = 'C: ' + self.assign_random_words(self.multiple_choice)
        self.choice_d = 'D: ' + self.assign_random_words(self.multiple_choice)
        print(self.ids.keys())
        try:
            # Set choices
            self.ids['button_a'].text = self.choice_a
            self.ids['button_b'].text = self.choice_b
            self.ids['button_c'].text = self.choice_c
            self.ids['button_d'].text = self.choice_d

            # reset colors
            self.ids['button_a'].background_color = (0, 172/255, 231/255, 1)
            self.ids['button_b'].background_color = (0, 172 / 255, 231 / 255, 1)
            self.ids['button_c'].background_color = (0, 172 / 255, 231 / 255, 1)
            self.ids['button_d'].background_color = (0, 172 / 255, 231 / 255, 1)

            self.ids['question'].text = self.question
        except:
            pass

        print(self.choice_a, self.choice_b, self.choice_c, self.choice_d)


    # chooses random english word to assign to a choice and removes it from the original list
    def assign_random_words(self, word_list):
        self.random_choice = choice(word_list) # chooses random english word from the list
        word_list.remove(self.random_choice) # removes the random english word from the list
        print(word_list) # testing if the function works
        return self.random_choice

    # checks the answer when button is pressed
    def check_answer(self, text):
        # if answer is right button turns green
        if text[3:] == self.answer:
            self.ids['button_'+ text[0].lower()].background_color = (0, 1, 0, 1)

        # if answer is wrong button turns red
        else:
            self.ids['button_'+ text[0].lower()].background_color = (1, 0, 0, 1)


class Review(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class LanguageApp(App):
    pass


LanguageApp().run()