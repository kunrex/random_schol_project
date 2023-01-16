import os
import random
from google.cloud import dialogflow_v2beta1 as dialogflow

class ChatBot:
    session_client = None
    session_path = None

    projectId = None

    def __init__(self, credentialsVariable, credentialsPath, id, passWord):
        os.environ[credentialsVariable] = credentialsPath
        self.projectId = id

        self.session_client = dialogflow.SessionsClient()
        self.session_path = self.session_client.session_path(self.projectId, passWord)

    async def response(self, content):
        text_input = dialogflow.TextInput(text=content, language_code = "en-US")
        query_input = dialogflow.QueryInput(text=text_input)
    
        knowledge_base_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
            self.projectId, "knowledge_base_id"
        )

        query_params = dialogflow.QueryParameters(
            knowledge_base_names=[knowledge_base_path]
        )

        request = dialogflow.DetectIntentRequest(
            session=self.session_path, query_input=query_input, query_params=query_params
        )
        
        response = self.session_client.detect_intent(request=request)
        answers = response.query_result.fulfillment_messages
        return answers[random.randrange(0, len(answers))].text.text[0]