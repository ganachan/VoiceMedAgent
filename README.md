# VoiceMedAgent

#VoiceMedAgent – Overview
VoiceMedAgent is a proof-of-concept (POC) application demonstrating how to build a voice-driven workflow leveraging Azure services:

Speech Capture (User → Application/Device):
The user speaks into a device or application. Audio is captured and prepared for transcription.

Speech-to-Text (Azure AI Speech):
The audio is sent to Azure’s Speech service, which returns text along with a confidence score indicating transcription accuracy.

#Confidence Scoring & Retry Loop:

If High Confidence, the system proceeds to the next step.
If Low Confidence, the user is prompted to retry or clarify their request.
Transcription Processing:
The validated transcript is passed along for query embedding and further analysis.

#Query Embeddings & AI Search:

Query Embeddings: The text is transformed into vector embeddings (e.g., using Azure OpenAI).
Azure AI Search: These embeddings are used to find the most relevant documents or data in your store.
Slot Matching / Intent Extraction:
Using the search results and any additional AI logic, the system extracts user commands or specific entities (slots) (e.g., user’s name, action to perform, etc.).

#Feedback & Actions:

If confidence is high, the action (e.g., “move user,” “add user,” “update record”) proceeds.
If further clarification is needed, the user is notified to restate or provide additional info.
Data Storage & Monitoring:

Query IDs, confidence scores, response times, and retrieval results can be logged to Cosmos DB or SQL for monitoring.
These logs help with analytics, troubleshooting, and performance tuning.
Key Benefits
Hands-Free Interaction: Allows users to operate via voice commands.
Robust Error Handling: Confidence checks ensure low-confidence transcriptions prompt the user to speak again.
Extendable Embeddings: You can switch to other embedding providers or vector databases as needed.
Scalable Search: Azure AI Search scales with the data volume while still returning relevant results quickly.
Data Logging & Monitoring: Storing logs helps track usage patterns, response times, and success rates.
Typical Use Cases
Healthcare: Retrieve patient info or schedule updates via voice commands.
Customer Support: Guide agents through knowledge bases by spoken queries.
Workforce Management: Perform user/group updates (e.g., “move user from one team to another”) hands-free.
Field Operations: Voice-based info lookups while on the go, without needing a keyboard.
#Getting Started
Clone the Repo:

bash
Copy
Edit
git clone https://github.com/<YourOrg>/vociemedagent.git
cd vociemedagent
Set Up Environment:

Create a .env file with your Azure Speech, Azure OpenAI, Azure Search, and database credentials (e.g., Cosmos DB).
Install required Python packages (pip install -r requirements.txt).
Prepare Your Data:

(Optional) Insert any initial documents or records in your database for testing (e.g., user listings, knowledge articles).
Run the Application:

Start with python app.py.
Speak into your microphone when prompted; watch the console logs to see the entire flow—speech recognition, confidence check, embedding & search, and final action or retry message.
