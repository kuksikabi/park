from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..interfaces import ITicketService
from ..models import Ticket, PriceList, Visitor, Purchase, AuditLog, db

class TicketService(ITicketService):
    """Реализация сервиса управления билетами"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def calculate_price(self, ticket_type: str, age_category: str) -> float:
        """Рассчитать стоимость билета на основе price_list"""
        price_entry = PriceList.query.filter_by(
            ticket_status=ticket_type.lower(),
            age_category=age_category.lower(),
            valid_until=None  # Актуальная цена
        ).order_by(PriceList.valid_from.desc()).first()
        
        if not price_entry:
            raise ValueError(f"Цена не найдена для {ticket_type} + {age_category}")
        
        return float(price_entry.price)
    
    def create_ticket(
        self,
        visitor_id: int,
        purchase_id: int,
        ticket_status: str,
        age_category: str,
        duration_minutes: Optional[int] = None
    ) -> Dict:
        """Создать новый билет после успешной оплаты"""
        from sqlalchemy.exc import IntegrityError
        
        # Валидация
        visitor = Visitor.query.get(visitor_id)
        purchase = Purchase.query.get(purchase_id)
        if not visitor or not purchase:
            raise ValueError("Посетитель или покупка не найдены")
        
        # Расчёт срока действия
        now = datetime.utcnow()
        if duration_minutes:
            valid_until = now + timedelta(minutes=duration_minutes)
            remaining_time = duration_minutes
        else:
            # Бессрочный билет (действует 24 часа)
            valid_until = now + timedelta(days=1)
            remaining_time = None
        
        # Создание билета
        new_ticket = Ticket(
            visitor_id=visitor_id,
            purchase_id=purchase_id,
            status=ticket_status.lower(),
            issue_date=now,
            valid_until=valid_until,
            duration_minutes=duration_minutes,
            remaining_time=remaining_time,
            is_activated=False
        )
        
        try:
            self.db.session.add(new_ticket)
            self.db.session.flush()  # Получаем ID
            
            # Audit log
            audit = AuditLog(
                action='create',
                table_name='tickets',
                record_id=new_ticket.id,
                new_value=f"ticket_id={new_ticket.id}, status={ticket_status}"
            )
            self.db.session.add(audit)
            self.db.session.commit()
            
            return {
                'id': new_ticket.id,
                'status': new_ticket.status,
                'valid_until': new_ticket.valid_until.isoformat(),
                'remaining_time': new_ticket.remaining_time,
                'is_activated': new_ticket.is_activated
            }
        except IntegrityError:
            self.db.session.rollback()
            raise ValueError("Ошибка при создании билета")
    
    def validate_ticket(self, ticket_id: int) -> Dict:
        """Проверить статус и валидность билета"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise ValueError(f"Билет #{ticket_id} не найден")
        
        now = datetime.utcnow()
        is_valid = (
            ticket.is_activated and 
            ticket.valid_until > now and
            (ticket.remaining_time is None or ticket.remaining_time > 0)
        )
        
        return {
            'id': ticket.id,
            'status': ticket.status,
            'is_valid': is_valid,
            'is_activated': ticket.is_activated,
            'valid_until': ticket.valid_until.isoformat(),
            'remaining_time': ticket.remaining_time,
            'message': 'OK' if is_valid else 'Билет недействителен'
        }
    
    def activate_ticket(self, ticket_id: int) -> bool:
        """Активировать билет при первом использовании"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise ValueError(f"Билет #{ticket_id} не найден")
        
        if ticket.is_activated:
            raise ValueError("Билет уже активирован")
        
        if ticket.valid_until < datetime.utcnow():
            raise ValueError("Билет просрочен")
        
        ticket.is_activated = True
        self.db.session.commit()
        return True
    
    def extend_ticket_time(self, ticket_id: int, additional_minutes: int) -> bool:
        """Продлить время действия билета"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise ValueError(f"Билет #{ticket_id} не найден")
        
        # Нельзя продлить билет без ограничения по времени
        if ticket.duration_minutes is None:
            raise ValueError("Этот билет не имеет ограничения по времени")
        
        # Нельзя продлить просроченный билет
        if ticket.valid_until < datetime.utcnow():
            raise ValueError("Нельзя продлить просроченный билет")
        
        # Обновляем время
        ticket.remaining_time = (ticket.remaining_time or 0) + additional_minutes
        ticket.valid_until = datetime.utcnow() + timedelta(minutes=ticket.remaining_time)
        
        self.db.session.commit()
        return True
    
    def get_tickets_by_visitor(self, visitor_id: int) -> List[Dict]:
        """Получить все билеты посетителя"""
        tickets = Ticket.query.filter_by(visitor_id=visitor_id).all()
        return [
            {
                'id': t.id,
                'status': t.status,
                'is_activated': t.is_activated,
                'valid_until': t.valid_until.isoformat(),
                'remaining_time': t.remaining_time,
                'issue_date': t.issue_date.isoformat()
            }
            for t in tickets
        ]