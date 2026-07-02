from enum import Enum

class EmailIntent(str, Enum): # recall an enum has a name and a value
    MEETING="meeting"
    THANKS="thanks"
    FOLLOW_UP="follow_up"
    UNKNOWN="unknown"

def detect_intent(text:str)->EmailIntent:
    email_lower=text.lower()
    if "meeting" in email_lower or "reschedule" in email_lower or "calendar" in email_lower:
        return EmailIntent.MEETING
    if "thank" in email_lower or "appreciate" in email_lower:
        return EmailIntent.THANKS
    if "follow up" in email_lower or "following up" in email_lower or "checking up":
        return EmailIntent.FOLLOW_UP
    return EmailIntent.UNKNOWN

def generate_reply_for_intent(intent:EmailIntent)->tuple[str,float]:
    if intent == EmailIntent.MEETING:
        return(
            "Hi, thanks for your message. That works for me. Please let me know what time suits you best.",
            0.7
        )

    if intent == EmailIntent.THANKS:
        return(
            "Hi, you are very welcome. Happy to help.",
            0.8
        )
    
    if intent == EmailIntent.FOLLOW_UP:
        return(
            "Hi, thanks for following up. I'll take a look and get back to you shortly.",
            0.6
        )
    
    return(
        "Hi, thanks for your email. I'll review this and get back to you shortly.",
        0.5
    )

def generate_draft_reply(email_body:str)->dict:
    intent=detect_intent(email_body)
    draft, confidence=generate_reply_for_intent(intent)
    return{
        "draft":draft,
        "confidence":confidence,
        "needs_review":confidence < 0.8
    }

