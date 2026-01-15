# core/repositories/supplier_repository.py

from core.models import Supplier


class SupplierRepository:
    def get(self, supplier_id):
        return Supplier.objects.get(id=supplier_id)

    def get_all(self):
        return Supplier.objects.all()
