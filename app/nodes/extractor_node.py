from graph_state import TriageState
from llm.clients import get_llm_client
from llm.prompts import EXTRACTOR_PROMPT
from pydantic import BaseModel

class SchemaForExtraction(BaseModel):
    order_id: str 
    customer_email: str 
    item_name: str 

def extractor_agent(state: TriageState) -> dict:
    client = get_llm_client()
    
    text = state["raw_text"]
    
    # Chain with structured output
    chain = EXTRACTOR_PROMPT | client.with_structured_output(SchemaForExtraction)
    
    response = chain.invoke({"raw_text": text})
    
    return {"extracted_data": response.model_dump()}
