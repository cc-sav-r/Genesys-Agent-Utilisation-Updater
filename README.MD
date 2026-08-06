## Prerequisites

- Python (version 3.13 or higher)
- pip (Python package manager)

Install dependencies:

```
pip install -r requirements.txt
```

---

## Configuration

Add required environment variables:

### macOS & Linux - Add the below to .zshrc/.bashrc

```
export GENESYSCLOUD_OAUTHCLIENT_ID=ID_HERE
export GENESYSCLOUD_OAUTHCLIENT_SECRET=SECRET_HERE
```

### Windows

Refer to https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set_1

---

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/cc-sav-r/Genesys-Agent-Utilisation-Updater.git
   ```

2. Change directory into project folder

3. (Optional: create a virtual environment)

   ```
   python3 -m venv .venv
   ```

   3a. Activate the virtual environment:

   ```
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

---

## Run the tool

Ensure the agents.csv file is complete before running, then run:

```
python3 app.py
```
