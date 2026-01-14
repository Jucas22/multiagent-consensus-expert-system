import os
import litellm
import requests
import feedparser
from typing import List, Dict
from datetime import date
from dotenv import load_dotenv

load_dotenv()
env = os.environ

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.lite_llm import LiteLlm

from docs.constants import LLM_MODEL, GLOBAL_INSTRUCTIONS
from docs.experts_descriptions import *


# Registrar modelo personalizado en litellm
# litellm.add_known_models(
#     {
#         "gpt-oss-120b": {
#             "max_tokens": 1280000,
#             "input_cost_per_token": 0,
#             "output_cost_per_token": 0,
#             "litellm_provider": "openai",
#             "mode": "chat",
#         }
#     }
# )

llm_model = LiteLlm(
    model="openai/gpt-oss-120b",
    api_key="sk-LFXs1kjaSxtEDgOMlPUOpA",
    api_base="https://api.poligpt.upv.es/v1",
)

litellm._turn_on_debug()


# ============================================================
#  TOOLS:
# ============================================================


def generate_summat_file(content: str | None = None, session=None) -> str:
    """Escribe el informe final en final_report.txt usando session.state si no se pasa content."""
    if content is None and session is not None and hasattr(session, "state"):
        content = session.state.get("final_report", "")
    if content is None:
        content = ""
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write(content)
    return "Archivo final_report.txt generado correctamente."


# Agentes Expertos:

ethics = LlmAgent(
    name="agente_etico",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos éticos.",
    instruction=ETIHICS_EXPERT + "\n\n" + GLOBAL_INSTRUCTIONS,
    tools=[],
    output_key="ethics_response",
)

psychology = LlmAgent(
    name="agente_psicologia",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos psicológicos.",
    instruction=PSYCHOLOGY_EXPERT + "\n\n" + GLOBAL_INSTRUCTIONS,
    tools=[],
    output_key="psychology_response",
)

security = LlmAgent(
    name="agente_seguridad",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos de seguridad.",
    instruction=SECURITY_EXPERT + "\n\n" + GLOBAL_INSTRUCTIONS,
    tools=[],
    output_key="security_response",
)

legal = LlmAgent(
    name="agente_legal",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos legales.",
    instruction=LEGAL_EXPERT + "\n\n" + GLOBAL_INSTRUCTIONS,
    tools=[],
    output_key="legal_response",
)

ai = LlmAgent(
    name="agente_ia",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos técnicos de IA.",
    instruction=AI_EXPERT + "\n\n" + GLOBAL_INSTRUCTIONS,
    tools=[],
    output_key="ai_response",
)

coordinador = LlmAgent(
    name="coordinador_evaluacion",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que recopila opiniones de varios expertos.",
    instruction=COORDINATOR_AGENT,
    output_key="expert_opinions",
)

redactor = LlmAgent(
    name="redactor_informe_final",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que redacta el informe final.",
    instruction=REDACTOR_AGENT,
    output_key="final_report",
)

generador_documentos = LlmAgent(
    name="generador_documentos",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que genera documentos a partir del informe final.",
    instruction=(
        "Eres el Agente Generador de Documentos.\n"
        "Usa SIEMPRE la función generate_summat_file(content: str) para crear final_report.txt con el contenido en session.state['final_report']. Si no hay contenido, infórmalo."
    ),
    tools=[generate_summat_file],
)
# ============================================================
# ============================================================

parallel_expertes = ParallelAgent(
    name="evaluacion_expertos",
    sub_agents=[ethics, psychology, security, legal, ai],
    description="Evalúa el sistema propuesto desde múltiples perspectivas de expertos.",
)

consenso = LoopAgent(
    name="agente_multiexperto_consenso",
    sub_agents=[parallel_expertes, coordinador],
    description="Agente multi-experto que itera hasta alcanzar consenso o máximo número de iteraciones.",
    max_iterations=1,
)

root_agent = SequentialAgent(
    name="news_bulletin_pipeline",
    sub_agents=[consenso, redactor, generador_documentos],
    description="Agente secuencial que coordina la evaluación y generación del informe final.",
)
