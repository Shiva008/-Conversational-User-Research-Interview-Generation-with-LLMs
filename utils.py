import openai
prompt = """
Introduction and Purpose:
"Hello! Welcome to our user research interview. Our goal is to gather valuable insights to improve our services/products. Your feedback is incredibly important to us. Are you ready to start?"

Initial Question:
"Could you please share your recent experience related to [topic of research]? This could be a specific event, interaction, or general thoughts you've had."

Follow-up Question Generation:
- Digging Deeper:
  - "What aspects of [user's experience] stood out to you the most?"
  - "Can you describe any challenges or pain points you encountered during [the experience]?"
  - "How do you think [specific aspect mentioned by the user] could be improved?"
  
- Adapting Dynamically:
  - Use keywords and sentiment analysis to tailor follow-up questions to the user's responses.

- Maintaining Natural Flow:
  - Ensure that the follow-up questions sound human-like and continue the conversation seamlessly. Avoid abrupt transitions or unrelated topics.
-add yourn own question also
-when user type 'end' end the conversation and give the feedback and some fields user can improve take reference of chat.give user an honest review.
"""
def get_initial_message():
    messages=[
            {"role": "system", "content":prompt},
            {"role": "user", "content": "input"},
            {"role": "assistant", "content": "Tell me your field"}
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages