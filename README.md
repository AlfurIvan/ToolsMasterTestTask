# Time Tracking System in Coda.io

This project is designed to track time spent on tasks using Coda.io and Python integration for interaction and analysis.

## Features

* **Automatic Calculations:**
    * Daily productivity
    * Time distribution by category
    * Deadline calculations: to display somewhere or make Slack notifications f.e.
* **Live interface:** Simple data visualization using Coda.io.
    ```https://coda.io/@ivan-zharyi/tools-master-test-task```


## Getting Started

1. Create a `.env` file and copy all values from `.env.example`.
2. Run:
   ```bash
   poetry install
   ```

## Running the Application

1. Run:
   ```bash
   poetry run uvicorn app:app --reload --port 8000
   ```

## Documentation

Navigate to `http://127.0.0.1:8000/docs` to use the API.


I hope you'll enjoy your journey!
