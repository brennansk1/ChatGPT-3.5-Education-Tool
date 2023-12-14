"""
Author: Brennan Kelley
Class: CS1410 Project - Final Project
Description: This file contains the QuestionHandler class, responsible for handling user questions and interactions. 
It utilizes the OpenAI GPT-3 API to respond to questions, stores questions in subject-specific folders, and retrieves answers.
"""
import requests
import os
import time

class QuestionHandler:
    def __init__(self, api_key, subject):
        self.api_key = api_key
        self.subject = subject
        self.question_folder = os.path.join("questions", subject)

        # Create the questions folder if it doesn't exist
        if not os.path.exists(self.question_folder):
            os.makedirs(self.question_folder)

    def askForQuestions(self):
        return "What is your question?"

    def answerQuestion(self, question):
        if question.lower() == "done":
            return "You have no more questions. Goodbye!"

        answer = self.get_chat_response(question)
        self.save_question(question, answer)
        return answer

    def get_chat_response(self, user_message):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'system', 'content': 'You answers questions in a precise way'},
                         {'role': 'user', 'content': user_message}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        else:
            error_message = f"Error in API request: {response.status_code}, {response.text}"
            return error_message

    def save_question(self, question, answer):
        # Generate a unique filename based on the subject and the current timestamp
        timestamp = str(time.time()).replace('.', '_')
        filename = os.path.join(self.question_folder, f"{self.subject}_question_{timestamp}.txt")

        # Save the question and answer to a text file
        with open(filename, 'w') as file:
            file.write(f"Question: {question}\n")
            file.write(f"Answer: {answer}\n")


