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

**Option 1: Command Prompt (temporary, current session only)**

```
set GENESYSCLOUD_OAUTHCLIENT_ID=ID_HERE
set GENESYSCLOUD_OAUTHCLIENT_SECRET=SECRET_HERE
```

**Option 2: PowerShell (temporary, current session only)**

```
$env:GENESYSCLOUD_OAUTHCLIENT_ID = "ID_HERE"
$env:GENESYSCLOUD_OAUTHCLIENT_SECRET = "SECRET_HERE"
```

**Option 3: Permanent (persists across sessions/reboots)**

Using PowerShell:

```
[System.Environment]::SetEnvironmentVariable("GENESYSCLOUD_OAUTHCLIENT_ID", "ID_HERE", "User")
[System.Environment]::SetEnvironmentVariable("GENESYSCLOUD_OAUTHCLIENT_SECRET", "SECRET_HERE", "User")
```

Or via the GUI:

1. Open **Start** and search for "Environment Variables"
2. Select **Edit the system environment variables**
3. Click **Environment Variables...**
4. Under **User variables**, click **New...** and add each variable name/value pair
5. Click **OK** to save, then restart any open Command Prompt/PowerShell/terminal windows for the changes to take effect

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
