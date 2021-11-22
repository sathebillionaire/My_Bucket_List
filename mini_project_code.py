from graphics import *
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def click_in_list(clickPoint, draw_items):
    item = 0
    while item < len(draw_items):
        center = draw_items[item].getAnchor()
        height = (draw_items[item].getHeight()) / 2
        width = (draw_items[item].getWidth()) / 2
        if (center.getX()) - width <= clickPoint.getX() <= (center.getX()) + width and (
                center.getY()) - height <= clickPoint.getY() <= (center.getY()) + height:
            return item
        item = item + 1
    return "Click Again"


def check_click_next(click_point, button_coords):
    p1, p2 = button_coords.getP1(), button_coords.getP2()
    width = int(p2.getX() - p1.getX())
    height = int(p2.getY() - p1.getY())
    if p1.getX() <= click_point.getX() <= p1.getX() + width and p1.getY() <= click_point.getY() <= p1.getY() + height:
        return True
    else:
        return False


def draw_next_button(window_name):
    rect = Rectangle(Point(650, 670), Point(750, 730))
    rect.draw(window_name)
    click_next = Text(Point(700, 700), "NEXT")
    click_next.draw(window_name)
    return rect


def next_button(window_name):
    next_button = draw_next_button(window_name)
    clicked_next = False
    while not clicked_next:
        click_point = window_name.getMouse()
        clicked_next = check_click_next(click_point, next_button)


def chosen_number(number):
    second_window = GraphWin("Image of My Bucket List", 800, 800)
    heading = Text(Point(400, 40), "You have chosen " +
                   str(number) + " wishes to type in!")
    heading.draw(second_window)
    next_button(second_window)
    second_window.close()


def wish_entry_window(heading):
    wish_window = GraphWin("Image of My Bucket List", 800, 800)
    wish_entry_window_heading = Text(Point(400, 40), heading)
    wish_entry_window_heading.draw(wish_window)
    text_entry = Entry(Point(400, 80), 50)
    text_entry.draw(wish_window)
    next_button(wish_window)
    wish_text = text_entry.getText()
    wish_window.close()
    return wish_text


# The 1st window
win = GraphWin("Image of My Bucket List", 800, 800)
heading = Text(Point(400, 20), "Welcome to Image of My Bucket List")
heading.draw(win)
heading = Text(Point(400, 40), "Pick a number of wishes to type in")
heading.draw(win)

# Draw three coloured moving balls up and down for the user to click one from
ball_1 = Image(Point(200, 100), "ball3.gif")
ball_2 = Image(Point(300, 100), "ball5.gif")
ball_3 = Image(Point(400, 100), "ball7.gif")
ball_1.draw(win)
ball_2.draw(win)
ball_3.draw(win)

v_movement = [0, 0, 0]
v_acceleration = + 0.9
balls_list = [ball_1, ball_2, ball_3]

wish_number_chosen = False
while wish_number_chosen is False:
    c = 0
    while c < len(balls_list):
        v_movement[c] = v_movement[c] + v_acceleration
        if balls_list[c].getAnchor().getY() >= 300:
            v_movement[c] = -v_movement[c] * 0.9
        balls_list[c].move(0, v_movement[c])
        c = c + 1
        # check which ball the user picked
    clickPoint = win.checkMouse()
    if clickPoint is not None:
        print("Clicked")
        result = click_in_list(clickPoint, balls_list)
        if type(result) == int:
            wish_number_chosen = True
        else:
            print(result)
win.close()

wish_options = [3, 5, 7]
wishes = wish_options[result]
# Display a window showing how many wishes were chosen
chosen_number(wishes)
# consecutive wish entry windows of 3, 5, or 7
x = 0
order = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th"]
wish_list = []
while x < wishes:
    heading = "What is your " + order[x] + " wish?"
    wish_list.append(wish_entry_window(heading))
    x += 1
# Display all the wishes the use typed in
display_window = GraphWin("Image of My Bucket List", 800, 800)
heading = Text(Point(400, 20), "Your wishes were:")
heading.draw(display_window)

x = 0
ycoordinates = 50
while x < len(wish_list):
    message = Text(Point(400, ycoordinates), str(x + 1) + ". " + wish_list[x])
    message.draw(display_window)
    ycoordinates += 30
    x += 1
next_button(display_window)
# extract nouns/verbs in base forms/adjectives/adverbs
nlp = spacy.load('en_core_web_sm')
wish_words = []
for wish in wish_list:
    doc = nlp(wish)
    for token in doc:
        lemma_mask = ['do', 'be', 'use', 'have', 'want', 'wish', 'go']
        if token.pos_ == 'NOUN' or token.pos_ == 'PROPN' or token.pos_ == 'VERB' or token.pos_ == 'ADJ' or token.pos_ == 'ADV':
            lemma_mask = ['do', 'be', 'use', 'have', 'want', 'wish', 'go']
            if token.lemma_ in lemma_mask:
                pass
            elif token.pos_ == 'VERB':
                wish_words.append(token.lemma_)
            else:
                wish_words.append(token.text)

# switch from list to a long string with spaces
list_words = ""
for words in wish_words:
    list_words = list_words + " " + words
display_window.close()
# second last window for image instruction
last_window = GraphWin("Image of My Bucket List", 800, 800)
heading = Text(Point(400, 20),
               "Now let's get you an image of your Bucket List! The image will pop up upon clicking Next")
heading.draw(last_window)
heading = Text(Point(400, 40),
               "Otherwise, check the folder you launched this program in and you will find the image of Your Bucket "
               "List")
heading.draw(last_window)
heading = Text(Point(400, 60),
               "Download and use it as your display picture on your wall, phone or pc to remind you of your wishes!")
heading.draw(last_window)
next_button(last_window)
last_window.close()
# Create the wordcloud object
wordcloud = WordCloud(width=480, height=480, margin=0).generate(list_words)
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.savefig('Image of My Bucket List.png')
plt.show()
