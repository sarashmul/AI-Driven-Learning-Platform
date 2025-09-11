"""
AI service for OpenAI API integration.
Handles lesson generation, response formatting, and AI model management.
"""
import openai
import time
import logging
import ssl
import httpx
from typing import Optional, Dict, Any
from ..core.config import settings
from ..core.exceptions import AIServiceException

# Configure logging
logger = logging.getLogger(__name__)


class AIService:
    """Service for handling AI-powered lesson generation using OpenAI."""
    
    def __init__(self):
        self.model_name = settings.openai_model
        
        # Create an SSL context that doesn't verify certificates for development
        # Note: This is not recommended for production!
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Create custom HTTP client with relaxed SSL
        http_client = httpx.Client(
            verify=False,  # Disable SSL verification
            timeout=30.0
        )
        
        try:
            self.client = openai.OpenAI(
                api_key=settings.openai_api_key,
                http_client=http_client
            ) if settings.openai_api_key else None
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
        
        if not self.client:
            logger.error("Failed to initialize OpenAI client")
    
    def generate_lesson(
        self,
        prompt: str,
        category_name: Optional[str] = None,
        subcategory_name: Optional[str] = None,
        user_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a learning lesson based on user prompt and context.
        
        Args:
            prompt: User's learning prompt
            category_name: Selected category for context
            subcategory_name: Selected subcategory for context
            user_context: Additional user context
            
        Returns:
            Dictionary containing response, model info, and timing
            
        Raises:
            AIServiceException: If AI service fails
        """
        if not self.client:
            raise AIServiceException("AI service is not properly configured")
        
        start_time = time.time()
        
        try:
            # Build enhanced prompt with context
            enhanced_prompt = self._build_enhanced_prompt(
                prompt, category_name, subcategory_name, user_context
            )
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert tutor who creates comprehensive, educational lessons. Provide clear, well-structured explanations with examples and practical applications."
                    },
                    {
                        "role": "user",
                        "content": enhanced_prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract text from response
            if response.choices and response.choices[0].message.content:
                lesson_content = response.choices[0].message.content
            else:
                raise AIServiceException("AI service returned empty response")
            
            return {
                "response": lesson_content,
                "model_used": self.model_name,
                "response_time_ms": response_time_ms,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            response_time_ms = int((time.time() - start_time) * 1000)
            
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                raise AIServiceException("AI service quota exceeded. Please try again later.")
            elif "api" in str(e).lower():
                raise AIServiceException("AI service is temporarily unavailable")
            else:
                raise AIServiceException(f"AI generation failed: {str(e)}")
    
    def _build_enhanced_prompt(
        self,
        user_prompt: str,
        category_name: Optional[str] = None,
        subcategory_name: Optional[str] = None,
        user_context: Optional[str] = None
    ) -> str:
        """
        Build an enhanced prompt with context for better AI responses.
        
        Args:
            user_prompt: Original user prompt
            category_name: Category context
            subcategory_name: Subcategory context
            user_context: User context
            
        Returns:
            Enhanced prompt string
        """
        enhanced_parts = [
            "You are an expert educational content creator. Generate a comprehensive, engaging learning lesson based on the following request."
        ]
        
        # Add category context
        if category_name:
            enhanced_parts.append(f"Category: {category_name}")
        
        if subcategory_name:
            enhanced_parts.append(f"Subcategory: {subcategory_name}")
        
        # Add user context if available
        if user_context:
            enhanced_parts.append(f"Learning Context: {user_context}")
        
        # Add the main prompt
        enhanced_parts.extend([
            f"User Request: {user_prompt}",
            "",
            "Please provide a structured lesson that includes:",
            "1. A clear introduction to the topic",
            "2. Key concepts and explanations",
            "3. Practical examples or applications",
            "4. Summary of main points",
            "5. Suggested next steps for further learning",
            "",
            "Make the content engaging, educational, and appropriate for the specified category and context."
        ])
        
        return "\n".join(enhanced_parts)
    
    def validate_prompt_content(self, prompt: str) -> bool:
        """
        Validate if the prompt content is appropriate for AI processing.
        
        Args:
            prompt: User prompt to validate
            
        Returns:
            True if prompt is valid, False otherwise
        """
        # Basic content validation
        if not prompt or len(prompt.strip()) < 10:
            return False
        
        # Check for potentially harmful content (basic filtering)
        harmful_keywords = [
            "hack", "exploit", "illegal", "violence", "harmful",
            "dangerous", "inappropriate", "explicit"
        ]
        
        prompt_lower = prompt.lower()
        for keyword in harmful_keywords:
            if keyword in prompt_lower:
                logger.warning(f"Potentially harmful content detected in prompt: {keyword}")
                return False
        
        return True
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current AI model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "provider": "OpenAI",
            "available": self.client is not None,
            "api_configured": settings.openai_api_key is not None
        }
    
    def health_check(self) -> bool:
        """
        Perform a health check on the AI service.
        
        Returns:
            True if service is healthy, False otherwise
        """
        if not self.client or not settings.openai_api_key:
            return False
        
        try:
            # Simple test generation
            test_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "Say 'AI service is working'"}],
                max_tokens=50
            )
            return test_response.choices[0].message.content is not None
        except Exception as e:
            logger.error(f"AI service health check failed: {e}")
            return False


# Global AI service instance
ai_service = AIService()
