# Quiz Question Generator

## Introduction

This project is a Quiz Question Generator that uses the OpenAI API to generate multiple-choice questions based on a given learning objective. It provides a RESTful API and a web front-end interface to interact with the generated questions. It is a technical assessment for the ML Engineer position at Labster (March 2025).

## Instructions on how to use the code

**Prerequisites**:
- Python installed and its path added to the system environment variables.

**Steps**:
1. Clone this git repository to your local environment: `git clone https://github.com/damian-mateos/labster-quiz.git`
2. Optional but recommended: create a virtual environment to have the project's dependencies: `python -m venv <your-venv-name>`. Then activate your virtual envioronment: `.\<your-venv-name>\Scripts\activate`.
3. Install the necessary dependencies by running `pip install -r .\labster-quiz\requirements.txt` in the terminal.
4. Run the Flask server: `python ./labster-quiz/src/quiz_api.py`
5. Copy the full path of the web_index.html file and open it in you preferred web browser (Chrome, Edge, Safari, etc.).
6. Enter a learning objective and click "Generate Question".
7. Answer the question and see if you are correct. The top right corner shows the ratio of correctly answered questions, and the bottom right corner indicates the current OpenAI API cost for the given token.

## Instructions on how to deploy the code to the cloud (Azure based)

- You need to create an Azure App Service in the Azure portal (you will need an Azure account).
- Install Azure CLI if you don't already have it available (follow the Azure CLI documentation) and use it to deploy the app. You can also use the Azure Portal, but here are the instructions using Azure CLI:
- Log in to Azure: `az login`.
- Create an App Service Plan: `az appservice plan create --name YourAppServicePlan --resource-group YourResourceGroup --sku FREE`
- Create a Web App: `az webapp create --resource-group YourResourceGroup --plan YourAppServicePlan --name YourWebAppName`
- Deploy the Flask App with Git: `git remote add azure https://YourWebAppName.scm.azurewebsites.net/YourWebAppName.git`, `git push azure main`.
  
## Explain the steps you took to finish the assessment

**1st commit - Initial commit**
- Set up the project: Initialized the project structure and created a virtual environment. Created and connected the GitHub repository to Visual Studio.

**2nd commit - QuizQuestionGenerator class 1.0.0**
- Created a config.yaml file to store the configuration variables, in this case just the OpenAI API key.
- Created a tokens_usage.csv file to log every call made with the provided OpenAI API key to monitor cost and usage.
- Created an initial system message and store it in the system_message.txt file.
- Created an initial notebook main_nb.ipynb to perform tests and call the OpenAI API.
- Created a requirements.txt file to store the necessary libraries.
- Created a quiz_generator.py script containing the QuizQuestionGenerator class to generate the quiz questions and log the API calls.

**3rd commit - QuizQuestionAPI v1.0.0, web_index.html v1.0.0 & QuizQuestionGenerator v1.0.1**
- Created the quiz_api.py script containing the QuizQuestionAPI class that provides a RESTful API interface for the QuizQuestionGenerator.
- Created the web_index.html file containing the simple front-end interface to interact with the API.
- Made minor adjustments to the previous files.

**4th commit - MVP: v1.0.1 and new system prompt**
- Changed the prompt in the system_message.txt file to give more specific instructions to the LLM.
- Parsed the LLM answer in the quiz_api.py script to JSON format.
- Updated the interface in the web_index.html file for a better user experience.

**5th commit - Readme with documentation and minor changes**
- Reorganized some files, updated this README.md file and renamed main_nb.ipynb to testing_endpoints.ipynb for testing endpoints without the web interface.

## Highlight the easiest and the hardest part of it

- Easiest part: developing the QuizQuestionGenerator class and designing a simple prompt to get the desired format and type of answers from the LLM.
- Hardest part: the most challenging task for me was creating the web_index.html front-end code, as I am not accustomed to front-end development. However, modern AI tools significantly help non-experienced users in some coding languages to create simple front-end code for projects like this one.

## Quality and scientific correctness of the questions generated

To ensure the quality and scientific correctness of the generated questions, the following steps could be taken in a production environment:

- System Prompt Refinement: Continuously refine and improve the system prompt to guide the AI in generating accurate and high-quality questions. I have only tried one prompt as I see this testing out of the scope of the assessment. In a real-scenario I would have tried more models (gpt-4.5-preview, gpt-4o, gpt-4, gpt-3.5-turbo), different parameters of the model as temperature, top_p, max_completion_tokens, etc. I would choose the final model and parameters depending on the cost and the quality of the results.

- Human Review: Implement a human review process where subject matter experts review the generated questions for accuracy and scientific correctness. This option depends on your budget and resources, but it is a good option if available.

- Automated Validation: Develop automated validation scripts to check the format and basic correctness of the generated questions. This is cheaper than the option above and more scalable.

- User Feedback: Collect feedback from users and students to identify any inaccuracies or areas for improvement in the generated questions. The feedback from the users of an AI tool is very useful, so it would be interesting to ask them for feedback and use it to improve the generating process.

By following these steps, the quality and scientific correctness of the questions can be maintained and continuously improved in a real-world scenario.