import azure.cognitiveservices.speech as speechsdk
import openai
import json
import os
from datetime import datetime
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# =========== Azure OpenAI Configuration ===========
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# =========== Azure Search Configuration ===========
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX_NAME")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")

# =========== MongoDB (Cosmos DB) Configuration ===========
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

def main():
    print("Azure Speech Recognition Application")
    recognize_speech_with_confidence()

# Azure Speech Recognition Function
def recognize_speech_with_confidence():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Enable detailed output for sentence and word-level information
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Listening... Please speak into your microphone.")
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized Speech: {result.text}")

        # Parse detailed recognition result
        detailed_result_json = result.properties[speechsdk.PropertyId.SpeechServiceResponse_JsonResult]
        detailed_result = json.loads(detailed_result_json)

        # Save transcription and confidence details to a unique file
        save_transcription_with_timestamp(detailed_result)

        # Extract sentence-level confidence
        nbest = detailed_result.get("NBest", [{}])
        if nbest:
            sentence_confidence = nbest[0].get("Confidence", 0.0)
            print(f"Sentence-Level Confidence: {sentence_confidence:.2f}")

            # Check if confidence is below threshold
            if sentence_confidence < 0.60:
                print("Sentence confidence is too low. Please speak again.")
                prompt_user_to_speak_again()
                return
        else:
            print("No sentence-level confidence available.")

        # Detect intents and actions using Azure OpenAI
        detect_intents_and_actions(result.text)

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print(f"No speech could be recognized: {result.no_match_details}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

# Function to save transcription with a timestamped filename
def save_transcription_with_timestamp(transcription_data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"transcription_{timestamp}.json"
    try:
        with open(filename, "w") as file:
            json.dump(transcription_data, file, indent=4)
        print(f"Transcription saved to '{filename}'.")
    except Exception as e:
        print(f"Failed to save transcription: {e}")

# Function to prompt the user to speak again using text-to-speech
def prompt_user_to_speak_again():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    prompt_message = "Your confidence score was too low. Please speak again."
    print("Starting text-to-speech synthesis...")
    try:
        result = speech_synthesizer.speak_text_async(prompt_message).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Text-to-speech synthesis completed successfully.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Text-to-speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
    except Exception as e:
        print(f"Failed to synthesize speech: {e}")

# Function to detect intents and actions using Azure OpenAI
def detect_intents_and_actions(transcription):
    print(f"Sending transcription to Azure OpenAI for intent detection: {transcription}")

    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT, 
        api_key=AZURE_OPENAI_KEY,  
        api_version=AZURE_OPENAI_API_VERSION
    )

    # Prepare the conversation messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant trained to process user commands in natural language. "
                "Important: Return only valid JSON, with no markdown formatting or backticks. Return no additional text. "
                "Your task is to:\n"
                "1. Identify the user's primary intent (for example, 'add user', 'remove user', 'update a group','locate user' or 'move user').\n"
                "2. Extract relevant entities and slots from the input (e.g., user names, group names, additional details).\n"
                "3. Ignore irrelevant or side speech.\n\n"
                "If the user wants to move someone from one group to another, use: "
                "{\n"
                '  "intent": "update a group",\n'
                '  "slots": {\n'
                '    "user": "<user_name>",\n'
                '    "from_group": "<group_name>",\n'
                '    "to_group": "<group_name>"\n'
                "  },\n"
                '  "action": "<action_description>"\n'
                "}\n\n"
                "If it's unclear, return:\n"
                "{\n"
                '  "intent": "Unknown",\n'
                '  "slots": {},\n'
                '  "action": "Request clarification from the user."\n'
                "}"
            ),
        },
        {"role": "user", "content": transcription},
    ]

    intent_response = None
    try:
        # Call the Azure OpenAI Chat Completion API
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            max_tokens=500,
            temperature=0.3,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )

        intent_response = response.choices[0].message.content
        print("Detected Intent and Suggested Actions:")
        print(intent_response)

    except Exception as e:
        print(f"Error calling Azure OpenAI: {e}")
        return  # Exit here if we can't get a valid response

    # Parse the response and then perform any associated actions
    try:
        response_data = json.loads(intent_response)

        # 1. Optionally perform an AI Search based on "action" if desired
        action_query = response_data.get("action", "")
        if action_query:
            print(f"Performing AI Search with query: {action_query}")
            search_results = perform_azure_ai_search(action_query)
            print("Search Results:")
            for result in search_results:
                print(result)
        else:
            print("No actionable query extracted from the response.")

        # 2. Then attempt a database operation if the intent says so
        perform_database_operation(response_data)

    except Exception as e:
        print(f"Error parsing intent_response JSON or performing search: {e}")

