
import json
from watson_developer_cloud import ConversationV1

conversation = ConversationV1(
    username='param.virginatlantic@gmail.com',
    password='q1g6P4NM&',
    version='2016-09-20')

# replace with your own workspace_id
workspace_id = '4382aedb-14c0-409d-947f-a26c31a1615c'

response = conversation.message(workspace_id=workspace_id, message_input={
    'text': 'Hello'})
print(json.dumps(response, indent=2))