from const import MAX_LEVEL

class Effect:
    def __init__(self, effect_type, value, duration, name, target_colony_func=None, duration_type='rounds', experience_base=None):
        self.effect_type = effect_type
        self.value = value
        self.duration = duration
        self.name = name
        self.duration_type = duration_type
        self.target_colony_func = target_colony_func
        self.experience_base = experience_base
        self.applied = False

    def apply(self, colony, log, cycle_number, iteration_number):
        if self.duration_type == 'once' and self.applied:
            return
        if self.duration_type == 'until_next_event' and self.applied:
            return
        if self.effect_type == 'income':
            colony.income += colony.income * (self.value / 100)
            log.append(f"{colony.name}: Доход увеличен на {self.value}%.")
        elif self.effect_type == 'expenses':
            colony.expenses -= colony.expenses * (self.value / 100)
            colony.expenses = max(1, colony.expenses)
            log.append(f"{colony.name}: Расходы уменьшены на {self.value}%.")
        elif self.effect_type == 'balance':
            colony.balance += colony.balance * (self.value / 100)
            log.append(f"{colony.name}: Баланс увеличен на {self.value}%.")
        elif self.effect_type == 'level':
            colony.level = MAX_LEVEL
            colony.status = "Максимальный уровень"
            log.append(f"{colony.name}: Уровень установлен на {colony.level}. Статус: {colony.status}.")
        elif self.effect_type == 'balance_fixed':
            colony.balance += self.value
            log.append(f"{colony.name}: Баланс увеличен на {self.value}.")
        elif self.effect_type == 'expenses_fixed':
            colony.expenses -= self.value
            colony.expenses = max(0, colony.expenses)
            log.append(f"{colony.name}: Расходы уменьшены на {self.value}.")
        elif self.effect_type == 'income_fixed':
            colony.income += self.value
            log.append(f"{colony.name}: Доход увеличен на {self.value}.")
        elif self.effect_type == 'experience':
            experience_gain = int(self.experience_base * (self.value / 100))
            colony.experience += experience_gain
            log.append(f"{colony.name}: Получено {experience_gain} опыта.")
        elif self.effect_type == 'experience_fixed':
            colony.experience += self.value
            log.append(f"{colony.name}: Получено {self.value} опыта.")
        elif self.effect_type == 'zero_experience':
            if self.target_colony_func:
                self.target_colony = self.target_colony_func(colony)
            if self.target_colony:
                self.target_colony.experience = 0
                log.append(f"{self.target_colony.name}: Опыт обнулен.")
            else:
                log.append(f"Не удалось найти соперника для обнуления опыта.")
        elif self.effect_type == 'balance_multiply':
            colony.balance *= self.value
            log.append(f"{colony.name}: Баланс умножен на {self.value}.")
        self.applied = True

    def rollback(self, colony, log):
        if self.effect_type == 'income':
            colony.income -= colony.income * (self.value / 100)
            log.append(f"{colony.name}: Эффект на доход ({self.value}%) снят.")
        elif self.effect_type == 'expenses':
            colony.expenses += colony.expenses * (self.value / 100)
            log.append(f"{colony.name}: Эффект на расходы ({self.value}%) снят.")
        elif self.effect_type == 'balance':
            colony.balance -= colony.balance * (self.value / 100)
            log.append(f"{colony.name}: Эффект на баланс ({self.value}%) снят.")
        elif self.effect_type == 'balance_fixed':
            colony.balance -= self.value
            log.append(f"{colony.name}: Эффект на баланс ({self.value}) снят.")
        elif self.effect_type == 'expenses_fixed':
            colony.expenses += self.value
            log.append(f"{colony.name}: Эффект на расходы ({self.value}) снят.")
        elif self.effect_type == 'income_fixed':
            colony.income -= self.value
            log.append(f"{colony.name}: Эффект на доход ({self.value}) снят.")
        elif self.effect_type == 'experience':
            experience_gain = int(self.experience_base * (self.value / 100))
            colony.experience -= experience_gain
            log.append(f"{colony.name}: Эффект на опыт ({experience_gain}) снят.")
        elif self.effect_type == 'experience_fixed':
            colony.experience -= self.value
            log.append(f"{colony.name}: Эффект на опыт ({self.value}) снят.")