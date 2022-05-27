import argparse
import json

from environs import Env
from google.cloud import dialogflow


def parse_args():
    parser = argparse.ArgumentParser(
        description="Adds new questions and answers to DialogFlow"
    )
    parser.add_argument("path", help="path to json file")
    return parser.parse_args()


def load_json(filepath):
    with open(filepath, "r") as file:
        return json.loads(file.read())


def detect_intent_texts(project_id, session_id, text, language_code="ru-RU"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result


def create_intent(project_id, display_name, questions, answers):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for question in questions:
        part = dialogflow.Intent.TrainingPhrase.Part(text=question)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=answers)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )
    intents_client.create_intent(request={"parent": parent, "intent": intent})


if __name__ == "__main__":
    env = Env()
    env.read_env()
    args = parse_args()

    try:
        intents = load_json(args.path)
    except (FileNotFoundError, PermissionError) as err:
        exit(err)

    for intent, texts in intents.items():
        create_intent(
            env.str("DIALOGFLOW_PROJECT_ID"),
            intent,
            texts["questions"],
            [texts["answer"]],
        )
