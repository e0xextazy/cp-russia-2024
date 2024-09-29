from transformers import AutoTokenizer, AutoTokenizer, AutoModelForCausalLM
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
import torch
import re
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate


class RAG():
    def __init__(self):
        super().__init__()
        self.embed_model = HuggingFaceEmbedding(model_name="api/encoder_model")

        model_llm = AutoModelForCausalLM.from_pretrained(
            "IlyaGusev/saiga_llama3_8b",
            load_in_8bit=True,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        tokenizer_llm = AutoTokenizer.from_pretrained("IlyaGusev/saiga_llama3_8b")
        self.llm = HuggingFaceLLM(
            model=model_llm,
            tokenizer=tokenizer_llm,
            max_new_tokens=256,
            generate_kwargs={
                "temperature": 0.00001, 
                "do_sample": False, 
                "repetition_penalty": 1.12, 
                # "top_p": 0.9,
                # "top_k": 30,
                "pad_token_id": 128000,
                "eos_token_id": 128009,
                "bos_token_id": 128000},
            system_prompt="Ты умный ассистент которого зовут Наташа. Ты любишь отвечать на вопросы пользователей.",
            device_map="auto",
        )

        self.index = self.setup_index()
        self.template = PromptTemplate(
            "Ниже представлена информация из правовых документов:\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "На основе вышеуказанной информации из документов, ответь на вопрос пользователя. В ответе укажи только содержательную часть без повторения вопроса.\n"
            "Вопрос: {query}\n"
            "Ответ:"
        )

    def setup_index(self):
        node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=128)
        docs = SimpleDirectoryReader(input_files=[
            "case/03_ГЕНЕРАЛЬНОЕ ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ RUTUBE.docx", 
            "case/04_УСЛОВИЯ РАЗМЕЩЕНИЯ КОНТЕНТА.docx"]).load_data()
        nodes = node_parser.get_nodes_from_documents(docs)
        for node in nodes:
            node.text = re.sub("\\n", " ", node.text)
            node.text = re.sub(" +", " ", node.text)
        index = VectorStoreIndex(nodes, embed_model=self.embed_model)
        index = index.as_retriever(similarity_top_k=10)

        return index

    def predict(self, query):
        nodes = self.index.retrieve(query)
        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.complete(self.template.format(context_str=context_str, query=query)).text
        print(response)
        # response = re.findall(r"[\S \n]+?(?=---)", response)[0]
        response = re.findall(r".*", response)[0]

        return response.strip()

rag = RAG()
