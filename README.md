# Label Studio Deployment & Data Extraction

## Introduction
This repository provides a standardized method for deploying Label Studio using Docker and offers a Python package for programmatic data extraction from Label Studio projects.

## Objective 1: Deploy Label Studio with Docker

### Prerequisites
*   Docker
*   Docker Compose

### Quick Start
Follow these steps to get Label Studio running quickly on your local machine or a virtual machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/daniel-klein-isi/label-studio.git
    cd label-studio
    ```

2.  **Build and start Label Studio container:**
    ```bash
    docker compose -f ./docker/docker-compose.yaml up -d --build
    ```
    This command builds the Docker image (if not already built) and starts the Label Studio container in detached mode.

3.  **Access Label Studio:**
    Once the container is running, open your web browser and navigate to:
    `http://localhost:8000`

### Configuration
Label Studio's behavior can be customized by modifying the `docker/config/env.sh` file. This file sets crucial environment variables, including:

*   `LABEL_STUDIO_USERNAME`: Default username for initial access.
*   `LABEL_STUDIO_PASSWORD`: Default password for initial access.
*   `LABEL_STUDIO_USER_TOKEN`: API token for programmatic access.
*   `LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED`: Enables serving local files.
*   `LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT`: Specifies the directory for local files (mapped to `./docker/data` on the host).

**Important:** For production deployments, it is highly recommended to change these default credentials and manage them securely using Docker secrets or environment variables passed at runtime.

### Data Storage
The `./docker/data` directory on your host machine is mounted to `/workspace/data` inside the container. This is where Label Studio stores project-specific data (e.g., uploaded files, annotations).

### Advanced Usage

#### Uploading Data without GUI
To upload data (e.g., images) without using the graphical interface:

1.  Place your files into the `./docker/data` directory on your host machine.
2.  Ensure `LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED` is set to `true` in `docker/config/env.sh`.
3.  In Label Studio, configure a new project to use "Local files" as a data source, pointing to `/workspace/data` within the container.
4.  Synchronize the storage in Label Studio to create tasks from your uploaded files.

#### Importing Annotations JSON
You can import existing annotations in JSON format. Refer to the official Label Studio documentation for the required JSON structure and import methods.

#### API for Data Extraction
Label Studio provides a comprehensive API for programmatic data extraction, project management, and automation. The `LABEL_STUDIO_USER_TOKEN` in `docker/config/env.sh` can be used for authentication. Refer to the official Label Studio documentation for detailed API usage: [https://labelstud.io/api/](https://labelstud.io/api/)

## Objective 2: Install Package and Extract Data

### Installation
This repository also provides a Python package to facilitate data extraction from Label Studio projects.

1.  **Install the package:**
    ```bash
    pip install .
    ```
    This command installs the `label_studio` package from the current directory.

### Usage
The `LabelStudioExtractor` class in `src/label_studio/data_extactor.py` allows you to connect to your Label Studio instance and extract project, task, and annotation data.

#### Example: Extracting Annotations
```python
import os
from label_studio.data_extactor import LabelStudioExtractor
from dotenv import load_dotenv

# Load environment variables from .env file (if not already loaded)
load_dotenv()

# Initialize the extractor with your Label Studio API key and URL
# You can set LABEL_STUDIO_API_KEY and LABEL_STUDIO_URL in a .env file
# or pass them directly to the constructor.
extractor = LabelStudioExtractor(
    api_key=os.getenv("LABEL_STUDIO_API_KEY"),
    url=os.getenv("LABEL_STUDIO_URL", "http://localhost:8000")
)

# Get all projects
projects_df = extractor.get_projects(as_dataframe=True)
print("Projects:")
print(projects_df)

# Replace with your project ID
project_id = 1 

# Get all tasks for a specific project
tasks_list = extractor.get_tasks(project_id=project_id, iterator=False)
print(f"\nTasks for Project {project_id}:")
for task in tasks_list:
    print(task)

# Get all annotations for a specific project as a DataFrame
annotations_df = extractor.get_annotations(project_id=project_id, as_dataframe=True)
print(f"\nAnnotations for Project {project_id}:")
print(annotations_df)
```

### Environment Variables for Package
The Python package uses environment variables for configuration. Create a `.env` file in your project root with the following:

```
LABEL_STUDIO_API_KEY="your_label_studio_api_key"
LABEL_STUDIO_URL="http://localhost:8000" # Or your Label Studio instance URL
```

## Project Structure
*   `docker/`: Contains Docker-related files for deploying Label Studio.
    *   `docker-compose.yaml`: Defines the Docker service for Label Studio.
    *   `Dockerfile`: Specifies how to build the Label Studio Docker image.
    *   `entrypoint.sh`: Script to initialize configuration and start Label Studio.
    *   `run.sh`: Executes the Label Studio application.
    *   `config/`: Default configuration files for Label Studio, including `env.sh`.
    *   `data/`: Mounted directory for Label Studio project data.
*   `src/`: Contains the Python package for data extraction.
    *   `label_studio/data_extactor.py`: The core data extraction logic.
*   `pyproject.toml`: Project metadata and dependencies for the Python package.
*   `requirements.txt`: Python dependencies for the Docker image.
*   `README.md`: This file.
*   `LICENSE`: Licensing information for the project.

## License
This project is licensed under the [LICENSE](LICENSE) file.
