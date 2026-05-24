from pydantic import BaseModel, Field, validator
import re

class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50)
    # Limit message length to save tokens and prevent "buffer" attacks
    message: str = Field(..., min_length=1, max_length=1000)

    @validator("message")
    def sanitize_message(cls, v):
        # 1. Strip whitespace
        v = v.strip()
        
        # 2. Basic Sanitization: Remove potential script tags
        v = re.sub(r'<[^>]*?>', '', v)
        
        # 3. Check for obvious malicious patterns (Optional but recommended)
        forbidden_phrases = ["ignore all previous instructions", "system override"]
        if any(phrase in v.lower() for phrase in forbidden_phrases):
            raise ValueError("Potential security threat detected in message.")
            
        return v