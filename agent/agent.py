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
from docs.experts_descriptions import (
    ETIHICS_EXPERT,
    LEGAL_EXPERT,
    PSYCHOLOGY_EXPERT,
    SECURITY_EXPERT,
    AI_EXPERT,
)


# Registrar modelo personalizado en litellm
# litellm.model_cost_map.update(
#     {
#         "gpt-oss-120b": {
#             "max_tokens": 128000,
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


def fetch_opinions(texto: str) -> Dict:
    """Devuelve un diccionario con el texto consolidado de opiniones."""
    return {"opiniones_unidas": texto}


def generate_summat_file(content: str | None = None, session=None) -> str:
    """Escribe el informe final en final_report.txt usando session.state si no se pasa content."""
    if content is None and session is not None and hasattr(session, "state"):
        content = session.state.get("final_report", "")
    if content is None:
        content = ""
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write(content)
    return "Archivo final_report.txt generado correctamente."


# ============================================================
#  1) Agente RECOPILADOR
# ============================================================

ethics = LlmAgent(
    name="agente_etico",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos éticos.",
    instruction=GLOBAL_INSTRUCTIONS + "\n\n" + ETIHICS_EXPERT,
    tools=[],
    output_key="ethics_response",
)

psychology = LlmAgent(
    name="agente_psicologia",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos psicológicos.",
    instruction=GLOBAL_INSTRUCTIONS + "\n\n" + PSYCHOLOGY_EXPERT,
    tools=[],
    output_key="psychology_response",
)

security = LlmAgent(
    name="agente_seguridad",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos de seguridad.",
    instruction=GLOBAL_INSTRUCTIONS + "\n\n" + SECURITY_EXPERT,
    tools=[],
    output_key="security_response",
)

legal = LlmAgent(
    name="agente_legal",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos legales.",
    instruction=GLOBAL_INSTRUCTIONS + "\n\n" + LEGAL_EXPERT,
    tools=[],
    output_key="legal_response",
)

ai = LlmAgent(
    name="agente_ia",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que evalúa aspectos técnicos de IA.",
    instruction=GLOBAL_INSTRUCTIONS + "\n\n" + AI_EXPERT,
    tools=[],
    output_key="ai_response",
)

coordinador = LlmAgent(
    name="coordinador_evaluacion",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que recopila opiniones de varios expertos.",
    instruction=(
        "Eres el Agente Coordinador.\n"
        "Debes recopilar las opiniones de los siguientes expertos:\n"
        "1. Agente Ético, opinion en session.state['ethics_response']\n"
        "2. Agente de Psicología, opinion en session.state['psychology_response']\n"
        "3. Agente de Seguridad, opinion en session.state['security_response']\n"
        "4. Agente Legal, opinion en session.state['legal_response']\n"
        "5. Agente de IA, opinion en session.state['ai_response']\n\n"
        "Recupera y une los pros y los contras de todos los expertos.\n"
        "Analiza el contenido que has juntado con la herramienta y genera un resumen, manteniendo los puntos clave y añade un resumen final del consenso.\n"
        "Guarda el resultado en session.state['expert_opinions']."
    ),
    output_key="expert_opinions",
    tools=[],
)

redactor = LlmAgent(
    name="redactor_informe_final",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que redacta el informe final.",
    instruction=(
        "Eres el Agente Redactor.\n"
        "En session.state['expert_opinions'] tienes el resumen de las opiniones de los expertos.\n"
        "Usa esa información para redactar un informe final claro sobre si se debe implementar el sistema propuesto, incluyendo los puntos clave y el consenso final. "
        "Quiero que recojas los principales argumentos, tanto a favor como en contra, los puntos fuertes y ventajas que supondría utilizar un sistema asi, los riesgos que conlleva y cualquier condición o salvaguarda necesaria.\n"
        "El informe final debe tener entre 600 y 900 palabras y guardao en session.state['final_report'].\n"
        "Tras redactarlo, llama explícitamente a la herramienta generate_summat_file(content: str) pasando session.state['final_report'] para escribir final_report.txt."
    ),
    output_key="final_report",
    tools=[generate_summat_file],
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
    description="Pipeline multiagente para generar un boletín de noticias diario.",
)
