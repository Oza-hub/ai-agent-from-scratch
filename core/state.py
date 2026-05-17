class ConversationState:

    def __init__(self):

        # ===== HISTORIAL =====
        self.history = []

        # ===== RESULTADOS =====
        self.results = {}

        # ===== ENTIDADES =====
        self.entities = {}

        # ===== CONTEXTO ACTIVO =====
        self.active_context = {
            "goal": None,
            "entities": []
        }

        # ===== TAREA ACTUAL =====
        self.task = {}

        # ===== FALLAS =====
        self.failures = []

    # =========================
    # HISTORIAL
    # =========================
    def add_user_message(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

    def add_agent_message(self, message):
        self.history.append({
            "role": "assistant",
            "content": message
        })

    def get_history(self, last_n=None):
        if last_n:
            return self.history[-last_n:]
        return self.history

    # =========================
    # RESULTADOS
    # =========================
    def set_result(self, key, value):
        self.results[key] = value

    def get_result(self, key):
        return self.results.get(key)

    # =========================
    # ENTIDADES
    # =========================
    def add_entity(self, name, data):

        key = name.lower()

        if key not in self.entities:
            self.entities[key] = {
                "name": name,
                **data
            }

    def get_entities(self):
        return self.entities

    def get_last_entity(self):
        if not self.entities:
            return None
        return list(self.entities.values())[-1]

    # =========================
    # CONTEXTO ACTIVO (CLAVE)
    # =========================
    def update_active_context(self, goal, entities):

        if goal:
            self.active_context["goal"] = goal

        if entities:
            self.active_context["entities"] = entities[-3:]  # límite

    def get_active_context(self):
        return self.active_context

    # =========================
    # TAREA ACTUAL
    # =========================
    def set_task(self, task_data):
        self.task = task_data

    def get_task(self):
        return self.task

    # =========================
    # FALLAS (APRENDIZAJE)
    # =========================
    def add_failure(self, failure):
        self.failures.append(failure)

    def get_failures(self):
        return self.failures