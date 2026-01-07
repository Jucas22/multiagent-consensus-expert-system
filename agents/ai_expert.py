from agents.base_expert import BaseExpertAgent
from docs.constants import RESPONSE_OUTPUT_KEY
from docs.experts_descriptions import AI_EXPERT


class AIExpertAgent(BaseExpertAgent):
    def __init__(self):
        super().__init__(
            role_name="ai_expert",
            role_description=AI_EXPERT,
            output_key=RESPONSE_OUTPUT_KEY["AI_EXPERT"],
        )
