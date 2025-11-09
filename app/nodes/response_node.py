from graph_state import TriageState
from llm.clients import get_llm_client
from llm.prompts import RESPONSE_PROMPT

def response_agent(state: TriageState) -> dict:

    client=get_llm_client() 

    chain=RESPONSE_PROMPT | client

    response =chain.invoke(RESPONSE_PROMPT.format(**state.model_dump()))    
     
    return {"final_customer_reply": response.content}



