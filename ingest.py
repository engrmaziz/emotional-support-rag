from datasets import load_dataset
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import pandas as pd

def ingest_datasets():
    print("Downloading MentalChat16K dataset from Hugging Face...")
    # This single line downloads the dataset directly into your codespace
    mental_chat = load_dataset("ShenLab/MentalChat16K", split="train")
    
    print("Downloading Cactus CBT dataset from Hugging Face...")
    cactus = load_dataset("LangAGI-Lab/cactus", split="train")

    # Convert to pandas dataframes to easily extract the text
    df_mental = mental_chat.to_pandas()
    df_cactus = cactus.to_pandas()

    print("Extracting text fields...")
    # MentalChat16K stores responses in an 'output' column
    texts_mental = df_mental['output'].dropna().head(500).tolist()
    
    # Cactus stores the counseling plans in a 'text' or 'counseling_plan' column
    # (Adjust column name if needed based on the dataset schema)
    texts_cactus = df_cactus['dialogue'].dropna().head(500).tolist() 

    # Combine both datasets
    all_texts = texts_mental + texts_cactus
    df_combined = pd.DataFrame({'text': all_texts})

    print(f"Total documents to process: {len(df_combined)}")

    # Load the text into LangChain Document format
    loader = DataFrameLoader(df_combined, page_content_column="text")
    documents = loader.load()

    # Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    print("Generating embeddings and saving to ChromaDB locally. This may take a minute...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Save to a local folder named 'chroma_db'
    Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
    print("Success! The RAG database has been built and saved to ./chroma_db")

if __name__ == "__main__":
    ingest_datasets()