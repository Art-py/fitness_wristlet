from typing import Dict, Type, Union
from dataclasses import dataclass


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Метод возвращает информацию о тренировке."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MINUTE: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplemented

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        ret_obj = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return ret_obj


class Running(Training):
    """Тренировка: бег."""

    COEF_RUN_1: int = 18
    COEF_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        first_arg = self.COEF_RUN_1 * self.get_mean_speed() - self.COEF_RUN_2
        second_arg = (self.duration * self.HOUR_IN_MINUTE)
        return first_arg * self.weight / self.M_IN_KM * second_arg


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_CALORIES_1: float = 0.035
    COEF_CALORIES_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        avr_speed_squared = self.get_mean_speed() ** 2 // self.height
        work_time_in_min = self.duration * self.HOUR_IN_MINUTE
        return ((self.COEF_CALORIES_1 * self.weight + avr_speed_squared
                * self.COEF_CALORIES_2 * self.weight) * work_time_in_min)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEF_SWIMM_1: int = 1.1
    COEF_SWIMM_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        first_arg = self.length_pool * self.count_pool
        return first_arg / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        first_arg = self.get_mean_speed() + self.COEF_SWIMM_1
        return first_arg * self.COEF_SWIMM_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    custom_dict = Dict[str, Type[Training]]
    workout_dict: custom_dict = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking}
    try:
        ret_obj = workout_dict[workout_type](*data)
    except KeyError:
        ret_obj = 'Unknown type of workout'
    return ret_obj


def main(training: Union[Training, str]) -> None:
    """Главная функция."""

    if isinstance(training, Training):
        info: InfoMessage = training.show_training_info()
        print(InfoMessage.get_message(info))
    else:
        print(training)


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180]),
                ('ERR', [0, 0, 0, 0])]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
