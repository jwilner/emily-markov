from flask import Flask, render_template
from random import choice
import pickle
from pymarkov.pymarkov import MarkovChainGenerator
import re

app = Flask('joeLy')

file_name = 'emily-dick.txt'
real_poem_file = 'new_emily.txt'
min_words = 15
fake_line_length = 30
line_break = '\r\n'

emily_pic = 'Emily_Dickinson.gif'
markov_pic = 'Andrei_Markov.jpg'

word_counter = re.compile(r'\b\S+\b')
punc_replacer = re.compile(r'\s(?=[:,;\'".\s?!])|\'\'|\`\`')
line_breaker = re.compile(r'\s(?=[A-Z])')

with open(real_poem_file, 'r') as f:
    all_poems = pickle.load(f)

markov = MarkovChainGenerator('emily-dick.txt')


def binary_random():
    return choice([True, False])


def get_fake():
    '''business logic for generating fake poem. Returns a tuple of 0 and the
    generated material.'''

    while True:
        poem = markov.generate_sentence()
        if len(word_counter.findall(poem)) >= min_words:
            break

    return line_breaker.sub(lambda x: '\r\n  ' if binary_random() else '\r\n',
                            punc_replacer.sub('', poem))


def get_real():
    '''Picks a random poem from the poems.'''
    return line_break.join(choice(all_poems))


@app.route('/', methods=['GET', 'POST'])
def front_page():
    '''Show a real-or-fake Emily Dickinson poem, provide a button to guess,
    on right or wrong show happy or sad Emily.'''

    real = binary_random()
    poem = get_real() if real else get_fake()
    pic = 'static/img/' + (emily_pic if real else markov_pic)
    return render_template('index.html', real=real, poem=poem, pic=pic)

if __name__ == '__main__':
    app.run(debug=True)
