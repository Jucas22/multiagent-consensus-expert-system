from agents.base_expert import BaseExpertAgent
from docs.constants import RESPONSE_OUTPUT_KEY
from docs.experts_descriptions import PSYCHOLOGY_EXPERT


class PsychologyExpertAgent(BaseExpertAgent):
    def __init__(self):
        super().__init__(
            role_name="psychology_expert",
            role_description=PSYCHOLOGY_EXPERT,
            output_key=RESPONSE_OUTPUT_KEY["PSYCHOLOGY_EXPERT"],
        )
