# YAML-Doctor 🩺📄  
[![PyPI version](https://badge.fury.io/py/yaml-doctor.svg)](https://pypi.org/project/yaml-doctor/)
[![CI](https://github.com/thisguy022/yaml-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/thisguy022/yaml-doctor/actions/workflows/ci.yml)

Validate – and automatically **fix duplicate keys** – in Home-Assistant-style YAML files.  
No more mysterious “duplicated mapping key” errors breaking your automations!

---

## ✨ Features
- **Fast validation** of any YAML file (Home Assistant, ESPHome, CI pipelines, etc.)
- **Smart auto-fix** `--fix` flag renames duplicate keys in-place (optionally backs up originals)
- **Colorful Rich output** for quick at-a-glance feedback
- **Zero-config CLI** – just run `yaml-doctor your_file.yaml`
- Works on **Windows, macOS, and Linux** (Python ≥ 3.9)

---

## 📦 Installation

### User install (from PyPI – easiest)

```bash
pip install yaml-doctor
