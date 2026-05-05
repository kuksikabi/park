
from typing import Dict, Tuple, Optional
from ..interfaces import IAccessStrategy
from ..models import AccessRule, Attraction, Ticket, Visitor, VisitRecord, AuditLog, db
from datetime import datetime

class StandardAccessStrategy(IAccessStrategy):
    """Стратегия для билетов Standard"""
    
    def check_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int
    ) -> Tuple[bool, str]:
        # Проверка по матрице доступа
        rule = AccessRule.query.filter_by(
            ticket_status='standard',
            attraction_category=attraction_category.lower()
        ).first()
        
        if not rule or not rule.is_allowed:
            return False, "Ваш билет не даёт доступа к этой категории аттракционов"
        
        # Проверка возраста
        if visitor_age < attraction_min_age:
            return False, f"Недостаточный возраст. Минимум: {attraction_min_age} лет"
        
        return True, "Доступ разрешён"
    
    def has_priority_access(self, ticket_status: str) -> bool:
        return False


class VIPAccessStrategy(IAccessStrategy):
    """Стратегия для билетов VIP"""
    
    def check_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int
    ) -> Tuple[bool, str]:
        # VIP имеет доступ ко всем категориям
        rule = AccessRule.query.filter_by(
            ticket_status='vip',
            attraction_category=attraction_category.lower()
        ).first()
        
        if rule and not rule.is_allowed:
            return False, "Аттракцион временно недоступен"
        
        # Проверка возраста (строже)
        if visitor_age < attraction_min_age:
            return False, f"Недостаточный возраст. Минимум: {attraction_min_age} лет"
        
        return True, "Доступ разрешён (VIP)"
    
    def has_priority_access(self, ticket_status: str) -> bool:
        return True


class PlatinumAccessStrategy(IAccessStrategy):
    """Стратегия для билетов Platinum"""
    
    def check_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int
    ) -> Tuple[bool, str]:
        # Platinum: почти полный доступ
        # Только абсолютные ограничения по возрасту
        if visitor_age < attraction_min_age:
            return False, f"Абсолютное ограничение: минимум {attraction_min_age} лет"
        
        return True, "Доступ разрешён (Platinum)"
    
    def has_priority_access(self, ticket_status: str) -> bool:
        return True


class AccessControlService:
    """Сервис контроля доступа с паттерном Strategy"""
    
    def __init__(self):
        self.strategies = {
            'standard': StandardAccessStrategy(),
            'vip': VIPAccessStrategy(),
            'platinum': PlatinumAccessStrategy()
        }
    
    def validate_access(
        self,
        ticket_status: str,
        attraction_category: str,
        visitor_age: int,
        attraction_min_age: int,
        remaining_time: Optional[int] = None
    ) -> Dict:
        """Проверить доступ посетителя к аттракциону"""
        
        # Проверка времени билета
        if remaining_time is not None and remaining_time <= 0:
            return {
                'allowed': False,
                'message': 'Время действия билета истекло',
                'priority': False
            }
        
        # Получаем стратегию
        strategy = self.strategies.get(ticket_status.lower())
        if not strategy:
            return {
                'allowed': False,
                'message': f'Неизвестный тип билета: {ticket_status}',
                'priority': False
            }
        
        # Делегируем проверку стратегии
        allowed, message = strategy.check_access(
            ticket_status, attraction_category, visitor_age, attraction_min_age
        )
        
        return {
            'allowed': allowed,
            'message': message,
            'priority': strategy.has_priority_access(ticket_status)
        }
    
    def register_strategy(self, ticket_type: str, strategy: IAccessStrategy):
        """Зарегистрировать кастомную стратегию"""
        self.strategies[ticket_type.lower()] = strategy