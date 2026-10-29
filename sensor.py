"""Class OOP untuk memvalidasi dan melaporkan data sensor suhu."""

from abc import ABC, abstractmethod


# ASUMSI DEMO: ambang berikut dipakai untuk mengevaluasi suhu.
# NORMAL  : suhu < 60
# WARNING : 60 <= suhu < 80
# DANGER  : suhu >= 80
# Ambang ini bukan standar industri; sesuaikan jika dosen memberi rule resmi.
WARNING_THRESHOLD = 60.0
DANGER_THRESHOLD = 80.0


class SensorReading(ABC):
    """Class induk untuk pembacaan sensor."""

    def __init__(self, sensor_id, location, temperature, reported_status, operator_id=None):
        self.sensor_id = sensor_id
        self.location = location
        self.temperature = float(temperature)
        self.reported_status = str(reported_status).upper()
        self.operator_id = operator_id

    @property
    @abstractmethod
    def evaluated_status(self):
        """Status hasil evaluasi berdasarkan suhu."""
        raise NotImplementedError

    @abstractmethod
    def status_message(self):
        """Pesan yang berbeda sesuai status sensor (polymorphism/override)."""
        raise NotImplementedError

    def has_status_mismatch(self):
        return self.reported_status != self.evaluated_status

    def operator_label(self):
        return str(self.operator_id) if self.operator_id is not None else "Belum ditetapkan"

    def to_report(self):
        return {
            "sensor_id": self.sensor_id,
            "location": self.location,
            "temperature": self.temperature,
            "reported_status": self.reported_status,
            "evaluated_status": self.evaluated_status,
            "operator": self.operator_label(),
            "message": self.status_message(),
            "status_match": not self.has_status_mismatch(),
        }


class NormalSensor(SensorReading):
    @property
    def evaluated_status(self):
        return "NORMAL"

    def status_message(self):
        return "Suhu berada pada rentang normal."


class WarningSensor(SensorReading):
    @property
    def evaluated_status(self):
        return "WARNING"

    def status_message(self):
        return "Peringatan: suhu meningkat, perlu dipantau."


class DangerSensor(SensorReading):
    @property
    def evaluated_status(self):
        return "DANGER"

    def status_message(self):
        return "BAHAYA: suhu tinggi, segera periksa kondisi lokasi."


def sensor_from_dict(data):
    """Membuat subclass sensor berdasarkan rule suhu."""
    temperature = float(data["temperature"])
    common = {
        "sensor_id": data["sensor_id"],
        "location": data["location"],
        "temperature": temperature,
        "reported_status": data["status"],
        "operator_id": data.get("operator_id"),
    }

    if temperature >= DANGER_THRESHOLD:
        return DangerSensor(**common)
    if temperature >= WARNING_THRESHOLD:
        return WarningSensor(**common)
    return NormalSensor(**common)
