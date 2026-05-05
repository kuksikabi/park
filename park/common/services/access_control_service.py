
from typing import Dict, Tuple
from common.interfaces import IAccessStrategy

class AccessControlService:
    """
    Сервис контроля доступа
    Использует паттерн Strategy для проверки прав доступа
    """
    
    def __init__(self):
        """Инициализация сервиса с регистрацией стратегий"""
        self.strategies: Dict[str, IAccessStrategy] = {}
        # TODO: Зарегистрировать стратегии для standard, vip, platinum
    
    def register_strategy(self, ticket_type: str, strategy: IAccessStrategy):
        """
        Зарегистрировать стратегию для типа билета
        
        Args:
            ticket_type: Тип билета (standard/vip/platinum)
            strategy: Экземпляр стратегии
        """
        self.strategies[ticket_type.lower()] = strategy
    
    def validate_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int,
        remaining_time: int = None
    ) -> Dict:
        """
        Проверить доступ посетителя к аттракциону
        
        Args:
            ticket_status: Тип билета посетителя
            attraction_category: Категория аттракциона
            visitor_age: Возраст посетителя
            attraction_min_age: Минимальный возраст для аттракциона
            remaining_time: Оставшееся время билета (опционально)
        
        Returns:
            Dict {
                'allowed': bool,
                'message': str,
                'priority': bool
            }
        """
        # TODO: Реализовать
        # 1. Получить стратегию по ticket_status
        # 2. Проверить remaining_time (если есть)
        # 3. Вызвать strategy.check_access()
        # 4. Вернуть результат
        pass


class StandardAccessStrategy(IAccessStrategy):
    """Стратегия доступа для билетов Standard"""
    
    def check_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int
    ) -> Tuple[bool, str]:
        """
        Проверка доступа для Standard
        
        TODO: Реализовать логику
        - Проверить access_rules
        - Проверить возраст
        """
        pass
    
    def has_priority_access(self, ticket_status: str) -> bool:
        """Standard не имеет приоритетного доступа"""
        pass


class VIPAccessStrategy(IAccessStrategy):
    """Стратегия доступа для билетов VIP"""
    
    def check_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int
    ) -> Tuple[bool, str]:
        """
        Проверка доступа для VIP
        
        TODO: Реализовать логику
        """
        pass
    
    def has_priority_access(self, ticket_status: str) -> bool:
        """VIP имеет приоритетный доступ"""
        pass


class PlatinumAccessStrategy(IAccessStrategy):
    """Стратегия доступа для билетов Platinum"""
    
    def check_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int
    ) -> Tuple[bool, str]:
        """
        Проверка доступа для Platinum
        
        TODO: Реализовать логику
        """
        pass
    
    def has_priority_access(self, ticket_status: str) -> bool:
        """Platinum имеет приоритетный доступ"""
        pass