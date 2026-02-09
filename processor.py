import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 1. LOAD ENVIRONMENT VARIABLES
load_dotenv()

# 2. SETUP THE LLM (The "Brain")
# We use gpt-4o-mini because it is cheap, fast, and good enough for this task.
# If you want to use a local model (Ollama), swap this for ChatOllama.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. DEFINE THE OUTPUT STRUCTURE (Pydantic)
# This forces the LLM to return JSON, which prevents regex headaches later.
# Employers LOVE seeing Pydantic used for data validation.
class ArticleAnalysis(BaseModel):
    clickbait_element: str = Field(description="The specific part of the original title that is hype (e.g., 'Shocking truth', 'You won't believe').")
    main_fact: str = Field(description="The core piece of information the article is actually conveying.")
    new_title: str = Field(description="A dry, boring, factual summary of the Main Fact. Max 15 words.")
    hype_score: int = Field(description="1-10 score.")
    category: str = Field(description="Category.")

parser = JsonOutputParser(pydantic_object=ArticleAnalysis)

# 4. THE PROMPT TEMPLATE (The "Instruction Manual")
# We give it a "Persona" (Boring Editor) to enforce the style we want.
template = """
You are a 'Boring News Editor'. Your job is to de-sensationalize news.
Analyze the following article headline and summary.

Rules:
1. Rewrite the title to be purely factual. Remove questions, exclamations, and emotional words.
2. If the title is already factual, keep it similar.
3. Rate the 'Hype Score' of the ORIGINAL title (1 = Boring/Factual, 10 = Pure Clickbait).
4. Categorize the article.

Input Title: {title}
Input Summary: {summary}

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(template, partial_variables={"format_instructions": parser.get_format_instructions()})

# Create the Chain (Prompt -> LLM -> Parser)
chain = prompt | llm | parser

# 5. THE PROCESSING FUNCTION
def process_articles(csv_file_path):
    print(f"Loading data from {csv_file_path}...")
    df = pd.read_csv(csv_file_path)
    
    # Let's just process the top 5 for testing (so you don't spend $$ on API credits yet)
    # Remove .head(5) when you are ready to run the full batch.
    subset = df.head(200).copy()
    
    results = []
    
    print("--- Starting AI Processing ---")
    for index, row in subset.iterrows():
        try:
            print(f"Processing: {row['title'][:30]}...")
            
            # Invoke the LangChain chain
            response = chain.invoke({
                "title": row['title'],
                "summary": row['summary']
            })
            
            # Add original data + new AI data to results
            response['original_title'] = row['title']
            response['original_link'] = row['link']
            results.append(response)
            
        except Exception as e:
            print(f"❌ Error on row {index}: {e}")
            
    # Convert results to DataFrame
    processed_df = pd.read_json(pd.DataFrame(results).to_json()) # normalization trick
    
    # Save
    output_filename = "processed_news.csv"
    processed_df.to_csv(output_filename, index=False)
    print(f"--- Done! Saved to {output_filename} ---")
    
    # Preview
    print("\nSample Output:")
    print(processed_df[['original_title', 'new_title', 'hype_score']].head())

if __name__ == "__main__":
    # Replace with the actual name of your CSV file from Step 1
    # You might need to check your folder for the exact date-stamped name
    latest_csv = [f for f in os.listdir('.') if f.startswith('news_data')][0] 
    process_articles(latest_csv)