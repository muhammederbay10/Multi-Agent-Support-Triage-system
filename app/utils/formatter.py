from graph_state import TriageState
import logging 
from typing import Dict

logger = logging.getLogger(__name__)

def final_formatter(state: TriageState) -> Dict:
    """
    This is the final node in the graph. It takes the complete state
    and formats a clean JSON output for the API.
    """
    logger.info("Formatting final output")

    # Get all the key data from the state
    intent = state.get("intent")
    order_id = state.get("extracted_data", {}).get("order_id")
    customer_email = state.get("extracted_data", {}).get("customer_email")
    enrichment = state.get("enrichment")
    email_status = state.get("email_sent")
    customer_reply_text = state.get("final_customer_reply")


    # Handle the gneral inquiry case
    if intent == "general_inquiry":
        logger.info("Handling general inquiry")
        output = {
            "status": "Resolved",
            "intent": intent,
            "order_id": None,
            "customer_email": customer_email,
            "enrichment_data": None,
            "response_sent": email_status,
            "customer_reply": customer_reply_text
        }
    else:
        logger.info("Handling order-related inquiry")
        output = {
            "status": "Processed",
            "intent": intent,
            "order_id": order_id,
            "customer_email": customer_email,
            "enrichment_data": enrichment, # attach enrichment data if any
            "response_sent": email_status,
            "customer_reply": customer_reply_text
        }

    return {"final_output": output }
