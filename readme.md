# NetPulse 0.1

## Description

**This project enables multiple agents to send data to multiple monitors simultaneously.**

### Monitored Data

1. CPU Temperature
2. GPU Temperature
3. RAM Usage
4. Swap Usage
5. Download Speed
6. Upload Speed
7. CPU Core Temperature

## Screenshots


| Screenshot 1 | Screenshot 2 | Screenshot 3 |
| ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| ![1791126892810](images/readme/1791126892810.png) | ![1791126906180](images/readme/1791126906180.png) | ![1791126933027](images/readme/1791126933027.png) |
|                                                   |                                                   |                                                   |

## Features

* Multiple agents can transmit data to multiple monitors at the same time.
* Fast, modern, and sleek user interface (GUI).
* Agent data collection backed by SQL storage.

## Tech Stack & Prerequisites

### Server

* Built asynchronously with FastAPI, allowing concurrent listening and data transmission.
* Uses MySQL 8.0 as the database with asynchronous operations via SQLModel.

### Agent

* Retrieves system hostname using `platform`.
* Collects system telemetry using `psutil`.
* Transmits data asynchronously to the server via `aiohttp`.

### Client

* Built using `Flet` for the UI and `flet-charts` for real-time visualization.
* Continuously polls the server asynchronously via `aiohttp`.

## Installation & Usage

Download Python 3.12.3.

### Windows

[Download Python for Windows](https://www.python.org/downloads/release/python-3123/)

### macOS

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew install python
```

Verify installation:
```bash
python3 --version
```

### Linux

#### Debian, Ubuntu, and derivatives (e.g., Linux Mint)

```bash
sudo apt install python3
```

#### Fedora and derivatives

```bash
sudo dnf install python3
```

#### Arch Linux and derivatives

```bash
sudo pacman -S python
```

#### Pisi Linux and derivatives

```bash
sudo pisi it python3
```

### Installing Required Dependencies

```bash
pip install -r requirements.txt
```

### Running the Application

Activate the virtual environment:
```bash
source venv/bin/activate
```

#### Run Server

```bash
python3 main.py
```

#### Run Agent

```bash
python3 agent.py
```

#### Run Client

```bash
python3 client.py
```