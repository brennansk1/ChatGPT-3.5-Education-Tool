"""
Author: Brennan Kelley
Class: CS1410 
Project - Final Project
Description: This file contains the EnhancedHomeworkGenerator class, which is responsible for generating customized homework assignments 
and answers based on the subject provided by the user. 
It enhances the learning experience with tailored exercises.
"""
import os
import random
import requests
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class EnhancedHomeworkGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.homework_folder = 'homework'
        self.answers_folder = 'answers'
        self.ensure_folder_exists(self.homework_folder)
        self.ensure_folder_exists(self.answers_folder)
        self.generated_questions = []

    def ensure_folder_exists(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def generateHomework(self, subject):
        homework_questions = self.createVariedQuestions(subject)
        self.generated_questions = homework_questions  # Store generated questions
        pdf_output = os.path.join(self.homework_folder, f"{subject}_Homework.pdf")
        self.create_pdf([q['text'] for q in homework_questions], pdf_output)
        return pdf_output

    def generateHomeworkAnswers(self, subject):
        answers = self.create_homework_answers(subject)
        pdf_output = os.path.join(self.answers_folder, f"{subject}_Answers.pdf")
        self.create_pdf([a['text'] for a in answers], pdf_output)
        return pdf_output

    def createVariedQuestions(self, subject):
        question_types = ["multiple-choice", "short answer", "true/false"]
        questions = []
        for _ in range(8):
            question_type = random.choice(question_types)
            question_prompt = f"Create a {question_type} question about {subject}."
            question_text = self.get_chat_response(question_prompt)
            questions.append({"text": question_text, "type": question_type})
        return questions

    def create_homework_answers(self, subject):
        answers = []
        for question in self.generated_questions:
            question_text = question['text']
            question_type = question['type']
            answer_prompt = f"Provide a short concise answer for the following {question_type} question about {subject}:\n{question_text}"
            answer_text = self.get_chat_response(answer_prompt)
            answers.append({"text": answer_text, "type": "answer"})
        return answers

    def create_pdf(self, contents, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        margin = 72
        font_size = 12
        font_name = "Times-Roman"

        text_object = c.beginText(margin, letter[1] - margin)
        text_object.setFont(font_name, font_size)

        for content in contents:
            for line in textwrap.wrap(content, width=80):
                if text_object.getY() - font_size < margin:
                    c.drawText(text_object)
                    c.showPage()
                    text_object = c.beginText(margin, letter[1] - margin)
                    text_object.setFont(font_name, font_size)
                text_object.textLine(line)
            text_object.textLine('')  # Add a blank line after each line

        c.drawText(text_object)
        c.save()

    def get_chat_response(self, user_message):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are a homework question and answer generator.'},
                {'role': 'user', 'content': user_message}
            ]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        else:
            error_message = f"Error in API request: {response.status_code}, {response.text}"
            return error_message
