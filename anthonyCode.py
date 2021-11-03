"""
Author: Andy Wicks
Code can be found at: https://lyw4.life/Resources/python.php
Date started: Mon,  19 Oct 2020
Version: 0.0
Purposes:
    - To use the grid geometry to lay out widgets.
    Reference: https://tkdocs.com/tutorial/grid.html
"""
import tkinter as tk             # This has all the code for GUIs.
import tkinter.font as font      # This lets us use different fonts.
from tkinter import messagebox   # This gives access to message boxes.


def center_window_on_screen():
    """
    This centres the window when it is not maximised.  It
    uses the screen and window height and width variables
    defined in the program below.
    :return: Nothing
    """
    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))


def calculate():
    """
    This method is used to calculate the
    average score across the five quizzes.
    The result is returned in a dialog box.
    :return: Nothing
    """
    # Set the total to 0 at the start.
    total = 0
    # Now, go through each entry widget ...
    for entry in ent_dict:
        # Get whatever is in that entry widget
        temp = ent_dict[entry].get()
        # If the entry is numeric ...
        if temp.isnumeric():
            # Turn the entry into a number.
            score = int(temp)
            # Add the score to the total
            total += score

    # Display a message box which shows the average score.
    messagebox.showinfo('Average Score', 'Average = ' + str(total / 5))


def change_to_work():
    """
    This function swaps from the quiz
    frame to the work frame.
    :return: Nothing
    """
    quiz_frame.forget()
    work_frame.pack(fill='both', expand=1)


def change_to_quiz():
    """
    This function swaps from the work
    frame to the quiz frame.
    :return: Nothing
    """
    quiz_frame.pack(fill='both', expand=1)
    work_frame.forget()


# Now we get to the program itself:-
# Let's set up the window ...
root = tk.Tk()
root.title("My Work - Using Grid Layout")
root.configure(bg='lightyellow')
# Set the icon used for your program
# root.iconphoto(True,
#                tk.PhotoImage(file='info.png'))

width, height = 500, 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_window_on_screen()

# Here, we create two frames of which only
# one will be visible at a time.
quiz_frame = tk.Frame(root)
work_frame = tk.Frame(root)

# Let's create the fonts that we need.
font_large = font.Font(family='Georgia',
                       size='24',
                       weight='bold')
font_small = font.Font(family='Georgia',
                       size='12')

# # The widgets needed for the quiz frame.
# # First, let's display te logo.
# img_logo = tk.PhotoImage(file='logo.png')
lbl_logo_quiz = tk.Label(quiz_frame,
                          text='hey')

# Next, comes the heading for this frame.
lbl_heading_quiz = tk.Label(quiz_frame,
                            text='Weekly Quiz Scores',
                            font=font_large)
lbl_logo_quiz.grid(column=0, row=0, columnspan=5)
lbl_heading_quiz.grid(column=0, row=1, columnspan=5)

# We now create a dictionary of label and entry widgets.
# The key will be the number of the week and the value
# will be the widget.  Yes, a dictionary can contain widgets!
lbl_dict = dict()
ent_dict = dict()

# The next step is to create and display the labels and
# entry widgets for each week.
for week in range(3, 8):
    # This creates the text for the labels.
    label_text = 'Week', week
    # col is the column in the grid where each widget
    # will appear.
    col = week - 3
    # The next commands create and display the labels.
    lbl_dict[week] = tk.Label(quiz_frame,
                              text=label_text,
                              font=font_small)
    lbl_dict[week].grid(column=col, row=2, sticky='S')
    # These two commands create and display the entry widgets.
    ent_dict[week] = tk.Entry(quiz_frame,
                              font=font_small,
                              width=3)
    ent_dict[week].grid(column=col, row=3, sticky='N')

# We can now add the button which calculates the average.
btn_calculate_quiz = tk.Button(quiz_frame,
                               font=font_small,
                               text='Calculate',
                               command=calculate)
btn_calculate_quiz.grid(column=3, row=4)

# And finally, the button to swap between the frames.
btn_change_to_work = tk.Button(quiz_frame,
                               font=font_small,
                               text='Change',
                               command=change_to_work)
btn_change_to_work.grid(column=4, row=4)

# The widgets needed for the work frame.
# These are only being used in this example
# to show that both frames are working as
# expected.

# First the image gets added.
# lbl_logo_work = tk.Label(work_frame,
#                          text='amigio')
# lbl_logo_work.pack()

# Next, we'll add a heading.
lbl_heading_work = tk.Label(work_frame,
                            text='Work Submitted',
                            font=font_large)
lbl_heading_work.pack()

# Finally, we need the button to
# swap back to the quiz frame.
btn_change_to_quiz = tk.Button(work_frame,
                               text='Change',
                               command=change_to_quiz)
btn_change_to_quiz.pack()

# Only the quiz frame needs to be shown
# when the program starts.  The work frame
# will only appear when the Change button
# is clicked.
quiz_frame.pack(fill='both', expand=1)

root.mainloop()