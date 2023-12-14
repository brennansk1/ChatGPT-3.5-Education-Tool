"""
Author: Brennan Kelley
Class: CS1410 
Project - Final Project
Description: The main.py file serves as the entry point for the Educational Application. 
It initializes the application, interacts with the user using a text-based interface, 
and coordinates the generation of educational content, questions, and homework.

Notes: There was one errors I couldn't fix with the UI. When you ask it a questions the question do you have any other questions, 
it will appear in the middle of the generated text.
"""
import curses
import time  
from educational_content_generator import EducationalContentGenerator
from question_handler import QuestionHandler
from enhanced_homework_generator import EnhancedHomeworkGenerator

class MainApplication:
    def __init__(self, api_key):
        self.api_key = api_key
        self.content_generator = EducationalContentGenerator(api_key)
        self.question_handler = None
        self.homework_generator = EnhancedHomeworkGenerator(api_key)

    def initialize_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Define color pair 1 (white background, black text)

    def run(self):
        stdscr = curses.initscr()
        curses.curs_set(0)
        stdscr.clear()

        # Initialize colors
        self.initialize_colors()

        # Use color pair 1 (white text on black background)
        stdscr.attron(curses.color_pair(1))

        stdscr.addstr(0, 0, "Welcome to the Educational Application!", curses.A_BOLD)
        stdscr.refresh()

        stdscr.addstr(2, 0, "Enter the subject you would like to learn about:")
        stdscr.refresh()

        curses.echo()
        subject = stdscr.getstr(3, 0).decode('utf-8')
        curses.noecho()

        stdscr.addstr(4, 0, "Generating lecture...")
        stdscr.refresh()

        lecture_pdf = self.content_generator.generateLecture(subject)
        stdscr.addstr(5, 0, f"Lecture saved as: {lecture_pdf}")
        stdscr.refresh()

        time.sleep(5)  # Add a 5-second delay

        stdscr.addstr(7, 0, "Do you have any questions? (yes/no):")
        stdscr.refresh()
        question_prompt = stdscr.getstr(8, 0).decode('utf-8')
        stdscr.addstr(9, 0, f"Your response: {question_prompt}")  # Display user's response
        stdscr.refresh()

        if question_prompt.lower() == 'yes':
            stdscr.addstr(10, 0, "Please enter the subject again:")
            stdscr.refresh()
            curses.echo()
            subject = stdscr.getstr(11, 0).decode('utf-8')
            curses.noecho()

            self.question_handler = QuestionHandler(self.api_key, subject)
            while True:
                question = self.question_handler.askForQuestions()
                stdscr.addstr(13, 0, question)
                stdscr.refresh()

                curses.echo()
                user_input = stdscr.getstr(14, 0).decode('utf-8')
                curses.noecho()

                if user_input.lower() == 'done':
                    break

                stdscr.addstr(15, 0, "Loading...")
                stdscr.refresh()

                answer = self.question_handler.answerQuestion(user_input)
                stdscr.addstr(16, 0, f"Answer: {answer}")
                stdscr.refresh()

                time.sleep(3)  # Add a 5-second delay

                stdscr.addstr(18, 0, "Do you have any more questions? (yes/no):")
                stdscr.refresh()
                more_questions_prompt = stdscr.getstr(19, 0).decode('utf-8')
                stdscr.addstr(20, 0, f"Your response: {more_questions_prompt}")  # Display user's response
                stdscr.refresh()

                if more_questions_prompt.lower() == 'no':
                    break

        stdscr.addstr(21, 0, "Would you like homework generated? (yes/no):")
        stdscr.refresh()
        homework_prompt = stdscr.getstr(22, 0).decode('utf-8')
        stdscr.addstr(23, 0, f"Your response: {homework_prompt}")  # Display user's response
        stdscr.refresh()

        if homework_prompt.lower() == 'yes':
            stdscr.addstr(24, 0, "Generating homework...")
            stdscr.refresh()

            homework_pdf = self.homework_generator.generateHomework(subject)
            stdscr.addstr(25, 0, f"Homework saved as: {homework_pdf}")
            stdscr.refresh()

            stdscr.addstr(26, 0, "Generating answers...")
            stdscr.refresh()

            answers_pdf = self.homework_generator.generateHomeworkAnswers(subject)
            stdscr.addstr(27, 0, f"Answers saved as: {answers_pdf}")
            stdscr.refresh()

        stdscr.addstr(29, 0, "Press any key to exit.")
        stdscr.refresh()
        stdscr.getch()
        curses.endwin()

if __name__ == "__main__":
    api_key = "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"
    app = MainApplication(api_key)
    app.run()
