from openai import OpenAI
from typing_extensions import override
import json


OPENAI_API_FILE = "serviceAccountCredsOpenAI.txt"

# Authenticate and build service
with open(OPENAI_API_FILE, "r") as file:
    api_key = file.read().strip()  # Read and remove any unwanted spaces/newlines

client = OpenAI(
    api_key=api_key)
gptModel = "gpt-4o-mini"

def get_GPT_response(prompt, systemRole="You are a helpful assistant.", reponseFormat='text', json_schema=None, gptModel = "gpt-4o-mini"):

    """
    Function to send a text prompt (and optionally an image) to OpenAI's GPT model.


    Parameters:
    - prompt (str): The user input or question.
    - systemRole (str): System instructions for GPT behavior.
    - responseFormat (str): "text" or "json_object" or "json_schema".
    - json_schema (dict): JSON schema if using responseFormat="json_schema".
    - gptModel (str): Model name (e.g., "gpt-4o").
    - image_url (str): URL of an image (optional).


    Returns:
    - response (str/dict): The model's response.
    """

    if reponseFormat != "json_schema":
        completion = client.chat.completions.create(
            model=gptModel,
            messages=[
                {"role": "system", "content": systemRole},
                {
                    # instructions that request an output
                    "role": "user",
                    "content": prompt
                }],
            response_format={"type": reponseFormat}
        )

        response = completion.choices[0].message.content


    else:
        completion = client.chat.completions.create(
            model=gptModel,
            messages=[
                {"role": "system", "content": systemRole},
                {
                    # instructions that request an output
                    "role": "user",
                    "content": prompt
                }],
            response_format={"type": "json_object"},
            tool_choice={"type": "function", "function": {"name": "get"}},
            tools=[{"type": "function", "function": {"name": "get", "parameters": json_schema}}]
        )

        response = completion.choices[0].message.tool_calls[0].function.arguments

        try:
            response = completion.choices[0].message.tool_calls[0].function.arguments
        except:
            print("unexpected response format")
            response = completion.choices

    print(response)
    tokens_used = completion.usage.total_tokens

    # Pricing per 1,000 tokens (as of 2024, update with OpenAI’s pricing)
    PRICING = {
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},  # Prices in dollars per 1k tokens
    }
    model_pricing = PRICING.get(gptModel, {"input": 0.15 / 1000, "output": 0.6 / 1000})
    cost = (tokens_used / 1000) * model_pricing["input"]

    print(f"Tokens used: {tokens_used}, Estimated cost: ${cost:.6f}")

    return (response)


if __name__ == "__main__":
    print("****FIRST PROMPT****")
    prompt = "give me five interesting facts about Shakespeare"
    systemRole = "you are a bot making quiz questions for age 12-18 and provide your output in json format"
    data = get_GPT_response(prompt, systemRole, reponseFormat="json_object")

    try:
        jData = json.loads(data)
    except:
        print("invalid json format")

    print("****SECOND PROMPT****")
    prompt = "give me 10 jokes, each with a comedy score out of 10. Give it in a JSON format, for example - joke: text, score: score. Do not give me anything other than the JSON response"
    systemRole = "you are a joke creating bot"
    data = get_GPT_response(prompt, systemRole)

    print("****THIRD PROMPT****")
    prompt = "give me 10 different jokes, each with a comedy score out of 10. Give it in a JSON format, for example - joke: text, score: score. Do not give me anything other than the JSON response"
    systemRole = "you are a joke creating bot"
    data = get_GPT_response(prompt, systemRole, reponseFormat="json_object")


'''
completion.choices = 

[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='{\n  "characters": [\n    "Robin Hood",\n    "Ron Weasley",\n    "Ray Charles"\n  ]\n}', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None, annotations=[]))]
[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_1axbjdC6F6dLi5G8wufqmnAY', function=Function(arguments='{"characterList":[{"name":"Ron Weasley"},{"name":"Robin Hood"},{"name":"Rosa Parks"}]}', name='get'), type='function')], annotations=[]))]

'''
