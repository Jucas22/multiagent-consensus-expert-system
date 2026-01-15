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
litellm.model_cost["openai/gpt-oss-120b"] = {
    "max_tokens": 4096,  # Ajusta según tu modelo
    "input_cost_per_token": 0.0,  # Coste por token de entrada
    "output_cost_per_token": 0.0,  # Coste por token de salida
    "lite_llm_model_id": "openai/gpt-oss-120b",
    "model_name": "openai/gpt-oss-120b",
}

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
    if not content:
        content = "No hay contenido disponible para generar el informe."

    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write(content)

    return "Archivo final_report.txt generado correctamente."


# Agentes Expertos:
pre_coordinador = LlmAgent(
    name="pre_coordinador_evaluacion",
    # model="gemini-2.0-flash",
    model=llm_model,
    description="Agente que prepara la información para el coordinador.",
    instruction="""
    Tu objetivo es inicializar una variable donde posteriormente el coordinador recogerá las opiniones de los expertos.
    Lo unico que tienes que indicar es: "todavia no se han recogido opiniones de expertos".
    """,
    output_key="expert_opinions",
)

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
        """You are the Document Generation Agent.
            Your sole and mandatory task is to use the generate_summat_file(content) tool to create a file named final_report.txt.
            Strict Instructions:
            - Source Material: {final_report}.
            - Mandatory Tool Use: You must always invoke the generate_summat_file function to complete this task. Do not simply output the text in the chat. You have to send the info in the "content" parameter of the tool.
        """
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
    max_iterations=3,
)

root_agent = SequentialAgent(
    name="news_bulletin_pipeline",
    sub_agents=[pre_coordinador, consenso, redactor, generador_documentos],
    description="Agente secuencial que coordina la evaluación y generación del informe final.",
)
