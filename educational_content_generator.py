"""
Author: Brennan Kelley
Class: CS1410 
Project - Final Project
Description: This file defines the EducationalContentGenerator class, responsible for generating educational lecture content based on user-specified subjects. 
It interacts with external sources to create informative lectures.
"""
import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

class EducationalContentGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.lecture_folder = 'lectures'
        self.ensure_folder_exists(self.lecture_folder)

    def ensure_folder_exists(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def generateLecture(self, subject):
        lecture_content = self.get_chat_response(f"Give a lengthy summary of {subject}")
        pdf_output = os.path.join(self.lecture_folder, f"{subject}_Lecture.pdf")
        self.create_pdf(lecture_content, pdf_output)
        return pdf_output

    def create_pdf(self, content, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        margin = 72
        font_size = 12
        font_name = "Times-Roman"

        text_object = c.beginText(margin, height - margin)
        text_object.setFont(font_name, font_size)

        wrapped_text = textwrap.wrap(content, width=80)  # Adjust wrap width as needed
        for line in wrapped_text:
            if text_object.getY() - font_size < margin:
                c.drawText(text_object)
                c.showPage()
                text_object = c.beginText(margin, height - margin)
                text_object.setFont(font_name, font_size)
            text_object.textLine(line)
            text_object.textLine('')  # Add a blank line after each line of text

        c.drawText(text_object)
        c.save()



    def get_chat_response(self, user_message):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'system', 'content': 'You are a subject summarizer, that summarizes information on a subject provided.'},
                         {'role': 'user', 'content': user_message}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        else:
            error_message = f"Error in API request: {response.status_code}, {response.text}"
            return error_message


