"""
Datenmodelle für das CRM-System
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Customer:
    id: Optional[int]
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    birthdate: Optional[str]
    notes: Optional[str]
    loyalty_points: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

@dataclass
class Service:
    id: Optional[int]
    name: str
    category: Optional[str]
    duration: Optional[int]  # in Minuten
    price: float
    description: Optional[str]
    active: bool = True
    created_at: Optional[str] = None

@dataclass
class Product:
    id: Optional[int]
    name: str
    category: Optional[str]
    brand: Optional[str]
    price: float
    stock_quantity: int = 0
    min_stock_level: int = 5
    description: Optional[str]
    created_at: Optional[str] = None
    
    @property
    def is_low_stock(self) -> bool:
        return self.stock_quantity <= self.min_stock_level

@dataclass
class Appointment:
    id: Optional[int]
    customer_id: int
    service_id: int
    employee_name: Optional[str]
    appointment_date: str
    appointment_time: str
    duration: Optional[int]
    status: str = "geplant"  # geplant, bestätigt, abgeschlossen, abgesagt
    notes: Optional[str] = None
    created_at: Optional[str] = None
    
    @property
    def datetime_str(self) -> str:
        return f"{self.appointment_date} {self.appointment_time}"

@dataclass
class Sale:
    id: Optional[int]
    customer_id: Optional[int]
    sale_date: str
    sale_time: str
    total_amount: float
    payment_method: Optional[str]
    discount: float = 0.0
    loyalty_points_used: int = 0
    notes: Optional[str] = None
    created_at: Optional[str] = None
    
    @property
    def final_amount(self) -> float:
        return self.total_amount - self.discount

@dataclass
class SaleItem:
    id: Optional[int]
    sale_id: int
    item_type: str  # "service" oder "product"
    item_id: int
    item_name: str
    quantity: int = 1
    price: float = 0.0

@dataclass
class Voucher:
    id: Optional[int]
    code: str
    customer_id: Optional[int]
    amount: float
    used: bool = False
    valid_until: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class Employee:
    id: Optional[int]
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    role: Optional[str]
    active: bool = True
    created_at: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

