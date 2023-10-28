# Activision Ban Checker

Script for automatic check of bans on Activision accounts

## Getting Started

#### Prerequisites:

1. [Download and install Python](https://www.python.org/downloads/) (Version 3.10+ is recommended).

#### Setting up the project:

##### Install

```
git clone https://github.com/TemaDrakoshef/acrivision-ban-checker.git
```

2. Navigate to the project directory:

```
cd acrivision-ban-checker
```

3. (Recommended) Create a virtual environment to manage Python packages for your project:

```
python3 -m venv venv
```

4. Activate the virtual environment:
   - On Windows:
   ```
   .\venv\Scripts\activate
   ```
   - On macOS and Linux:
   ```
   source venv/bin/activate
   ```
5. Install the required Python packages from `requirements.txt`:

```
pip install -r requirements.txt
```

##### Config params

6. Rename the `.env.dist` file to `.env`.

|        Name         | Type  | Description                                                            |
|:-------------------:|:-----:|:-----------------------------------------------------------------------|
|     SLEEP_TIME      | float | The amount of time you need to sleep before the next ban check         |
| CONCURRENT_REQUESTS |  int  | Number of accounts that need to be checked at the same time            |
|      BOT_TOKEN      |  str  | Your API token ([botfather](https://t.me/botfather))                   |
|       ADMINS        | list  | Identifiers of users to whom account status information should be sent |
