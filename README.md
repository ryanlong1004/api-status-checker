# Install
- Clone the repository
- In the root of the local cloned repo enter the following to install depenedencies
`pip install -r requirements.txt`

# Configuration
```bash
STATUS_CHECKER_EMAIL=<john.smith@noaa.gov>
STATUS_CHECKER_KEY=<API_KEY>
LOG_LOCATION=<DIRECTORY TO SAVE LOGS>
QUEUE_LOCATION=<DIRECTORY CONTAINING queue.json>
QUEUE_URL_ROOT=<ROOT URL OF APP example: https://spot-dev.ncep.noaa.gov">
```

# To Run
- In the root of the directory, run:
`python[3] src/main.py`