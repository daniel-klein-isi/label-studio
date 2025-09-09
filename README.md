# projectname-label-studio
This repository provides a Dockerized deployment of Label Studio, a powerful open-source tool for data annotation, specifically packaged for data extraction with an API.

## Overview
This project simplifies the deployment and management of Label Studio using Docker and Docker Compose. It includes pre-configured settings and a mechanism to initialize configuration files, making it easy to get started with data annotation tasks.

## Getting Started

### Prerequisites
*   Docker
*   Docker Compose

### Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/projectname-label-studio.git
    cd projectname-label-studio
    ```
    (Note: Replace `https://github.com/your-repo/projectname-label-studio.git` with the actual repository URL.)

2.  **Build the Docker image:**
    ```bash
    docker-compose build
    ```

3.  **Start Label Studio:**
    ```bash
    docker-compose up -d
    ```
    This will start the Label Studio container in detached mode.

### Accessing Label Studio

Once the container is running, you can access Label Studio in your web browser:

*   **URL:** `http://localhost:8000`

### Default Credentials

The default authentication credentials are set in `config/env.sh`. For initial access:

*   **Username:** `user@email.com`
*   **Password:** `mypassword123456`

**Important:** For production deployments, it is highly recommended to change these default credentials and manage them securely using Docker secrets or environment variables passed at runtime.

## Project Structure

*   `docker-compose.yaml`: Defines the Docker service for Label Studio, including image build instructions, port mapping, restart policy, and volume mounts.
*   `Dockerfile`: Specifies the steps to build the `projectname-label-studio` Docker image, including Python environment setup, dependency installation, and application configuration.
*   `entrypoint.sh`: The entry point script for the Docker container. It initializes configuration files from a template if the `/workspace/config` directory is empty.
*   `run.sh`: Executes the Label Studio application, loading environment variables from `config/env.sh`.
*   `config/`: Contains configuration files for Label Studio.
    *   `config/env.sh`: Sets various environment variables for Label Studio, including paths, feature flags, data upload limits, and authentication details.
*   `requirements.txt`: Lists the Python dependencies required by Label Studio.
*   `data/`: A directory mounted into the container for storing project-specific data (e.g., uploaded files, annotations).
*   `LICENSE`: Contains the licensing information for the project.

## Customization

### Configuration
You can customize Label Studio's behavior by modifying the `config/env.sh` file. This file sets crucial environment variables.

### Data Storage
The `./data` directory on your host machine is mounted to `/workspace/data` inside the container. This is where Label Studio stores project data.

### API for Data Extraction
Label Studio provides a comprehensive API that can be used for programmatic data extraction, project management, and automation. Refer to the official Label Studio documentation for detailed API usage: [https://labelstud.io/api/](https://labelstud.io/api/)
