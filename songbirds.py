from pygame import midi
from time import sleep
import logging
import random

midi.init()
logging.basicConfig(level=logging.DEBUG)

sample_1 = "Hi @CodeNewbies my eyes have very recently been opened to the world of programming. I am a total novice. Do you have any advice in where is a good place to start? Or can advise me generally about the world of coding?"
sample_2 = "ROLL WITH IT: Palestinian women in Gaza are learning to skateboard. This is thanks to an Italian cultural exchange group that hopes to help link Gaza to the rest of the world."
sample_3 = "what do you call cheese that isn't yours? Nacho Cheese."

def select_MIDI_out():
    """ Select and appropriate midi device"""
    midi_count =  midi.get_count()
    avail_devices = [midi.get_device_info(i) for i in range(midi_count)]
    print("Please select a MIDI device by selecting appropriate number")
    for num, device in enumerate(avail_devices):
        print("{}. {}".format(num, device))
    midi_choice = input("device id: ")
    return int(midi_choice)

print("welcome to the tweet songifier")
midi_out = select_MIDI_out()
player = midi.Output(midi_out)
player.set_instrument(0)
main_channel = 0

chord_prog = [48]
song_key = chord_prog[0]

# Letters are arranged by frequency of use in the english language
# Vowels are separated to make chords while consonants make melodic notes
vowels = { #Vowel linked to major aspects of scale degrees based on root note to create more pleasing chords
    'e':0,
    'a':7,
    'i':5,
    'o':9,
    'u':11,
    }
consonants = { # consonants will be played as melodic notes
    'r':2,
    't':4,
    'n':5,
    's':7,
    'l':9,
    'c':11,
    'd':12,
    'p':2,
    'm':4,
    'h':5,
    'g':7,
    'b':9,
    'f':11,
    'y':12,
    'w':1,
    'k':3,
    'v':5,
    'x':6,
    'z':8,
    'j':9,
    'q':11
    }

def play(chord, notes, length, channel):
    """ Plays a chord (list) and group of notes (list) for desired length (int/float) on specific MIDI channel(int 0-15)"""
    for note in chord:    
        player.note_on(note, random.randint(0, 100), channel)
#         sleep(random.random())
        logging.debug("playing chord {}".format(chord))
    for note in notes:
        logging.debug('playing note: {}'.format(note))
        player.note_on(note, random.randint(0,110), channel)
        sleep(1*random.randint(1,2)/len(notes))
    sleep(random.random()/2)
    
    sleep(random.randint(0,1))
    for note in chord:
        player.note_off(note, 127, channel)
    for note in notes:
        player.note_off(note, 127, channel)

def play_tweet(tweet):
    """divides text/tweets into words, vowels become chords and consonants become melodic notes, then calls the play function"""
    word_tweet = tweet.lower().split(' ')
    logging.debug(word_tweet)
    curr_measure = 0
    for curr_word in word_tweet:
        root_note = chord_prog[curr_measure]
        vowel_count = 0
        consonant_count = 0
        curr_chord = set()
        curr_notes = []
        for letter in curr_word:
            if letter in vowels:
                vowel_count = vowel_count + 1
                curr_chord.add(root_note + vowels[letter])
            elif letter in consonants:
                consonant_count = consonant_count + 1
                curr_notes.append(song_key + consonants[letter] + 12)
            else:
                logging.debug("Invalid Char")
                continue
        if len(curr_chord) > 0 and len(curr_chord) < 3:
            curr_chord.add(root_note)
        chord_length = len(curr_word) - vowel_count
        logging.debug("current word: {}".format(curr_word))
        logging.debug("curr notes: {}".format(curr_notes))
        logging.debug("curr chord: {}".format(curr_chord))
        play(curr_chord, curr_notes, chord_length, main_channel)
        if curr_measure < len(chord_prog) -1:
            curr_measure =  curr_measure + 1
        else:
            curr_measure = 0
    sleep(3)

def main():
    """ Main program, determines if user would like to input custom text or a hear a sample tweet"""
    while True:
        print("Would you like to enter a custom tweet or hear a sample?")
        choice = input("Enter 1 for custom, enter 2 for sample: ")
        if choice == '1':
            custom_tweet = input("Please enter your tweet here: ")
            play_tweet(custom_tweet)
        elif choice == '2':
            sample_tweets = [sample_1, sample_2, sample_3]
            play_tweet(random.choice(sample_tweets))
    
main()