# Perform Azure AI Search
def perform_azure_ai_search(query):
    try:
        search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY),
        )
        
        # Use `select` to limit returned fields
        results = search_client.search(
            search_text=query,
            top=1,
            select=["doc_id", "description", "chunk"]
        )
        
        documents = []
        for doc in results:
            documents.append(doc)
        
        return documents
    
    except Exception as e:
        print(f"Error performing Azure AI Search: {e}")
        return []

# ========== Database Write Logic ========== #
def perform_database_operation(response_data):
    """
    Examine the intent and slots from 'response_data'.
    If we need to perform a 'move user', 'add user', 'remove user', or 'update a group' operation, handle it here.
    """

    intent = response_data.get("intent", "").lower()
    slots = response_data.get("slots", {})

    # Example slot keys. Adjust based on your actual AI output:
    user = slots.get("user")

    # For the 'update a group' flow
    from_group = slots.get("from_group")
    to_group = slots.get("to_group")

    if intent == "update a group":
        # This is effectively "move user" from from_group to to_group
        if user and from_group and to_group:
            move_user_to_new_group(user, from_group, to_group)
        else:
            print("Insufficient data to update a group. Need 'user', 'from_group', and 'to_group'.")

    elif intent == "move user":
        # If your AI sometimes uses "move user" instead of "update a group"
        source_group = slots.get("sourceGroup")
        destination_group = slots.get("destinationGroup")
        if user and source_group and destination_group:
            move_user_to_new_group(user, source_group, destination_group)
        else:
            print("Insufficient data to move user. Need user, sourceGroup, and destinationGroup.")

    elif intent == "add user":
        group = slots.get("group")
        if user and group:
            add_user_to_group(user, group)
        else:
            print("Insufficient data to add user. Need user and a group.")

    elif intent == "remove user":
        group = slots.get("group")
        if user and group:
            remove_user_from_group(user, group)
        else:
            print("Insufficient data to remove user. Need user and group.")

    else:
        # You can add more logic for other intent types
        print(f"No database operation triggered for this intent: '{intent}'.")

def move_user_to_new_group(user, old_group, new_group):
    """
    Example function to update a user's group in Cosmos DB (MongoDB).
    Adjust the collection name, schema, etc., for your scenario.
    """
    try:
        client = MongoClient(MONGO_CONNECTION_STRING)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]

        # Suppose each document has fields: {"user": <string>, "group": <string>}
        # We'll attempt to find a doc {user: ..., group: ...} and change group to new_group
        result = collection.update_one(
            {"user": user, "group": old_group},
            {"$set": {"group": new_group}}
        )
        if result.matched_count > 0:
            print(f"Successfully moved user '{user}' from '{old_group}' to '{new_group}'.")
        else:
            print(f"No matching user/group found for user '{user}' in '{old_group}'.")
    except Exception as e:
        print(f"Error moving user to new group: {e}")

def add_user_to_group(user, group):
    """ Example to add a user to a given group """
    try:
        client = MongoClient(MONGO_CONNECTION_STRING)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]

        new_doc = {"user": user, "group": group}
        result = collection.insert_one(new_doc)
        print(f"Added user '{user}' to group '{group}'. Inserted ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error adding user to group: {e}")

def remove_user_from_group(user, group):
    """ Example to remove a user from a group """
    try:
        client = MongoClient(MONGO_CONNECTION_STRING)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]

        result = collection.delete_one({"user": user, "group": group})
        if result.deleted_count > 0:
            print(f"Removed user '{user}' from group '{group}'.")
        else:
            print(f"No matching user/group found for user '{user}' and group '{group}'.")
    except Exception as e:
        print(f"Error removing user from group: {e}")

if __name__ == "__main__":
    main()
