# Modbus Data Types and Register Mapping

This document summarizes practical and authoritative usage of data types in Modbus devices, focusing on how real industrial hardware maps data onto Modbus coils and registers.

---

## 1️⃣ Modbus Core Data Model

Modbus defines only two primitive storage types:

| Category | Storage Size | Access Functions | Notes |
|---------|--------------|-----------------|------|
| **Discrete Inputs / Coils** | 1 bit | FC 1,2,5,15 | Boolean values only |
| **Holding / Input Registers** | 16 bits | FC 3,4,6,16 | Default interpretation: **unsigned 16-bit** |

Everything else (8/32/64-bit integers, floats, strings) is a **convention layered on top** of 16-bit registers.

---

## 2️⃣ Data Types Table

| Type Name | Bits | Signed? | Registers Used | Common Use | Notes |
|---|---:|:---:|:--:|:---|---|
| **Bit (Coil/Discrete)** | 1 | N/A | N/A | Very common | Digital I/O, alarms — sometimes packed into bitfields |
| **INT8** | 8 | Yes | 1 | Rare | Stored in low byte; high byte reserved |
| **UINT8** | 8 | No | 1 | Rare | Values: 0–255; packing two per register is possible but not common |
| **INT16** | 16 | Yes | 1 | Very common | Two’s complement |
| **UINT16** | 16 | No | 1 | Very common | The baseline Modbus register type |
| **INT32** | 32 | Yes | 2 | Common | Used for large signed measurements, position, power |
| **UINT32** | 32 | No | 2 | Common | Counters, energy totals, timestamps |
| **INT64** | 64 | Yes | 4 | Rare | High-precision counters; ensure client support |
| **UINT64** | 64 | No | 4 | Rare | Very large accumulators; not widely supported in tooling |
| **FLOAT32** | 32 | N/A | 2 | Very common | IEEE-754 single precision; widespread in energy & sensor data |
| **FLOAT64** | 64 | N/A | 4 | Uncommon | IEEE-754 double precision; only in specialized cases |

---

## 3️⃣ Practical Notes

### 8-bit Values
- Modbus has **no native byte addressing**
- 8-bit data almost always stored in a **full 16-bit register**
- Rarely packed 2-per-register due to SCADA/PLC tooling complexity

### Bitfields
- Common for alarms/status: one 16-bit register → 16 boolean flags
- Reduces address allocation vs coils

### Multi-register Values
- Two and four-word values **must be read atomically**
- Word ordering **varies by vendor**
  - Schema should **separate datatype vs endianness concerns**

---

## 4️⃣ Naming Conventions

| Source | Naming Style |
|---|---|
| Industrial vendors (Schneider, ABB, Janitza) | `INT16`, `UINT32`, `FLOAT32` |
| Libraries (pymodbus/libmodbus) | `uint16`, `float32`, `double` |
| Official Modbus Spec | Only defines **bits** and **16-bit registers** |

> Conclusion: Best practice is to name types by **size** and **signedness**:  
> **INT16, UINT16, INT32, UINT32, FLOAT32, FLOAT64**, etc.

---

## 5️⃣ Key Takeaways

✔ Only **1-bit** and **16-bit** are official Modbus data units  
✔ All larger data types are **conventions** using consecutive registers  
✔ Use **UINT16** and **FLOAT32** as defaults  
✔ Avoid packing **bytes** unless absolutely necessary  
✔ Be explicit about **endianness** in device profiles  

