from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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",
)

def draft():
    user = input("What do you want the email to be about? ")
    response = client.chat.completions.create(
        model="z-ai/glm-5.2",
        messages=[{"role": "system", "content": """Write a email based off what the user wants you will right it in this format
                                                    Dear [name here if they do not give a name then just put [name here]]
                                                    
                                                    [body text here]
                                                    
                                                    
                                                    sincerely [name if no name mentioned put [name] this should be the same name as the one in the greeting]
                                                    
                                                    do not put anything else in the reply but the email"""},
                  {"role": "user", "content": user}]
    )
    return response.choices[0].message.content

def grammar():
    user = input("Paste the email you want proofed here: ")
    response = client.chat.completions.create(
        model="z-ai/glm-5.2",
        messages=[{"role": "system", "content": "fix the grammar in the email do not change anything but the grammar in the email"},
                  {"role": "user", "content": user}]
    )
    return response.choices[0].message.content

def tone():
    user = input("Paste the email you want to sound more professional here: ")
    response = client.chat.completions.create(
        model="z-ai/glm-5.2",
        messages=[{"role": "system", "content": "fix the grammar in the email do not change anything but the grammar in the email"},
                  {"role": "user", "content": user}]
    )
    return response.choices[0].message.content[1]

tools = [{
    "type": "function",
    "function": {
        "name": "write_email",
        "description": "Writes a brand new email from scratch based on the user's instructions. Use this when the user wants an email drafted for them (e.g. 'write me an email asking my boss for time off'). Do NOT use this if an email already exists and the user wants it edited.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
},
{
    "type": "function",
    "function": {
        "name": "fix_grammar",
        "description": "Corrects spelling and grammar mistakes in an EXISTING email that the user has already written and pasted in. Use only when the user explicitly asks to fix/check grammar on text they provided.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
},
{
    "type": "function",
    "function": {
        "name": "professionalize_email",
        "description": "Rewrites an EXISTING email to sound more formal and professional in tone, without changing its meaning. Use only when the user has already provided email text and wants the tone adjusted.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
}]

def tool_call(user):
    response = client.chat.completions.create(
        model="z-ai/glm-5.2",
        messages={"role": "user", "content": user},
        tools=tools,
        tool_choice="required"
    )
    return response.choices[0].message

def main():
    user = input("User: ")
    tool_response = tool_call(user)
    if tool_response.tool_calls[0].function.name == "write_email":
        print("\n", draft())
    elif tool_response.tool_calls[0].function.name == "fix_grammar":
        print(grammar())
    elif tool_response.tool_calls[0].function.name == "professionalize_email":
        print(tone())

main()
