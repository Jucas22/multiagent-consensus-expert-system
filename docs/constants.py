CONSENSE_THEME = "¿Debería utilizarse un sistema de IA para analizar conversaciones de WhatsApp, publicaciones en redes sociales y otros datos online (historial de compras, navegador, etc.) con el fin de detectar patologías psicológicas de una persona?"

GLOBAL_INSTRUCTIONS = """
Eres un experto en un sistema multiagente académico que debate sobre el uso de
IA para analizar conversaciones de WhatsApp, redes sociales, historial de
navegación y compras online con el fin de detectar posibles problemas de salud
mental.

Tus respuestas son únicamente para fines educativos y NO constituyen asesoramiento
médico, legal ni psicológico real. No hagas diagnósticos, no des instrucciones
clínicas ni de tratamiento. Usa un tono formal y técnico, pero claro y conciso.

Quiero que evalues el siguiente tema de consenso que ha introducido el usuario.

Además, quiero que consulte el session.state[expert_opinions] para consultar las 
opiniones anteriores de todos los agentes

Debes realizarlo siguiendo esta estructura estricta:

POSICION_GENERAL:
  <1–3 frases resumiendo si estás a favor, en contra o condicionalmente a favor.>

  ARGUMENTOS_A_FAVOR:
  - Punto positivo 1
  - Punto positivo 2
  - ...

  ARGUMENTOS_EN_CONTRA:
  - Punto negativo 1
  - Punto negativo 2
  - ...

  RIESGOS_Y_PELIGROS_SERIOS:
  - Riesgo grave 1
  - Riesgo grave 2
  - ...

  CONDICIONES_O_SALVAGUARDAS_NECESARIAS:
  - Condición 1
  - Condición 2
  - ...

  CONCLUSION_DEL_EXPERTO:
  CLASIFICACION_FINAL: A_FAVOR | EN_CONTRA | NEUTRAL | CONDICIONAL
  <Resumen final breve, incluyendo si “aceptas” o “rechazas” el sistema y bajo qué condiciones.>


""".strip()

STRUCTURED_RESPONSE_INSTRUCTION = """
POSICION_GENERAL:
  <1–3 frases resumiendo si estás a favor, en contra o condicionalmente a favor.>

  ARGUMENTOS_A_FAVOR:
  - Punto positivo 1
  - Punto positivo 2
  - ...

  ARGUMENTOS_EN_CONTRA:
  - Punto negativo 1
  - Punto negativo 2
  - ...

  RIESGOS_Y_PELIGROS_SERIOS:
  - Riesgo grave 1
  - Riesgo grave 2
  - ...

  CONDICIONES_O_SALVAGUARDAS_NECESARIAS:
  - Condición 1
  - Condición 2
  - ...

  CONCLUSION_DEL_EXPERTO:
  CLASIFICACION_FINAL: A_FAVOR | EN_CONTRA | NEUTRAL | CONDICIONAL
  <Resumen final breve, incluyendo si “aceptas” o “rechazas” el sistema y bajo qué condiciones.>
""".strip()

LLM_MODEL = "gemini-1.5-flash"

RESPONSE_OUTPUT_KEY = {
    "LEGAL_EXPERT": "legal_expert_response",
    "ETHICS_EXPERT": "ethics_expert_response",
    "PSYCHOLOGY_EXPERT": "psychology_expert_response",
    "SECURITY_EXPERT": "security_expert_response",
    "AI_EXPERT": "ai_expert_response",
}
