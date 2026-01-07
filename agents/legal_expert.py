from agents.base_expert import BaseExpertAgent
from docs.constants import RESPONSE_OUTPUT_KEY
from docs.experts_descriptions import LEGAL_EXPERT


class LegalExpertAgent(BaseExpertAgent):
    def __init__(self):
        super().__init__(
            role_name="legal_expert",
            role_description=LEGAL_EXPERT,
            output_key=RESPONSE_OUTPUT_KEY["LEGAL_EXPERT"],
        )
