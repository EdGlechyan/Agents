
from Effect import Effect
from const import MAX_LEVEL

class Artifact:
    def __init__(self, name, effects):
        self.name = name
        self.effects = effects

    def apply_artifact(self, colony, log):
        """Применение артефакта добавляет его эффекты в список"""
        for effect in self.effects:
            colony.effects.append(effect)
        log.append(f"{colony.name}: Артефакт '{self.name}' применён.")


