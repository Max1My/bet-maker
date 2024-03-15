from enum import Enum


class StatusBet(Enum):
    NOT_PLAYED_YET = 'NOT_PLAYED_YET', 'Cоответствующее событие ещё не завершилось'
    WIN = 'WIN', 'Cобытие завершилось выигрышем первой команды'
    LOSE = 'LOSE', 'Cобытие завершилось проигрышем первой команды или ничьей'
