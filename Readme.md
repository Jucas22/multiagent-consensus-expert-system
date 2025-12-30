# Practica de consenso entre agentes expertos

En este repositorio se encuentra una práctica desarrollada para un curso de inteligencia artificial, en la cual se implementa un sistema de consenso entre agentes expertos utilizando Python y ADK.
El planteamiento que se va a seguir en esta practica es:
> ¿Debería utilizarse un sistema de IA para analizar conversaciones de WhatsApp, publicaciones en redes sociales y otros datos online (historial de compras, navegador, etc.) con el fin de detectar patologías psicológicas de una persona?

Este planteamiento se encuentra en un contexto para ser utiliado en una app voluntaria de autoayuda psicológica, en la cual el usuario puede recibir un análisis preliminar de su estado psicológico basado en sus interacciones digitales. La idea es que, al detectar posibles señales de patologías psicológicas, la app pueda recomendar al usuario que busque ayuda profesional si es necesario.

Para realizar la practica se estableceran varios agentes expertos, cada uno especializado en un área diferente para que lleguen a un consenso sobre la cuestión planteada. Los agentes expertos serán los siguientes:

- **Experto en ética de la IA**: Evaluará las implicaciones éticas del uso de IA para analizar datos personales y detectar patologías psicológicas.
- **Experto en privacidad de datos**: Analizará las preocupaciones relacionadas con la privacidad y la protección de datos personales en el contexto del análisis de conversaciones y publicaciones en línea.
- **Experto en psicología**: Evaluará la efectividad y precisión del análisis de datos digitales para detectar patologías psicológicas, asi como si es adecuado utilizar este enfoque en una app de autoayuda. Además analizará si la deteccion de patrones en los datos digitales puede ser un indicador fiable de patologías psicológicas.
- **Experto en tecnología de IA**: Evaluará la viabilidad técnica y las limitaciones del uso de IA para analizar grandes volúmenes de datos digitales y detectar patrones relacionados con patologías psicológicas.
- **Experto en legalidad y regulaciones**: Analizará las leyes y regulaciones aplicables al uso de IA para analizar datos personales y detectar patologías psicológicas, incluyendo aspectos como el consentimiento informado y la responsabilidad legal.
- **Experto en economia de la salud**: Evaluará el impacto económico potencial del uso de IA para detectar patologías psicológicas, incluyendo costos y beneficios para los usuarios y el sistema de salud en general.


## División de tareas

### 2.1. Persona A – Infraestructura, orquestación y workflows
Enfocada en el “esqueleto” del sistema.

**Responsabilidades principales**

- **Estructura del proyecto y punto de entrada**
	- Crear repo con estructura básica: `consenso_expertos_prac.py`, `config.py`, carpetas `agents/`, `workflow/`, `guards/`, `outputs/`, `docs/`, etc.
	- Configuración mínima de entorno (requirements, README básico).

- **Clase base de expertos (stub)**
	- Definir `BaseExpertAgent` con métodos:
		- `initial_opinion(self, topic: str) -> str`
		- `revise_opinion(self, topic: str, summary_other_opinions: str) -> str`
	- Sin prompts detallados aún; solo interfaz e integración mínima con ADK.

- **Workflow de debate**
	- Archivo `workflow/debate_workflow.py` con función `run_debate_workflow(topic, experts, max_rounds=2 o 3)`.
	- Lógica: recoger opiniones iniciales, resumir (p. ej., `join`), hacer 1–2 rondas de revisión, devolver dict con tema, opiniones iniciales/finales e historial.

- **Estrategia de consenso (simple)**
	- Archivo `workflow/consensus_strategy.py` con `check_consensus(opinions_dict) -> dict`.
	- Ejemplo: consenso si la mayoría incluye “parcialmente de acuerdo”, o marcar siempre “consenso parcial”.

- **Conexión general en `consenso_expertos_prac.py`**
	- Pedir tema al usuario o usar tema por defecto.
	- Instanciar expertos (de Persona B), llamar a `run_debate_workflow`.
	- Imprimir resultado (documento final lo puede montar Persona B).

> ✅ Se puede hacer casi sin contenido real de los expertos: basta con que Persona B respete la interfaz de `BaseExpertAgent`.

### 2.2. Persona B – Diseño de expertos, prompts de rol y documento final
Enfocada en el “cerebro” del sistema y la documentación de la práctica.

**Responsabilidades principales**

- **Definición de los 4 expertos**
	- En `agents/`: `ethic_expert.py`, `privacy_expert.py`, `psychology_expert.py`, `legal_expert.py`.
	- Cada uno hereda de `BaseExpertAgent` y define `role_name` y `system_prompt` (objetivo, prioridades, restricciones).

- **Guardrails / reglas de seguridad**
	- Archivo `guards/safety_rules.py` con `GLOBAL_SYSTEM_PROMPT` (contexto académico, no clínico).
	- Opcional: truncar respuestas largas, filtrar contenido explícito (aunque sea solo en comentarios).

- **Generación de documento de consenso**
	- Archivo `workflow/document_generator.py` con `generate_consensus_document(topic, debate_result) -> str` que cree `.md` con: Tema debatido, Resumen del proceso, Decisión consensuada, Recomendación final.
	- Inicialmente determinista usando `debate_result["consensus"]` y `debate_result["history"]`; luego se puede añadir un agente “Redactor”.

- **Informe técnico (`docs/informe_tecnico.md`)**
	- Estructura sugerida: introducción y objetivo, arquitectura, roles de expertos, workflow, herramientas y guardrails, limitaciones y extensiones.

- **Tema base y ejemplo de salida**
	- Archivo `docs/ejemplo_tema_y_salida.md` con el tema y una copia de un documento real de consenso desde `outputs/`.

> ✅ Persona B puede trabajar en paralelo: solo necesita la interfaz de `BaseExpertAgent` y la estructura de `debate_result` para `document_generator.py`.
