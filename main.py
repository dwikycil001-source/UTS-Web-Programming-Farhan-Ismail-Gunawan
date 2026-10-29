"""Program utama UTS Web Programming - OOP dan JSON."""

import json
from pathlib import Path

from employee import employee_from_dict
from sensor import sensor_from_dict


BASE_DIR = Path(__file__).resolve().parent


def load_json(filename, key):
    """Membaca file JSON dan mengembalikan daftar pada key yang diminta."""
    path = BASE_DIR / filename
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise SystemExit(f"File tidak ditemukan: {path.name}")
    except json.JSONDecodeError as error:
        raise SystemExit(f"Format JSON tidak valid di {path.name}: {error}")

    if key not in data or not isinstance(data[key], list):
        raise SystemExit(f"Struktur {path.name} harus memiliki daftar '{key}'.")
    return data[key]


def rupiah(value):
    return "Rp{:,.0f}".format(value).replace(",", ".")


def show_employee_report(employees):
    print("\n" + "=" * 88)
    print("LAPORAN DATA KARYAWAN")
    print("=" * 88)
    permanent_count = sum(1 for item in employees if item.is_permanent)
    contract_count = len(employees) - permanent_count
    total_payroll = sum(item.calculate_salary() for item in employees)

    print(f"Total karyawan       : {len(employees)}")
    print(f"Karyawan tetap       : {permanent_count}")
    print(f"Karyawan non-tetap   : {contract_count}")
    print(f"Total estimasi gaji  : {rupiah(total_payroll)}")
    print("\nRINCIAN GAJI")
    print("-" * 88)
    print(f"{'ID':<10} {'Nama':<22} {'Jenis':<12} {'Gaji Pokok':>15} {'Bonus':>13} {'Total':>15}")
    print("-" * 88)

    for employee in employees:
        report = employee.to_report()
        print(
            f"{report['emp_id']:<10} "
            f"{report['name']:<22.22} "
            f"{report['employee_type']:<12} "
            f"{rupiah(report['base_salary']):>15} "
            f"{rupiah(report['bonus']):>13} "
            f"{rupiah(report['total_salary']):>15}"
        )

    print("\nCatatan: perhitungan bonus mengikuti asumsi demo yang dijelaskan di README.md.")


def show_sensor_report(sensors):
    print("\n" + "=" * 88)
    print("LAPORAN DATA SENSOR")
    print("=" * 88)

    counts = {"NORMAL": 0, "WARNING": 0, "DANGER": 0}
    mismatches = []

    for sensor in sensors:
        counts[sensor.evaluated_status] += 1
        if sensor.has_status_mismatch():
            mismatches.append(sensor)

    print(f"Total sensor         : {len(sensors)}")
    print(f"Status NORMAL        : {counts['NORMAL']}")
    print(f"Status WARNING       : {counts['WARNING']}")
    print(f"Status DANGER        : {counts['DANGER']}")
    print(f"Status tidak cocok   : {len(mismatches)}")
    print("\nRINCIAN SENSOR")
    print("-" * 88)

    for sensor in sensors:
        report = sensor.to_report()
        match_label = "SESUAI" if report["status_match"] else "BERBEDA"
        print(
            f"{report['sensor_id']} | {report['location']:<15} | "
            f"{report['temperature']:>5.1f} C | "
            f"JSON: {report['reported_status']:<7} | "
            f"Evaluasi: {report['evaluated_status']:<7} | "
            f"Operator: {report['operator']} | {match_label}"
        )
        print(f"  -> {report['message']}")

    unassigned = [item for item in sensors if item.operator_id is None]
    print(f"\nSensor tanpa operator: {len(unassigned)}")
    if unassigned:
        print(", ".join(item.sensor_id for item in unassigned))


def show_oop_summary():
    print("\n" + "=" * 88)
    print("PENERAPAN KONSEP OOP")
    print("=" * 88)
    print("1. Class dan Object : Employee, PermanentEmployee, ContractEmployee, dan class sensor.")
    print("2. Inheritance      : class turunan mewarisi atribut/method class induk.")
    print("3. Polymorphism     : calculate_salary() dan status_message() dipanggil melalui objek berbeda.")
    print("4. Override         : class turunan mengimplementasikan ulang method dari class induk.")
    print("5. Rule             : aturan bonus demo dan evaluasi suhu; detail asumsi ada di README.md.")


def main():
    employee_data = load_json("employee.json", "employees")
    sensor_data = load_json("sensor_logs.json", "readings")

    employees = [employee_from_dict(item) for item in employee_data]
    sensors = [sensor_from_dict(item) for item in sensor_data]

    print("=" * 88)
    print("UTS WEB PROGRAMMING - PYTHON OOP & JSON")
    print("Nama : Farhan Ismail Gunawan")
    print("NIM  : 202504385")
    print("=" * 88)

    show_employee_report(employees)
    show_sensor_report(sensors)
    show_oop_summary()


if __name__ == "__main__":
    main()
