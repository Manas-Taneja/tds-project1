# Task Agent API

## Overview

The Task Agent API is designed to automate routine tasks based on plain-English input, leveraging a Large Language Model (LLM) where required. This agent can process log files, reports, and code artifacts to perform a series of steps as part of an operational pipeline. The goal is to improve operational efficiency and consistency in various tasks.

## Features
- Accepts plain-English tasks as input.
- Uses LLM for intermediate task processing.
- Automation agent that performs multi-step tasks.
- The finished processing artifacts are verifiable against pre-computed expected results.

## Setup Instructions

### 1. **Set Up Environment Variables**

Before starting the application, you need to set up your environment variables. The `AIPROXY_TOKEN` is required for authentication.

You can set the `AIPROXY_TOKEN` from your `.env` file using the following PowerShell command:

```powershell
$env:AIPROXY_TOKEN = (Get-Content .env | Where-Object { $_ -match "^AIPROXY_TOKEN=" }) -replace "AIPROXY_TOKEN=", ""
```

### 2. **Run the Application Locally**
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. **Docker Setup**
- If you want to containerize the application using Docker, follow these steps:
  - Build the Docker Image:
     ```powershell
     docker build -t your-dockerhub-username/task-agent-api .
     ```
  - Log in to DockerHub:
     ```powershell
     docker login
     ```
  - Push your Docker image to DockerHub:
     ```powershell
     docker push your-dockerhub-username/task-agent-api
     ```

### 4. **Podman Setup**
- If you prefer using Podman over Docker, follow these steps:
  ```powershell
  podman machine init
  podman machine start
  ```
- Run the Podman Container:
  - Run the application in Podman with the environment variable AIPROXY_TOKEN:
    ```powershell
    podman run -e AIPROXY_TOKEN=$env:AIPROXY_TOKEN -p 8000:8000 -v ${PWD}/data:/data your-podmanhub-username/task-agent-api
    ```
- Stop Podman Container:
  - To stop the container:
    ```powershell
    podman stop $(podman ps -q)
    ```

## Sample File
```
2024-01-01
2024-02-14
2024-03-17
2024-04-10
2024-05-05
2024-06-20
2024-07-30
2024-08-15
2024-09-25
2024-10-31
2024-11-22
2024-12-25
```

## Dockerfile
Below is the Dockerfile used to build the container image for this application:
```dockerfile
# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /task-agent-api

# Copy and install dependencies separately for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the FastAPI server port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## OpenAI API Key
Ensure that you have an OpenAI API key. You can use the following Python snippet to connect to the OpenAI API:
```python
import openai

# Set your OpenAI API key
api_key = "your-key"

# Initialize OpenAI API client
client = OpenAI(api_key=api_key)

# Request completion
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "write a haiku about AI"}
    ]
)

# Print the completion result
print(completion.choices[0].message.content.strip())
```

### Installing the OpenAI Python Library
Install the OpenAI Python library by running:
```powershell
pip install openai
```

## Contribution
Feel free to fork the repository, open issues, and contribute to the codebase. For contributions, please follow the steps below:
1. Fork the repository
2. Create a new branch (`git checkout -b my-feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin my-feature-branch`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Sanjoli04/task-agent-api/blob/main/LICENSE) file for details.
```
