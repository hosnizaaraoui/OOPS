# OOPS - Operations Optimization & Python Scripts

> A curated collection of Python tools designed to automate Linux system administration tasks, eliminate repetitive work, and help system administrators manage infrastructure more efficiently.

<p align="center">
<img src="./assets/oops_banner.png" alt="Console Report">
</p>

## About

OOPS is a collection of production-inspired Python projects built around real-world system administration scenarios.

Each project starts from a practical operational problem ("ticket") and evolves into a reusable command-line tool with clean architecture, documentation, and reporting capabilities.

The goal of this repository is to:

- Learn Python through practical automation
- Solve common Linux administration tasks
- Build reusable command-line utilities
- Share production-inspired solutions with the community

---

# Repository Structure

```
OOPS/
│
├── assets/
│   ├── banner.png
│   └── screenshots/
│
├── docs/
│
├── pexa/
│   ├── README.md
│   ├── collectors/
│   ├── filters/
│   ├── hosts/
│   ├── models/
│   ├── reports/
│   ├── utils/
│   └── main.py
│
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

---

# Projects

| Ticket | Project                    | Description                 | Status        |
| ------ | -------------------------- | --------------------------- | ------------- |
| #001   | **[PEXA](PEXA/README.md)** | Password Expiration Auditor | [x] Completed |

---

# Ticket #001 — PEXA

PEXA (Password Expiration Auditor) automates password expiration audits across multiple Linux servers.

### Features

- Audit local and remote Linux hosts
- SSH-based execution using AsyncSSH
- Inventory file support
- Ignore system accounts automatically
- Password expiration analysis
- Powerful filtering
- Colored console reports
- JSON export
- CSV export
- HTML export
- Verbose execution mode

**Documentation**

See:

**[Ticket #001 - PEXA](PEXA/README.md)**

---

# Roadmap

## Completed

- [x] Ticket #001 - Password Expiration Auditor (PEXA)

## Planned

- [ ] Ticket #002
- [ ] Ticket #003
- [ ] Ticket #004
- [ ] Ticket #005

---

# Why OOPS?

System administrators spend a significant amount of time performing repetitive operational tasks.

Instead of executing the same commands every day, OOPS focuses on building reusable automation tools that:

- save time
- reduce human error
- improve operational visibility
- generate professional reports
- simplify infrastructure management

Every project in this repository is inspired by a realistic administration scenario.

---

# Contributing

Ideas, improvements, bug reports, and new automation scripts are always welcome.

Feel free to open an Issue or submit a Pull Request.

---

# License

This project is licensed under the MIT License.
