class AbstractProducer:
    # (Ель, Дуб, Красное дерево)
    material = {
        'spruce': 0.5,
        'oak': 0.7,
        'redwood': 1
    }

    machine_quality = {
        'chinese': 0.5,
        'korean': 0.6,
        'german': 1
    }

    def count_fixed_costs(self) -> float:
        """Считает постоянные затраты производителя"""
        pass

    def count_variable_costs(self) -> int:
        """Считает переменные затраты производителя"""
        pass

    def count_negotiation_costs(self) -> int:
        """Считает цену переговоров"""
        pass

    def count_logistics_costs(self) -> int:
        """Считает расходы на транспортировку заготовок"""
        pass

    def count_proceeds(self) -> int:
        """Считает выручку от продажи заготовок"""
        pass

    def make_deal(self, deal: dict) -> None:
        """Проводит сделку с неким маклером"""
        pass

    def store_billets(self) -> None:
        pass

    def billets_left(self) -> int:
        """Заготовки, оставшиеся на складе производителя"""
        pass

    def count_storage_costs(self) -> int:
        """Считает расходы на хранение заготовок"""
        pass


class ProducerNormal(AbstractProducer):

    def __init__(self, balance):
        self.id = 0
        self.balance = balance
        self.billets_produced = 0
        self.billets_stored = 0
        self.transactions = []
        self.is_bankrupt = False
        self.status = 'OK'

    def count_fixed_costs(self) -> float:
        if self.billets_produced <= 10:
            return 600
        elif self.billets_produced <= 20:
            return 1000
        elif self.billets_produced <= 30:
            return 1400
        elif self.billets_produced <= 50:
            return 2000
        elif self.billets_produced <= 100:
            return 4000

    def count_variable_costs(self) -> int:
        if self.billets_produced <= 10:
            return 110 * self.billets_produced
        elif self.billets_produced <= 20:
            return 100 * self.billets_produced
        elif self.billets_produced <= 30:
            return 85 * self.billets_produced
        elif self.billets_produced <= 50:
            return 70 * self.billets_produced
        elif self.billets_produced <= 100:
            return 60 * self.billets_produced

    def count_storage_costs(self) -> int:
        return self.billets_stored * 50

    def count_logistics_costs(self) -> int:
        costs = 0
        for transaction in self.transactions:
            costs += transaction['terms']['quantity'] * transaction['terms']['transporting_cost']
        return costs

    def count_negotiation_costs(self) -> int:
        return len(self.transactions) * 20

    def make_deal(self, deal: dict) -> None:
        self.transactions.append(deal)
        return

    def count_proceeds(self) -> int:
        proceeds = 0
        for transaction in self.transactions:
            proceeds += transaction['terms']['quantity'] * transaction['terms']['price']
        return proceeds

    @property
    def billets_left(self) -> int:
        billets_requested = 0
        for transaction in self.transactions:
            billets_requested += transaction['terms']['quantity']
        billets_left = self.billets_stored + self.billets_produced - billets_requested
        return billets_left

    def store_billets(self) -> None:
        self.billets_stored = self.billets_left
        self.billets_produced = 0
        return

    def produce(self, billet_amount) -> None:
        self.billets_produced = billet_amount
        return


