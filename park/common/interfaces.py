
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

class ITicketService(ABC):
    """Интерфейс сервиса управления билетами"""
    
    @abstractmethod
    def create_ticket(
        self,
        visitor_id: int,
        purchase_id: int,
        ticket_status: str,
        age_category: str,
        duration_minutes: Optional[int] = None
    ) -> Dict:
        """Создать билет"""
        pass
    
    @abstractmethod
    def calculate_price(self, ticket_type: str, age_category: str) -> float:
        """Рассчитать стоимость билета"""
        pass
    
    @abstractmethod
    def validate_ticket(self, ticket_id: int) -> Dict:
        """Проверить статус билета"""
        pass
    
    @abstractmethod
    def activate_ticket(self, ticket_id: int) -> bool:
        """Активировать билет"""
        pass


class IAccessStrategy(ABC):
    """Интерфейс стратегии контроля доступа"""
    
    @abstractmethod
    def check_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int
    ) -> Tuple[bool, str]:
        """
        Проверить доступ к аттракциону
        
        Returns:
            (разрешено, сообщение)
        """
        pass
    
    @abstractmethod
    def has_priority_access(self, ticket_status: str) -> bool:
        """Проверить наличие приоритетного доступа"""
        pass