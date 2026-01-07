from agents.base_expert import BaseExpertAgent
from docs.constants import RESPONSE_OUTPUT_KEY
from docs.experts_descriptions import ETIHICS_EXPERT


class EthicExpertAgent(BaseExpertAgent):
    def __init__(self):
        super().__init__(
            role_name="ethic_experts",
            role_description=ETIHICS_EXPERT,
            output_key=RESPONSE_OUTPUT_KEY["ETHICS_EXPERT"],
        )
