__version__ = "1.0.1"

from flask import Flask, request, jsonify
from flask_cors import CORS
from quiz_generator import QuizQuestionGenerator
import json


class QuizQuestionAPI:
    """
    QuizQuestionAPI version 1.0.1
    This class provides a RESTful API interface for the QuizQuestionGenerator.
    """

    def __init__(self, generator: QuizQuestionGenerator):
        """
        Initializes the QuizQuestionAPI class with a QuizQuestionGenerator instance.
        
        Parameters:
            generator (QuizQuestionGenerator): An instance of the QuizQuestionGenerator class.
        """
        self._generator = generator
        self._app = Flask(__name__)
        CORS(self._app)
        self._setup_routes()

    def run(self, debug: bool = True):
        """
        Runs the Flask app.
        
        Parameters:
            debug (bool): Whether to run the Flask app in debug mode.
        """
        self._app.run(debug=debug)

    def _setup_routes(self):
        """
        Sets up the Flask routes for the RESTful API.
        """
        @self._app.route('/generate_question', methods=['POST'])
        def generate_question():
            data = request.json
            learning_objective = data.get('learning_objective')
            question = self._generator.generate_questions(learning_objective)
            try:
                # Attempt to parse the question to JSON format
                question_dict = json.loads(question)
            except json.JSONDecodeError:
                # Handle the case where the JSON format is imperfect
                question_str = question.replace('\n', '').replace("'", '"')
                question_dict = json.loads(question_str)
            return jsonify(question_dict)

        @self._app.route('/current_cost', methods=['GET'])
        def current_cost():
            cost = self._generator.calculate_current_cost()
            return jsonify({'current_cost': cost})

if __name__ == '__main__':
    generator = QuizQuestionGenerator()
    api = QuizQuestionAPI(generator)
    api.run(debug=True)
