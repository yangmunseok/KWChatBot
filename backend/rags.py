from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import os

def load_data():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "documents", "2-2. 졸업이수학점 안내.md")
    loader = TextLoader(file_path, encoding = 'utf-8')
    data = loader.load()
    return data

def text_split(docs):
    splitter = CharacterTextSplitter(
        separator = '',
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    documents = splitter.split_documents(docs)
    return documents

def indexing(docs):
    embed_model = HuggingFaceEmbeddings(
        model_name = 'jhgan/ko-sroberta-nli',
        model_kwargs = {'device':'cpu'},
        encode_kwargs = {'normalize_embeddings':True}
    )
    vectorstore = FAISS.from_documents(docs,
                                    embedding = embed_model,
                                    distance_strategy = DistanceStrategy.COSINE)
    return vectorstore

def get_chain():
    llm = ChatOpenAI(
        temperature = 0,
        model_name = "gpt-4o-mini",
        max_tokens=500
    )

    template = '''당신은 광운대학교 학생인 사용자에게 사용자가 입력한 자신의 입학 연도를 기반으로 졸업 요건을 알려주는 인공지능 챗봇입니다.
            졸업 이수학점 표는 총 7열입니다. 이때 7열중 교양은 (필수+균형)과 기초라는 2열로 다시 나누어집니다.
            주전공학점(필수 포함)은 단일 전공시와 다전공 이수시로 2열로 나누어집니다.
            또한 이 문서는 각 졸업 요건이 동일한 입학 연도 단위 앞 부분에 가., 나., 다. ... 순으로 번호를 매깁니다.
            이 중 어떤 부분을 참고해서 답변 하였는지 맨 처음에 명시하세요.
            오직 한가지 한 단위만 참고해서 답변해야 하며, 당신이 참고했다 말하는 부분만을 기반으로 답변해야 합니다.
            생략되는 정보가 없어야 합니다.
            오직 다음의 context에 기반하여 대답하세요. {context}, Question: {question}
            '''
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain

