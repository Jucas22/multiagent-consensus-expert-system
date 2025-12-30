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

## Debate workflow

Primero, cada agente experto proporciona su opinión inicial sobre el tema planteado. Luego, se recopilan todas las opiniones y se resumen en un formato conciso. A continuación, cada agente revisa su opinión inicial a la luz del resumen de las opiniones de los demás agentes. Este proceso de revisión puede repetirse varias veces para fomentar un debate más profundo y refinado entre los agentes expertos.

## Estructura de consenso con coordinador central

En esta arquitectura, el consenso entre expertos se consigue mediante un **coordinador central** y una **pizarra común de acuerdo**, en varias rondas de debate. A continuación se explica en qué consiste y cómo se orquesta el código.

---

### 1. Idea general

- Hay varios **agentes expertos** (Ética, Privacidad, Psicología, Legal, …).
- Cada experto:
  - recibe el **tema**,
  - produce una **opinión estructurada** (con secciones fijas: POSICION_GENERAL, ARGUMENTOS_A_FAVOR, etc.).
- Un **agente coordinador**:
  - recoge todas las opiniones,
  - las **resume** y las **organiza**,
  - mantiene una **“pizarra común”** con:
    - puntos ya consensuados,
    - puntos en conflicto,
    - cuestiones abiertas.
- En cada ronda:
  - el coordinador envía a los expertos:
    - el **resumen global del debate**,
    - el estado actualizado de la **pizarra común**.
  - cada experto revisa su postura (`revise_opinion`) teniendo en cuenta:
    - los puntos acordados,
    - las objeciones y riesgos que han señalado otros.

Tras varias rondas, se obtiene un estado en el que:
- hay un conjunto de **puntos de acuerdo**,
- un conjunto de **condiciones mínimas**,
- y una **posición global consensuada**.

Ese estado se usa para generar el **documento de consenso final**.

---

### 2. Componentes principales en código

#### 2.1. Agentes expertos

- Clases concretas (p. ej. `EthicExpertAgent`, `PrivacyExpertAgent`, etc.) que:
  - heredan de una `BaseExpertAgent`,
  - implementan los métodos:
    - `initial_opinion(topic: str) -> str`
    - `revise_opinion(topic: str, resumen_global: str, pizarra: dict) -> str`
- Sus respuestas siguen siempre la **plantilla común** (secciones fijas).

#### 2.2. Coordinador

- Puede ser:
  - una clase `CoordinatorAgent` (que use LLM/ADK), o
  - un módulo de funciones en `workflow/debate_workflow.py` + `workflow/consensus_strategy.py`.
- Responsabilidades:
  - Recibir todas las respuestas de los expertos.
  - Extraer y agrupar la información por secciones:
    - argumentos a favor, en contra, riesgos, condiciones…
  - Actualizar la **pizarra común de consenso**.
  - Generar un **resumen global** claro que se enviará a todos los expertos.

#### 2.3. Pizarra común de consenso

Estructura de datos compartida (por ejemplo, un `dict`) que representa el estado del consenso:

```python
pizarra = {
    "puntos_acordados": [
        # frases o ideas en las que varios expertos coinciden
    ],
    "puntos_en_conflicto": [
        # temas donde hay desacuerdo claro entre expertos
    ],
    "preguntas_abiertas": [
        # cuestiones que aún no se han resuelto
    ]
}
```

Esta pizarra se **actualiza en cada ronda** y se pasa como contexto adicional a los expertos cuando revisan su opinión.

---

### 3. Orquestación del código (flujo por rondas)

#### 3.1. Ronda inicial – Opiniones independientes

1. El archivo principal (`consenso_expertos_prac.py`) pide el **tema** o usa uno por defecto.
2. Crea los **expertos** (lista de instancias).
3. Llama a `run_debate_workflow(topic, experts)`.

En `run_debate_workflow`:

```python
# Ronda 0: opiniones iniciales
initial_opinions = {}
for expert in experts:
    salida = expert.initial_opinion(topic)
    initial_opinions[expert.role_name] = salida
```

Cada `salida` es un texto estructurado por secciones.

#### 3.2. Coordinación y creación de la pizarra (después de la ronda inicial)

4. El coordinador procesa `initial_opinions`:
   - lee todas las secciones,
   - extrae:
     - puntos repetidos → `puntos_acordados`,
     - contradicciones claras → `puntos_en_conflicto`,
     - dudas no resueltas → `preguntas_abiertas`.

5. Con esto genera:
   - un **resumen global** del estado del debate,
   - una **pizarra inicial**.

Ejemplo de pseudocódigo:

```python
pizarra = construir_pizarra(initial_opinions)
resumen_global = resumir_debate(topic, initial_opinions, pizarra)
```

#### 3.3. Rondas de revisión iterativa

6. Se entra en un bucle de rondas (por ejemplo, 2 o 3 iteraciones):

```python
current_opinions = initial_opinions
history = []

for round_idx in range(1, max_rounds + 1):
    # Guardar estado de la ronda anterior
    history.append({
        "round": round_idx,
        "opinions": current_opinions,
        "resumen_global": resumen_global,
        "pizarra": pizarra,
    })

    # Cada experto revisa su opinión con el contexto global
    new_opinions = {}
    for expert in experts:
        salida = expert.revise_opinion(topic, resumen_global, pizarra)
        new_opinions[expert.role_name] = salida

    current_opinions = new_opinions

    # El coordinador vuelve a analizar las nuevas opiniones
    pizarra = construir_pizarra(current_opinions)
    resumen_global = resumir_debate(topic, current_opinions, pizarra)

    # Opcional: comprobar si ya hay suficiente consenso para terminar antes
    if hay_consenso_suficiente(pizarra, current_opinions):
        break
```

En cada iteración:

- El **resumen global** y la **pizarra** se van afinando.
- Los expertos ajustan sus posturas:
  - aceptan algunos puntos,
  - proponen condiciones adicionales,
  - o señalan conflictos que consideran inaceptables.

#### 3.4. Resultado final del workflow

7. Al terminar el bucle, el workflow devuelve una estructura con toda la información relevante:

```python
debate_result = {
    "topic": topic,
    "initial_opinions": initial_opinions,
    "final_opinions": current_opinions,
    "history": history,
    "pizarra_final": pizarra,
    "resumen_final": resumen_global,
}
```

---

### 4. Generación del documento de consenso

8. El módulo `workflow/document_generator.py` recibe `topic` y `debate_result`:

```python
doc = generate_consensus_document(topic, debate_result)
```

Con esa información, construye un documento (por ejemplo en Markdown) con las secciones que pide la práctica:

- **Tema debatido** → `topic`
- **Resumen del proceso de debate** → usa `history` y los resúmenes de cada ronda
- **Decisión consensuada** → se basa en `pizarra_final` y las conclusiones de los expertos
- **Recomendación final justificada** → integra:
  - los puntos acordados,
  - las condiciones mínimas,
  - referencias a riesgos que han sido tenidos en cuenta.

Finalmente, el archivo principal guarda el documento en `outputs/` y termina la ejecución.

---

### 5. Resumen de la orquestación

1. Entrada del usuario: **tema**.
2. Ronda 0:
   - Cada experto → `initial_opinion(topic)` (opiniones independientes, estructuradas).
3. Coordinador:
   - procesa todas las salidas,
   - construye un **resumen global** y una **pizarra común**.
4. Rondas iterativas:
   - expertos → `revise_opinion(topic, resumen_global, pizarra)`,
   - coordinador → actualiza resumen y pizarra.
5. Criterio de parada:
   - número máximo de rondas alcanzado,
   - o consenso suficiente detectado.
6. Generación del **documento final de consenso** a partir de:
   - tema,
   - historial de debate,
   - pizarra final,
   - conclusiones de los expertos.

Esta es la estructura de consenso basada en un **coordinador central y una pizarra común**, tal y como se usará en el código de la práctica.


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
