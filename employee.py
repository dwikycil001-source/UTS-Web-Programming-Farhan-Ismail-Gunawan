"""Class OOP untuk data karyawan pada tugas UTS Web Programming."""

from abc import ABC, abstractmethod


# ASUMSI DEMO: dosen belum memberikan persentase resmi untuk kode bonus.
# Persentase berikut hanya aturan contoh agar rule dan override dapat didemonstrasikan.
BONUS_RATES = {
    "PERF2026": 0.05,   # contoh: bonus 5% dari gaji pokok
    "SENIOR10": 0.10,   # contoh: bonus 10% dari gaji pokok
    "LEAD2026": 0.15,   # contoh: bonus 15% dari gaji pokok
}


class Employee(ABC):
    """Class induk yang menyimpan atribut umum karyawan."""

    def __init__(self, emp_id, name, base_salary, is_permanent, bonus_code=None):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = float(base_salary)
        self.is_permanent = bool(is_permanent)
        self.bonus_code = bonus_code

    @property
    def employee_type(self):
        return "Karyawan"

    def calculate_bonus(self):
        """Mengembalikan bonus berdasarkan kode; kode tidak dikenal/tidak ada = 0."""
        rate = BONUS_RATES.get(self.bonus_code, 0.0)
        return self.base_salary * rate

    @abstractmethod
    def calculate_salary(self):
        """Method abstrak yang wajib diimplementasikan oleh class turunan."""
        raise NotImplementedError

    def to_report(self):
        bonus = self.calculate_bonus()
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "employee_type": self.employee_type,
            "base_salary": self.base_salary,
            "bonus_code": self.bonus_code or "-",
            "bonus": bonus,
            "total_salary": self.calculate_salary(),
        }


class PermanentEmployee(Employee):
    """Class turunan untuk karyawan tetap."""

    @property
    def employee_type(self):
        return "Tetap"

    def calculate_salary(self):
        # OVERRIDE: karyawan tetap mendapat gaji pokok + bonus berkode (jika ada).
        return self.base_salary + self.calculate_bonus()


class ContractEmployee(Employee):
    """Class turunan untuk karyawan non-tetap/kontrak."""

    @property
    def employee_type(self):
        return "Non-tetap"

    def calculate_salary(self):
        # OVERRIDE: sesuai aturan demo, karyawan non-tetap menerima gaji pokok saja.
        return self.base_salary


def employee_from_dict(data):
    """Factory: mengubah dictionary JSON menjadi objek karyawan yang sesuai."""
    common = {
        "emp_id": data["emp_id"],
        "name": data["name"],
        "base_salary": data["base_salary"],
        "is_permanent": data["is_permanent"],
        "bonus_code": data.get("bonus_code"),
    }

    if data["is_permanent"]:
        return PermanentEmployee(**common)
    return ContractEmployee(**common)
