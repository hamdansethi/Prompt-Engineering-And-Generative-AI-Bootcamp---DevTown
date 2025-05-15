from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os


load_dotenv()

HF_TOKEN = os.getenv("HF_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"


st.title("LangChain Code Generator")
st.markdown("Powered by Hugging Face")

topic = st.text_input("Enter a topic for the joke")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Joke Generating Assistant, just give me a joke on the given topic and do not continue the conversation."),
        ("user", "topic: {topic}")
    ]
)

llm = HuggingFaceEndpoint(
    endpoint_url = "HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=HF_TOKEN
)

output_parser = StrOutputParser()

chain = prompt|llm|output_parser

if topic:
    with st.spinner("Generating your joke..."):
        response = chain.invoke({"topic":topic})
        st.success("Here is your generated joke")
        st.write(response.strip())