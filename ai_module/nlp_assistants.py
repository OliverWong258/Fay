import os
from openai import OpenAI
import openai
from utils import util
import time

os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

openai.proxy = "http://127.0.0.1:7890"
client = OpenAI(api_key=util.assistant_key) # gpt4 key
# for debug
print(f"client: {client}")

file_paths = ["C://Users//31853//Desktop//year//2016-2017.txt", "C://Users//31853//Desktop//year//2018-2019.txt", 
              "C://Users//31853//Desktop//year//2020-2021.txt", "C://Users//31853//Desktop//year//2022-2023.txt", "C://Users//31853//Desktop//year//NewLixon.txt"]

uploaded_files = []

for file_path in file_paths:
    with open(file_path, 'rb') as file_to_upload:
        uploaded_file = client.files.create(
            file=file_to_upload,
            purpose='assistants',
        )
        uploaded_files.append(uploaded_file)
# print info of the uploaded files
for file in uploaded_files:
    print(f"Uploaded file ID: {file.id}")
    
file_ids = [file.id for file in uploaded_files]
    
assistant = client.beta.assistants.create(
    name="NewLixon AI Assistent",
    instructions="You are a AI Assistent that answers any queries related to NewLixon company based on the files uploaded",
    tools=[{"type": "retrieval"}],
    model="gpt-4-turbo-preview",
    file_ids=file_ids
)
thread = client.beta.threads.create()
print(f"thread: {thread}")
    
def question(cont):
    starttime = time.time()
    print("here")
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=cont
    )
    
    # client.beta.threads.messages.list(thread_id=thread.id).data
    print(client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value)
    
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id
    )
    
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status=="completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            util.log(1, "Api time: " + str(time.time() - starttime))
            return text




