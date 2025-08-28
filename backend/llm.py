from langchain_google_genai import GoogleGenerativeAI

class LLM():
    def __init__(self, temperature = 0.0) -> None:
        self.__llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)
        
    def get_llm(self):
        return self.__llm