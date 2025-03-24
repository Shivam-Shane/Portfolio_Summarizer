from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv

# Add project root directory to PYTHONPATH
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from logger import logger

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio Summarizer API",
    description="API to summarize portfolio websites",
    version="1.0.0"
)

# Load environment variables
load_dotenv()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shivam-portfoliio.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Request model
class URLRequest(BaseModel):
    url: str

    class Config:
        schema_extra = {
            "example": {"url": "https://example.com/portfolio"}
        }

# Initialize LLM with validation
def initialize_llm():
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("LLM_MODEL", "mixtral-8x7b-32768")  # Default model if not specified
    
    if not api_key:
        logger.error("GROQ_API_KEY not found in environment variables")
        raise ValueError("GROQ_API_KEY is required")
    
    try:
        return ChatGroq(
            model=model,
            temperature=0,
            api_key=api_key,
            max_retries=2
        )
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise ValueError(f"LLM initialization failed: {str(e)}")

# Prompt template
prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM PORTFOLIO WEBSITE:
    {page_data}
    
    ### INSTRUCTION:
    The above text is scraped from a portfolio website. Extract and organize relevant details 
    in a clear, concise manner for industry-standard interviews. Include:
    
    - **Role**: Current or desired role
    - **Experience**: Relevant work experience with duration and achievements
    - **Projects**: Notable projects with descriptions and impact
    - **Skills**: Technical and soft skills
    - **Description**: Summary of professional background and goals

    Format as polished, structured text following resume writing best practices.
    
    ### FORMATTED OUTPUT (NO PREAMBLE):
    """
)

# Initialize chain
try:
    llm = initialize_llm()
    chain_extract = prompt_extract | llm
except ValueError as e:
    raise Exception(f"Failed to initialize application: {str(e)}")

async def fetch_portfolio_content(url: str) -> Optional[str]:
    """Fetch content from portfolio URL."""
    try:
        user_agent = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        loader = WebBaseLoader(url, header_template={"User-Agent": user_agent})
        documents = loader.load()
        
        if not documents:
            raise ValueError("No content retrieved from URL")
        
        content = documents[0].page_content
        logger.info(f"Successfully fetched content from {url}")
        return content
    
    except Exception as e:
        logger.error(f"Failed to fetch content from {url}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Content fetch failed: {str(e)}")

async def summarize_portfolio_content(content: Optional[str]) -> str:
    """Summarize portfolio content using LLM."""
    try:
        if not content or not isinstance(content, str):
            logger.warning("Invalid or empty content provided for summarization")
            return "No valid content available to summarize"
        
        result = await chain_extract.ainvoke({'page_data': content})
        logger.info("Successfully generated summary")
        return result.content
    
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")

@app.get("/", response_model=dict)
async def summarize(
    url: str = Query(..., 
                    description="URL of the portfolio website to summarize",
                    min_length=10,
                    regex=r"^https?://.*")
):
    """Summarize portfolio website content."""
    try:
        logger.info(f"Received request to summarize URL: {url}")
        content = await fetch_portfolio_content(url)
        summary = await summarize_portfolio_content(content)
        
        return {"summary": summary}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error processing {url}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/healthcheck")
async def root():
    """Root endpoint for health check."""
    return {"message": "Portfolio Summarizer API is running"}