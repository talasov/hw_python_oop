from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Отправка сообщений о тренировке."""

        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOURS_IN_MINUTES = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self,
                           coeff_calorie_1: int = 18,
                           coeff_calorie_2: int = 20) -> float:
        """Получить количество затраченных калорий."""

        avg_speed = (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
        training_time = self.duration * self.HOURS_IN_MINUTES
        count_calories = avg_speed * self.weight / self.M_IN_KM * training_time
        return count_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self,
                           cfcal_1: float = 0.035,
                           cfcal_2: float = 0.029) -> float:
        """Получить количество затраченных калорий."""
        calories = (cfcal_1 * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * cfcal_2) * self.duration * self.HOURS_IN_MINUTES
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.length_pool * self.count_pool / self.M_IN_KM
        return avg_speed / self.duration

    def get_spent_calories(self, cf_1=1.1, cf_2=2) -> float:
        """Получить количество затраченых калорий."""
        return (self.get_mean_speed() + cf_1) * cf_2 * self.weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_types: str, list_data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    from typing import Dict, Type

    dict_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_types in dict_training:
        return dict_training[workout_types](*list_data)
    raise KeyError('Ошибка в типе тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    training_info = training.show_training_info()
    print(training_info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
