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

## Projects

| Ticket | Project     | Description                 | Status        |
| ------ | ----------- | --------------------------- | ------------- |
| #001   | **PEXA**    | Password Expiration Auditor | [x] Completed |
| #002   | **STAyzer** | SSH Trust Analyzer          | [] Planned    |

---

## Ticket #001 — PEXA

PEXA (Password Expiration Auditor) automates password expiration audits across multiple Linux servers.

## Ticket #002 – STAyzer

STAyzer (SSH Trust Analyzer) audits SSH trust relationships across Linux servers by analyzing users' `authorized_keys` files. It identifies which public keys are authorized on each server, detects duplicate keys shared between users or hosts, and builds a trust map showing where SSH access has been granted.

### Planned Features

- Audit multiple Linux servers over SSH
- Discover all `authorized_keys` files
- Parse and fingerprint authorized public keys
- Detect duplicate public keys across users and servers
- Build a server-to-key trust map
- Export reports in JSON, CSV, and HTML
- Generate summary statistics and security findings

---

## Why OOPS?

System administrators spend a significant amount of time performing repetitive operational tasks.

Instead of executing the same commands every day, OOPS focuses on building reusable automation tools that:

- save time
- reduce human error
- improve operational visibility
- generate professional reports
- simplify infrastructure management

Every project in this repository is inspired by a realistic administration scenario.

---

**Full Documentation**

See:

**[Documentation](https://hosnizaaraoui.github.io/OOPS/)**

---

## Contributing

Ideas, improvements, bug reports, and new automation scripts are always welcome.

Feel free to open an Issue or submit a Pull Request.

---

## License

This project is licensed under the MIT License.
