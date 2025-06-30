# backend/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json
import logging
import time

# Local imports
from .llm import ask_gpt_to_plan
from .filter import filter_and_count
from .retrieval import retrieve_context
from .data_loader import load_data
from .embedding import load_embeddings_and_index # Import for embeddings and index
from sentence_transformers import SentenceTransformer # Import for the model

# Configure logging for the FastAPI application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FastAPI Lifespan Management ---
# This is crucial for loading heavy resources (DataFrame, embeddings, models)
# only once when the application starts, and cleaning them up when it shuts down.
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for managing the lifecycle of the FastAPI application.
    Loads shared resources at startup and cleans them up at shutdown.
    """
    logger.info("Application startup: Loading shared resources...")
    
    # Load DataFrame and texts
    try:
        app.state.df, app.state.texts = load_data()
        logger.info(f"DataFrame loaded successfully with {len(app.state.df)} rows.")
    except Exception as e:
        logger.critical(f"Failed to load data: {e}")
        # Depending on criticality, you might want to exit here or handle gracefully
        raise HTTPException(status_code=500, detail=f"Backend startup failed: Data loading error - {e}")

    # Load embeddings and FAISS index
    try:
        app.state.embeddings, app.state.faiss_index = load_embeddings_and_index()
        logger.info(f"Embeddings ({app.state.embeddings.shape}) and FAISS index loaded.")
    except Exception as e:
        logger.critical(f"Failed to load embeddings/FAISS index: {e}")
        raise HTTPException(status_code=500, detail=f"Backend startup failed: Embedding error - {e}")

    # Load SentenceTransformer model
    try:
        app.state.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("SentenceTransformer model loaded.")
    except Exception as e:
        logger.critical(f"Failed to load SentenceTransformer model: {e}")
        raise HTTPException(status_code=500, detail=f"Backend startup failed: Model loading error - {e}")

    yield # Application will run here

    logger.info("Application shutdown: Cleaning up resources (if any).")
    # You can add cleanup code here if needed, e.g., closing connections.
    del app.state.df
    del app.state.texts
    del app.state.embeddings
    del app.state.faiss_index
    del app.state.embedder
    logger.info("Resources cleaned up.")


# Initialize FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)

# --- CORS Configuration ---
# Allow Cross-Origin Resource Sharing.
# IMPORTANT: For production, replace "*" with specific frontend domains
# (e.g., allow_origins=["http://localhost:5500", "https://your-frontend-domain.com"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development (be specific in production)
    allow_credentials=True, # Allow cookies/authentication headers
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)

# --- Pydantic Models for Request Validation ---
class QueryRequest(BaseModel):
    user_query: str

# --- API Endpoints ---

@app.post("/ask")
async def ask_user_question(request: QueryRequest):
    """
    Handles user questions by generating a filtering plan using GPT,
    then filtering and counting data, and returning the results.
    """
    start_time = time.time()
    logger.info(f"Received query: '{request.user_query}'")

    try:
        # Step 1: Get filtering plan from LLM
        plan_json = ask_gpt_to_plan(request.user_query)
        gpt_time = time.time() - start_time
        logger.info(f"GPT planning took {gpt_time:.2f} seconds.")
    except Exception as e:
        logger.error(f"Error during GPT planning: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query with AI: {e}")

    try:
        # Step 2: Parse the JSON plan from LLM
        plan = json.loads(plan_json)
        # Basic validation of the plan structure
        if not isinstance(plan, dict):
            raise ValueError("GPT did not return a valid JSON dictionary.")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON plan returned by GPT: {e}\nRaw plan: {plan_json}")
        raise HTTPException(status_code=500, detail="Invalid analysis plan from AI.")
    except ValueError as e:
        logger.error(f"Plan validation error: {e}")
        raise HTTPException(status_code=500, detail=f"AI plan structure is incorrect: {e}")


    # Step 3: Filter and count data using the loaded DataFrame
    start_filter = time.time()
    try:
        answer = filter_and_count(app.state.df, plan)
        filter_time = time.time() - start_filter
        logger.info(f"Filtering took {filter_time:.2f} seconds.")
    except Exception as e:
        logger.error(f"Error during data filtering: {e}")
        raise HTTPException(status_code=500, detail=f"Error filtering data: {e}")

    total_time = time.time() - start_time
    logger.info(f"Total /ask endpoint took {total_time:.2f} seconds.")

    return {
        "plan": plan,
        "answer": answer
    }


@app.post("/retrieve")
async def retrieve_context_docs(request: QueryRequest):
    """
    Retrieves relevant context documents based on a user query using pre-loaded
    SentenceTransformer and FAISS index.
    """
    start_time = time.time()
    logger.info(f"Received retrieval query: '{request.user_query}'")

    try:
        # Use the pre-loaded texts, embedder, and faiss_index from app.state
        context = retrieve_context(request.user_query, app.state.texts, app.state.embedder, app.state.faiss_index)
        retrieval_time = time.time() - start_time
        logger.info(f"Context retrieval took {retrieval_time:.2f} seconds.")
        return {"results": context}
    except Exception as e:
        logger.error(f"Error during context retrieval: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving context: {e}")

@app.get("/health")
async def health_check():
    """
    Endpoint for health checking. Returns a simple status indicating the backend is running.
    """
    return {"status": "ok", "message": "Backend is healthy."}

# --- Main entry point for running the Uvicorn server ---
if __name__ == "__main__":
    # The `app` object is now initialized with the lifespan context manager.
    # `reload=True` is useful for development as it restarts the server on code changes.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

