# YAML-Doctor

![CI](https://github.com/thisguy022/yaml-doctor/actions/workflows/ci.yml/badge.svg)

Validate — and automatically **fix duplicate keys** — in Home-Assistant-style YAML files.

## Installation

```bash
git clone https://github.com/thisguy022/yaml-doctor.git
cd yaml-doctor
pip install -r requirements.txt

## Usage

| Action | Command |
|--------|---------|
| **Validate only** | `python yaml_doctor.py your_file.yaml` |
| **Validate and auto-fix duplicates** | `python yaml_doctor.py your_file.yaml --fix` |

## Contributing

Pull requests are welcome!  
Make sure `python -m unittest` passes and CI is green.
