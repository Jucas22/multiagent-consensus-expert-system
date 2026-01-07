from agents.base_expert import BaseExpertAgent
from docs.constants import RESPONSE_OUTPUT_KEY
from docs.experts_descriptions import SECURITY_EXPERT


class SecurityExpertAgent(BaseExpertAgent):
    def __init__(self):
        super().__init__(
            role_name="security_expert",
            role_description=SECURITY_EXPERT,
            output_key=RESPONSE_OUTPUT_KEY["SECURITY_EXPERT"],
        )