class ProducerHard(AbstractProducer):
    # FIXME Фиксить нужно вообще всё

    available_materials = {
        'spruce': False,
        'oak': False,
        'redwood': False
    }

    def __init__(self, balance):
        self.balance = balance
        self.billets_produced = (0, 0, 0)
        self.billets_stored = {
            'spruce': [],
            'oak': [],
            'redwood': []
        }
        self.machinery = {
            'chinese': [],
            'korean': [],
            'german': []
        }
        # Предполагается, что данные транзакции прошли все необходимые проверки, как то:
        # 1) На сумму сделки
        # 2) На наличие заготовок у производителя
        # 3) На наличие денег у маклера
        self.transactions = []

    def count_fixed_costs(self) -> float:
        rent_coefficient = 0.93 ** (self.machine[1] - 1)
        base_fixed_costs = 600
        # Для китайских станков
        if self.machinery['chinese'][0] == self.machine_quality['chinese']:
            if self.billets_produced[0] <= 10:
                return (base_fixed_costs + 200) * rent_coefficient
            elif self.billets_produced[0] <= 20:
                return (base_fixed_costs + 350) * rent_coefficient
            elif self.billets_produced[0] <= 30:
                return (base_fixed_costs + 500) * rent_coefficient
            elif self.billets_produced[0] <= 50:
                return (base_fixed_costs + 700) * rent_coefficient
            else:
                raise AttributeError
        # Для корейских станков
        elif self.machine[0] == 0.6:
            if self.billets_produced[0] <= 10:
                return (base_fixed_costs + 350) * rent_coefficient
            elif self.billets_produced[0] <= 20:
                return (base_fixed_costs + 600) * rent_coefficient
            elif self.billets_produced[0] <= 30:
                return (base_fixed_costs + 1000) * rent_coefficient
            elif self.billets_produced[0] <= 50:
                return (base_fixed_costs + 1400) * rent_coefficient
            else:
                raise AttributeError
        # Для немецких станков
        elif self.machine[0] == 1:
            if self.billets_produced[0] <= 10:
                return (base_fixed_costs + 500) * rent_coefficient
            elif self.billets_produced[0] <= 20:
                return (base_fixed_costs + 900) * rent_coefficient
            elif self.billets_produced[0] <= 30:
                return (base_fixed_costs + 1300) * rent_coefficient
            elif self.billets_produced[0] <= 50:
                return (base_fixed_costs + 1700) * rent_coefficient
            else:
                raise AttributeError

    def count_variable_costs(self) -> int:
        if self.billets_produced[1] == self.material['spruce']:
            if self.billets_produced[0] <= 10:
                return 80 * self.billets_produced[0]
            elif self.billets_produced[0] <= 20:
                return 75 * self.billets_produced[0]
            elif self.billets_produced[0] <= 30:
                return 70 * self.billets_produced[0]
            elif self.billets_produced[0] <= 50:
                return 65 * self.billets_produced[0]
            else:
                raise AttributeError
        elif self.billets_produced[1] == self.material['oak']:
            if self.billets_produced[0] <= 10:
                return 110 * self.billets_produced[0]
            elif self.billets_produced[0] <= 20:
                return 100 * self.billets_produced[0]
            elif self.billets_produced[0] <= 30:
                return 90 * self.billets_produced[0]
            elif self.billets_produced[0] <= 50:
                return 80 * self.billets_produced[0]
            else:
                raise AttributeError
        elif self.billets_produced[1] == self.material['redwood']:
            if self.billets_produced[0] <= 10:
                return 160 * self.billets_produced[0]
            elif self.billets_produced[0] <= 20:
                return 150 * self.billets_produced[0]
            elif self.billets_produced[0] <= 30:
                return 135 * self.billets_produced[0]
            elif self.billets_produced[0] <= 50:
                return 110 * self.billets_produced[0]
            else:
                raise AttributeError

    def count_logistics_costs(self) -> int:
        costs = 0
        for transaction in self.transactions:
            costs += transaction['terms']['billets'][0] * transaction['terms']['transporting_cost']
        return costs

    def count_negotiation_costs(self) -> int:
        return len(self.transactions) * 20

    def count_storage_costs(self) -> int:
        return len(self.transactions)

    def count_proceeds(self) -> int:
        proceeds = 0
        for transaction in self.transactions:
            proceeds += transaction['terms']['billets'][0] * transaction['terms']['price']
        return proceeds

    def make_deal(self, deal: dict) -> None:
        self.transactions.append(deal)
        return

    @property
    def billets_left(self) -> int:
        spruce_available = [x for x in self.billets_stored if x[1] == self.material['spruce']]
        oak_available = [x for x in self.billets_stored if x[1] == self.material['oak']]
        redwood_available = [x for x in self.billets_stored if x[1] == self.material['redwood']]
        for transaction in self.transactions:
            spruce_requested = []
            oak_requested = []
            redwood_requested = []
        return 0

    def produce(self, billet_amount, quality) -> None:
        self.billets_produced = (billet_amount, quality, self.machine[0])
        if billet_amount > 0:
            self.billets_stored.append(self.billets_produced)
        return

    def update_machine(self, machine_quality, rent_duration) -> None:
        self.machine = (machine_quality, rent_duration)
        return
