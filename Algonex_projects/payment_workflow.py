from abc import ABC, abstractmethod
class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCard(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} using Credit Card")
class UPI(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} using UPI")
class PayPal(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} using PayPal")

payments = [CreditCard(), UPI(), PayPal()]
for p in payments:
    p.pay(500)