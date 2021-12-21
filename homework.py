from typing import Union, Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

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
        pass

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

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:

        coeff_calories_1 = 0.035
        coeff_calories_2 = 0.029

        return (coeff_calories_1
                * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff_calories_2
                * self.weight) * self.duration * self.HOUR_IN_MINUTE


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

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

        coeff_swimm_1 = 1.1
        coeff_swimm_2 = 2

        first_arg = self.get_mean_speed() + coeff_swimm_1

        return first_arg * coeff_swimm_2 * self.weight


def read_package(workout_type: str, data: list) -> Union[Training, str]:
    """Прочитать данные полученные от датчиков."""

    CustomDict = Dict[str, Type[Union[Swimming, Running, SportsWalking]]]

    workout_dict: CustomDict = {'SWM': Swimming,
                                'RUN': Running,
                                'WLK': SportsWalking}

    try:
        return workout_dict[workout_type](*data)

    except KeyError:
        return 'Не найден тип тренировки!'


def main(training: Union[Training, str]) -> None:
    """Главная функция."""

    if isinstance(training, str):
        print(training)
    else:
        info: InfoMessage = training.show_training_info()
        print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('TEST', [0, 0, 0, 0])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
