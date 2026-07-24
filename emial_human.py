from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatNVIDIA(model="z-ai/glm-5.2", api_key="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", temperature=1)
llm2 = ChatNVIDIA(model="z-ai/glm-5.2", api_key="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", temperature=0)

write_email = PromptTemplate.from_template(
    template="""
            Based off the given description of the email '{user}' write me a email with this format
            
            Dear [persons name if not given leave blank]
            
            body text here
            
            make this the name you used at the top"""
)

humanize = PromptTemplate.from_template(template="make this email '{email}' sound more human only change the wording not the format even make it a little less formal if you have to make it sound like a 8th grader wrote it and make it short")

llm_chain = (
    write_email
    | llm
    | StrOutputParser()
    | (lambda text: {"email": text})
    | humanize
    | llm2
    | StrOutputParser()
)

user = input("Email: ")

email = llm_chain.invoke({"user": user})

print(email)
