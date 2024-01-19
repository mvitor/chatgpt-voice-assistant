import tempfile, json, openai, config, subprocess, argparse, os
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
console = Console()
# with open('path/to/your/markdown.md') as f:
#     md = Markdown(f.read())
     
    
    
#from st_custom_components import st_audiorec

#openai.api_key = config.OPENAI_API_KEY

client = OpenAI(
    # This is the default and can be omitted
    api_key=config.OPENAI_API_KEY,
)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--role",
    help="Role name",
    nargs="?",
    default="Therapist",
    const="Therapist",
    type=str,
)
parser.add_argument(
    "--debug",
    help="Debug",
    nargs="?",
    default=False,
    const=False,
    type=str,
)
args = parser.parse_args()
#print (args)
conversation_history = []
with open("roles_en.json", "r") as f:
    data = json.load(f)
for role in data:
    if role["name"].lower() == args.role.lower():
        conversation_history = [role]

print (conversation_history)
def chat_with_gpt(messages):
    # response = openai.Completion.create(
    #     engine="text-davinci-002",  # You can experiment with different engines
    #     prompt=prompt,
    #     temperature=0.7,  # Adjust the temperature for creativity vs. consistency
    #     max_tokens=150,  # Control the response length
    #     n=1  # Number of responses to generate
    # )
    # return response.choices[0].text.strip()
    if args.debug: 
        print (f"\n\n\nmessages: {messages}")
    streams = client.chat.completions.create(messages=messages,
        model="gpt-3.5-turbo",
        #temperature=0.7,  # Adjust the temperature for creativity vs. consistency
        #max_tokens=150,  # Control the response length        
        stream=True
    )
    response = ""
    for chunk in streams:
        if chunk.choices[0].delta.content is not None:
            if args.debug:
                print(chunk.choices[0].delta.content, end="")    
            response += chunk.choices[0].delta.content
    return response
    #return response.choices[0].text.strip()


def main():
    print("ChatGPT Command Line Chatbot")
    print("Type 'exit' to end the conversation.")

    

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        #conversation_history.append(f"You: {user_input}")
        conversation_history.append({"role": "user", "content": user_input})
        if args.debug: 
            print(f"Query: {user_input}")
    
        print("Querying ChatCompletion API")
        #response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation_history)
        gpt_response = chat_with_gpt(conversation_history)      
        #print(f"\n\nChatGPT: {gpt_response}")
        md = Markdown(gpt_response)
        print(f"\n\nChatGPT: {console.print(md)}")
        
        conversation_history.append({"role": "user", "content": gpt_response})
        print (args.debug)
        if args.debug: 
            print (f"\n\nconversation_history: {conversation_history}\n\n")
        #print (conversation_history)
        
        
if __name__ == "__main__":
    main()
    
    