# MDI VERSION HISTORY

MODBUS-DATA-INTELLIGENCE development history and roadmap.

---

## Current development series

### v0.0.0 — Initial project structure

Status: COMPLETED

- [✅] Initial repository structure.
- [✅] Public and local directory separation.
- [✅] Python package structure.
- [✅] Base README.
- [✅] MIT License.
- [✅] Initial `.gitignore`.

---

### v0.0.1 — Logging and configuration

Status: COMPLETED

- [✅] Reusable `LogMaster`.
- [✅] Terminal logs with ANSI colors.
- [✅] Clean persistent `.log` file.
- [✅] LOCAL and DEMO log environments.
- [✅] Local JSON configuration loader.
- [✅] Public DEMO configuration loader.
- [✅] Controlled configuration errors.

---

### v0.0.2 — Modbus connection layer

Status: COMPLETED

- [✅] PyModbus dependency.
- [✅] `ModbusLocalConnection`.
- [✅] `ModbusDemoConnection`.
- [✅] Fake DEMO Modbus client.
- [✅] Client creation.
- [✅] Connection opening.
- [✅] Connection status check.
- [✅] Controlled connection closing.
- [✅] Controlled network and configuration errors.
- [✅] LOCAL and DEMO manual tests.

---

### v0.0.3 — Connection selector

Status: COMPLETED

- [✅] Select LOCAL or DEMO mode.
- [✅] Return one common connection object.
- [✅] Prevent unknown connection modes.
- [✅] Validate DEMO selection.
- [✅] Validate LOCAL selection.
- [✅] Register selector events through LogMaster.
- [✅] Add neutral SYSTEM log environment.
- [✅] Prepared for terminal debug mode and future PySide6 selection.

---

### v0.0.4 — DEMO collector

Status: PENDING

- [  ] Create `DemoCollector`.
- [  ] Open DEMO connection.
- [  ] Acquire one snapshot.
- [  ] Generate simulated register values.
- [  ] Record collector events.
- [  ] Close the collector safely.

---

### v0.0.5 — Snapshot system

Status: PENDING

- [  ] Define snapshot structure.
- [  ] Add timestamp.
- [  ] Store raw Modbus registers.
- [  ] Convert raw register values.
- [  ] Validate incomplete snapshots.
- [  ] Support LOCAL and DEMO snapshots.

---

### v0.0.6 — Continuous collector

Status: PENDING

- [  ] Configurable acquisition interval.
- [  ] Start snapshot loop.
- [  ] Stop snapshot loop safely.
- [  ] Keep Modbus connection open during collection.
- [  ] Handle communication failures.
- [  ] Controlled reconnection.
- [  ] Prevent duplicate collector loops.

---

### v0.0.7 — Data persistence

Status: PENDING

- [  ] JSON snapshot storage.
- [  ] SQLite database.
- [  ] Database schema.
- [  ] Snapshot insertion.
- [  ] Query historical records.
- [  ] Controlled database errors.

---

### v0.0.8 — Testing system

Status: PENDING

- [  ] Modular component tests.
- [  ] Central test runner.
- [  ] Tests returning `True` or `False`.
- [  ] Configuration tests.
- [  ] Modbus connection tests.
- [  ] Collector tests.
- [  ] Shell script for complete test execution.

---

### v0.0.9 — Initial PySide6 interface

Status: PENDING

- [  ] Main application window.
- [  ] LOCAL / DEMO mode selector.
- [  ] Connect button.
- [  ] Start collector button.
- [  ] Stop collector button.
- [  ] Disconnect button.
- [  ] Connection status display.
- [  ] Snapshot status display.
- [  ] Collector execution outside the GUI thread.

---

## v0.1.0 — First functional Alpha

Status: PLANNED

Target requirements:

- [  ] LOCAL and DEMO operation modes.
- [  ] Stable Modbus connection lifecycle.
- [  ] Individual snapshots.
- [  ] Continuous snapshot collector.
- [  ] Safe start and stop operations.
- [  ] Persistent data storage.
- [  ] Basic PySide6 interface.
- [  ] Controlled errors and central logging.
- [  ] Basic automated tests.
- [  ] Updated English and Spanish documentation.

`v0.1.0` will represent the first usable Alpha version of MDI.

---

## Versioning rule

MDI uses development versions below `1.0.0`.

- `0.0.x`: individual modules and internal development milestones.
- `0.1.0`: first usable Alpha.
- `0.x.0`: relevant development-stage feature releases.
- `1.0.0`: future stable release.

A version number is increased when a functional milestone is completed,
tested, documented, and committed.

Not every internal commit requires a new version number.
