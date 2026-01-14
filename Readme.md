# Informe técnico de arquitectura (sistema multiagente de consenso)

Este documento describe la arquitectura del sistema multiagente que genera un informe consensuado sobre el uso de IA para analizar datos de WhatsApp/redes con fines de detección de riesgos psicológicos. La extensión está optimizada para caber en un máximo de dos páginas.

## 1. Objetivo y alcance

- Tema evaluado (docs/constants.py): ¿Debe usarse IA para analizar conversaciones y otros datos online con fines de detección psicológica?
- Salida esperada: informe de 600-900 palabras en final_report.txt, redactado en español, tono formal/técnico.
- Enfoque: deliberación multiagente con roles especializados, coordinación central y redacción final automatizada.

## 2. Visión general de la arquitectura

- Núcleo en agent/agent.py usando google.adk: LlmAgent, ParallelAgent, LoopAgent y SequentialAgent.
- Backend LLM: LiteLlm configurado contra https://api.poligpt.upv.es/v1 (model="openai/gpt-oss-120b"), con litellm debug activado para trazas detalladas.
- Composición en tres etapas:
  1) Paralelización de opiniones expertas.
  2) Coordinación y síntesis inicial.
  3) Redacción y persistencia del informe.

## 3. Componentes principales

- Expertos (LlmAgent): ética, psicología, seguridad, legal, IA. Cada uno combina su prompt de rol (docs/experts_descriptions.py) con GLOBAL_INSTRUCTIONS (docs/constants.py), generando salidas estructuradas en session.state[`<dominio>_response`].
- ParallelAgent evaluacion_expertos: ejecuta a todos los expertos en paralelo para maximizar cobertura de perspectivas.
- LlmAgent coordinador: instrucciones en COORDINATOR_AGENT; lee las salidas de los expertos, identifica pros/contras y áreas de acuerdo/conflicto. Puede usar fetch_opinions(texto) como stub de fusión (devuelve el texto en un diccionario).
- LoopAgent agente_multiexperto_consenso: orquesta [evaluacion_expertos, coordinador]; permite iterar hasta consenso (max_iterations=3) aunque el flujo actual suele converger en la primera pasada.
- LlmAgent redactor: aplica REDACTOR_AGENT para convertir expert_opinions en un informe cohesivo con estructura de 4 secciones (tema, resumen del debate, decisión, recomendación) y control de longitud.
- LlmAgent generador_documentos: instruido para invocar siempre generate_summat_file(content) y persistir final_report.txt en UTF-8.
- Herramientas internas (agent/agent.py):
  - generate_summat_file(content=None, session=None): escribe final_report.txt tomando content o session.state["final_report"].
  - fetch_opinions(texto): stub que devuelve {"opiniones_unidas": texto}; no realiza fusión real.

## 4. Flujo de datos y estado

1) Entrada implícita: el tema viene fijado en CONSENSE_THEME. No se recibe dataset; el sistema trabaja a nivel de razonamiento.
2) Paralelización: cada experto genera una opinión estructurada y la deja en session.state bajo su clave `<dominio>_response`.
3) Coordinación: el coordinador lee todas las claves anteriores, sintetiza pros/contras y produce expert_opinions.
4) Consenso iterado: LoopAgent puede repetir el ciclo expertos→coordinador hasta max_iterations.
5) Redacción: el redactor consume expert_opinions y escribe final_report en session.state.
6) Persistencia: generador_documentos guarda final_report.txt mediante generate_summat_file.

## 5. Convenciones de prompting

- Idioma: español, tono formal/técnico.
- Formato exigido por GLOBAL_INSTRUCTIONS: secciones POSICION_GENERAL, ARGUMENTOS_A_FAVOR, ARGUMENTOS_EN_CONTRA, RIESGOS_Y_PELIGROS_SERIOS, CONDICIONES_NECESARIAS_PARA_LA_IMPLEMENTACION, CONCLUSION_DEL_EXPERTO, CLASIFICACION_FINAL.
- El redactor sigue un esquema de 4 apartados con rangos de palabras para asegurar el total (600-900).

## 6. Configuración y dependencias

- LLM: LiteLlm con model="openai/gpt-oss-120b" y api_base poligpt.upv.es. .env se carga, pero la api_key y api_base están hardcodeadas en agent/agent.py (riesgo de exposición).
- constants.LLM_MODEL = "gemini-1.5-flash" no se usa; el modelo efectivo es el anterior.
- Dependencias principales: google.adk, litellm, python-dotenv. main.py está vacío; el entrypoint práctico es agent/agent.py.

## 7. Ejecución

Ejemplo mínimo desde la raíz del proyecto:

```
python - <<"PY"
from agent.agent import root_agent
print(root_agent.run())
PY
```

Notas:
- root_agent es un SequentialAgent que ejecuta [consenso, redactor, generador_documentos].
- Si se requiere estado inicial explícito para google.adk, se pasa como root_agent.run(initial_state={...}).
- final_report.txt se escribe en la raíz del repositorio.

## 8. Extensibilidad

- Añadir un experto: definir prompt en docs/experts_descriptions.py, crear LlmAgent con GLOBAL_INSTRUCTIONS, output_key único, incluirlo en ParallelAgent y actualizar COORDINATOR_AGENT para leer su salida.
- Cambiar modelo: actualizar llm_model en agent/agent.py y considerar externalizar api_key/api_base a variables de entorno.
- Iteraciones de consenso: ajustar max_iterations en agente_multiexperto_consenso si se desea mayor número de rondas.

## 9. Riesgos y limitaciones

- Seguridad: clave API incrustada; debe externalizarse antes de distribuir el código.
- Fusión limitada: fetch_opinions es un stub; la consolidación depende enteramente del LlmAgent coordinador.
- Validación: no existen tests automatizados ni comprobación programática de la longitud del informe final.
- Dependencia de LLM: calidad del consenso y redacción sujeta a respuestas del modelo remoto.

## 10. Archivos relevantes

- agent/agent.py: definición de agentes, orquestación y herramientas.
- docs/constants.py: tema, plantillas y claves de respuesta.
- docs/experts_descriptions.py: descripciones de roles y plantillas de prompts.
- final_report.txt: salida generada.

