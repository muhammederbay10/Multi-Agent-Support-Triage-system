
import dotenv

# Load environment variables
dotenv.load_dotenv() 

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any   

# Import the necessary modules
from workflow import app_graph
from graph_state import TriageState

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent Support Ticket API",
    description="API for processing raw support emails with a LangGraph agent system.",
    version="1.0.0"
)

# Define the request model
class SupportRequest(BaseModel):
    raw_text: str

# Define the response model
class SupportResponse(BaseModel):
    status: str
    intent: str
    order_id: str | None
    customer_email: str | None
    enrichment_data: Dict[str, Any] | None
    response_sent: bool | None
    customer_reply: str | None

@app.post("/v1/process_ticket", response_model=SupportResponse)
async def process_ticket(request: SupportRequest):
    """
    Process a new raw support email.
    
    This endpoint runs the full langgraph agent workflow:
    1. Triage
    2. Extraction
    3. Enrichment(billing & order)
    4. Response Generation
    5. Final Formatting
    """
    try:
        # Input state for the graph
        graph_input = {"raw_text": request.raw_text}

        # Invoke the graph
        config = {"recursion_limit": 25}
        final_state: TriageState = app_graph.invoke(graph_input, config=config)

        # Prepare the response
        final_api_output = final_state.get("final_output") 

        if not final_api_output:
            raise HTTPException(status_code=500, detail="Failed to generate final output.")

        # Map the final output to the response model
        response_data = {
            "status": final_api_output.get("status", "Error"),
            "intent": final_api_output.get("intent", "Unknown"),
            "order_id": final_api_output.get("order_id"),
            "customer_email": final_api_output.get("customer_email"),
            "enrichment_data": final_api_output.get("enrichment_data"),
            "response_sent": final_api_output.get("response_sent"),
            "customer_reply": final_api_output.get("customer_reply")
            }
 
        return SupportResponse(**response_data)

    except Exception as e:
        print(f"Error processing ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)