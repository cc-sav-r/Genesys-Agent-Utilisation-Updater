## Prerequisites

- Python (version 3.13 or higher)
- pip (Python package manager)
- PureCloudPlatformClientV2

Install dependency:

```
pip install PureCloudPlatformClientV2
```

---

## Configuration

Add required environment variables:

### macOS & Linux - Add the below to .zshrc/.bashrc

```
export GENESYSCLOUD_OATUCLIENT_ID=ID_HERE
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

```
python3 app.py
```

Ensure the agents.csv file is complete before running.
