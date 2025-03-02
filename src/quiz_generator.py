__version__ = "1.0.1"

import yaml
import csv
import os
import re
from openai import OpenAI


class QuizQuestionGenerator:
    """
    QuizQuestionGenerator version 1.0.1
    This class generates quiz questions using the OpenAI API and logs the token usage.
    """

    def __init__(
            self, 
            config_file: str = "../config/config.yaml",
            csv_path: str = "../data/tokens_usage.csv",
            system_message_path: str = "../data/system_message.txt"
        ):
        """
        Initializes the QuizQuestionGenerator class with the provided config and CSV file paths.
        
        Parameters:
            config_file (str): Path to the config.yaml file.
            csv_path (str): Path to the CSV file for logging token usage.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self._config_file = os.path.abspath(
            os.path.join(current_directory, config_file)
        )
        self._csv_path = os.path.abspath(
            os.path.join(current_directory, csv_path)
        )
        self._system_message_path = os.path.abspath(
            os.path.join(current_directory, system_message_path)
        )
        self._client = OpenAI(api_key=self._load_api_key())
        self._costs_dictionary = {"gpt-4o-mini": (0.15, 0.6), "gpt-4o": (2.5, 10)}

    def generate_questions(self, learning_objective: str) -> str:
        """
        Generates a multiple-choice quiz question based on the provided learning objective.
        
        Parameters:
            learning_objective (str): The learning objective for generating the quiz question.
        
        Returns:
            str: The generated quiz question.
        """
        with open(self._system_message_path, 'r') as prompt_path:
            system_message = prompt_path.read()
        chat_completion = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": system_message,
                },
                {
                    "role": "user", 
                    "content": f"Generate a multiple-choice question based on the following learning objective: {learning_objective}"
                }
            ]
        )
        answer = chat_completion.choices[0].message.content
        self._log_tokens_usage(
            call_id=chat_completion.id,
            finish_reason=chat_completion.choices[0].finish_reason,
            model=chat_completion.model,
            service_tier=chat_completion.service_tier,
            completion_tokens=chat_completion.usage.completion_tokens,
            prompt_tokens=chat_completion.usage.prompt_tokens,
            total_tokens=chat_completion.usage.total_tokens
        )
        return answer

    def calculate_current_cost(self) -> float:
        """
        Calculates the current cost based on the token usage logged in the CSV file.
        
        Returns:
            float: The total cost based on the logged token usage.
        """
        total_cost = 0
        with open(self._csv_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model = self._extract_base_model_name(row['model'])
                prompt_tokens = int(row['prompt_tokens'])
                completion_tokens = int(row['completion_tokens'])
                if model in self._costs_dictionary:
                    prompt_cost_per_million = self._costs_dictionary[model][0]
                    completion_cost_per_million = self._costs_dictionary[model][1]
                    total_cost += (prompt_tokens * prompt_cost_per_million + completion_tokens * completion_cost_per_million) / 1e6
        return round(total_cost, 8)

    def _load_api_key(self) -> str:
        """
        Loads the OpenAI API key from the config.yaml file.
        
        Returns:
            str: The OpenAI API key.
        """
        with open(self._config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config['openai']['api_key']

    def _log_tokens_usage(self, call_id: str, finish_reason: str, model: str, service_tier: str,
                          completion_tokens: int, prompt_tokens: int, total_tokens: int):
        """
        Logs the token usage and other relevant fields to the CSV file.
        
        Parameters:
            call_id (str): The ID of the API call.
            finish_reason (str): The reason the API call finished.
            model (str): The model used for the API call.
            service_tier (str): The service tier of the API call.
            completion_tokens (int): The number of completion tokens used.
            prompt_tokens (int): The number of prompt tokens used.
            total_tokens (int): The total number of tokens used.
        """
        file_exists = os.path.isfile(self._csv_path)
        with open(self._csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['id', 'finish_reason', 'model', 'service_tier', 'completion_tokens', 'prompt_tokens', 'total_tokens'])
            writer.writerow([call_id, finish_reason, model, service_tier, completion_tokens, prompt_tokens, total_tokens])

    def _extract_base_model_name(self, model: str) -> str:
        """
        Extracts the base model name using a regex.
        
        Parameters:
            model (str): The model name with version and date.
        
        Returns:
            str: The base model name.
        """
        match = re.match(r'^(.*?)(?:-\d{4}-\d{2}-\d{2})?$', model)
        return match.group(1) if match else model

# Example usage
# generator = QuizQuestionGenerator()
# learning_objective = "Balance chemical equations using the law of conservation of mass"
# question = generator.generate_questions(learning_objective)
# current_costs = generator.calculate_current_cost()