def generate_draft_reply(email_body: str) -> dict:
    email_lower = email_body.lower()

    if "reschedule" in email_lower or "meeting" in email_lower:
        draft = (
            "Hi, thanks for your message. That works for me. "
            "Please let me know what time suits you best."
        )
        confidence = 0.7
    elif "thank" in email_lower:
        draft = "Hi, you're very welcome. Happy to help."
        confidence = 0.75
    else:
        draft = (
            "Hi, thanks for your email. I'll review this and get back to you shortly."
        )
        confidence = 0.5

    return {
        "draft": draft,
        "confidence": confidence,
        "needs_review": confidence < 0.8,
    }