from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import PromptTemplate

client = ChatNVIDIA(
    model="z-ai/glm-5.2",
    api_key="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",
    max_tokens=200
)

rag_info = "We do accept paypal"
user = "Do you guys do shipping"

rag_template = PromptTemplate(
    input_variables=["rag_info", "user"],
    template="This is info given from a sematic search {rag_info} and this is the user question {user} does the info match the user question say true for it does false for it doesn't"
)

