# VoiceMedAgent

**VoiceMedAgent** demonstrates a voice-driven workflow using several Azure services.  
It listens to user speech, transcribes it, analyzes intent, and then takes automated actions or returns relevant data — **entirely by voice**.

---

## How It Works

### 1. Speech Capture (User → Application/Device)
- The user speaks into a device or application.  
- Audio is captured and prepared for transcription.

### 2. Speech-to-Text (Azure AI Speech)
- Audio is sent to **Azure’s Speech** service.  
- Returns text with a **confidence score** indicating transcription accuracy.

### 3. Confidence Scoring & Retry Loop
- **High Confidence**: Moves to the next step.  
- **Low Confidence**: Prompts the user to retry or clarify.  
- **Transcription Processing**: Validated transcript is forwarded for query embedding and further analysis.

### 4. Query Embeddings & AI Search
- **Query Embeddings**: Converts text into vector embeddings (e.g., via **Azure OpenAI**).  
- **Azure AI Search**: Uses embeddings to find relevant documents/data.  
- **Slot Matching / Intent Extraction**: Identifies user commands or entities (e.g., user name, action).

### 5. Feedback & Actions
- **If confidence is high**: Perform the requested action (e.g., “move user,” “add user,” “update record”).  
- **If clarification needed**: Ask the user to restate or provide extra details.

### 6. Data Storage & Monitoring
- **Cosmos DB** or **SQL** logs query IDs, confidence scores, response times, and results.  
- Use logs for **analytics**, **troubleshooting**, and **performance tuning**.

---

## Key Benefits

- **Hands-Free Interaction**: Issue commands via voice.  
- **Robust Error Handling**: Confidence checks prompt re-tries on low scores.  
- **Extendable Embeddings**: Swap in other embedding/vector services.  
- **Scalable Search**: Azure AI Search manages large data sets efficiently.  
- **Data Logging & Monitoring**: Track usage, response times, and success rates.

---

## Typical Use Cases

- **Healthcare**: Quickly retrieve patient info or schedule updates.  
- **Customer Support**: Guide agents through knowledge bases using voice queries.  
- **Workforce Management**: Move or add users to groups effortlessly.  
- **Field Operations**: On-the-go info lookups without a keyboard.

---

## Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/<YourOrg>/vociemedagent.git
cd vociemedagent


### 2. Set Up Environment
Create a .env file with your Azure Speech, Azure OpenAI, Azure Search, and Cosmos DB credentials.
Install Python packages:
pip install -r requirements.txt
### 3. Prepare Your Data
(Optional) Insert initial documents or records in your database (e.g., user entries, knowledge articles).
### 4. Run the Application
python app.py
