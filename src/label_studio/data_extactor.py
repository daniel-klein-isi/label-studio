import os
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

import pandas as pd
from dotenv import load_dotenv
from label_studio_sdk.client import LabelStudio
from label_studio_sdk.types import Project, Task


@dataclass
class AnnotationData:
    """Data class for storing annotation information."""

    project_id: int
    task_id: int
    data_source: str
    annotation_id: Optional[int] = None
    img_width: Optional[int] = None
    img_height: Optional[int] = None
    area_id: Optional[str] = None
    ann_type: Optional[str] = None
    label: Optional[str] = None
    meta: Optional[str] = None
    bbox_x: Optional[float] = None
    bbox_y: Optional[float] = None
    bbox_width: Optional[float] = None
    bbox_height: Optional[float] = None
    rotation: Optional[float] = None
    relation_from: Optional[str] = None
    relation_to: Optional[str] = None
    relation_type: Optional[str] = None
    segmentation_points: Optional[List[List[float]]] = None


class LabelStudioExtractor:
    """Main class for extracting data from Label Studio projects.

    This class provides a unified interface for connecting to Label Studio.
    and extracting different types of annotations as DataFrames.
    """

    def __init__(self, api_key: Optional[str] = None, url: Optional[str] = None):
        """Initialize the Label Studio extractor.

        Parameters
        ----------
        Args:
            api_key: Label Studio API key (if not provided, will load from .env)
            url: Label Studio URL (if not provided, will load from .env)
        """
        load_dotenv()

        self.api_key = api_key or os.getenv("LABEL_STUDIO_API_KEY")
        self.url = url or os.getenv("LABEL_STUDIO_URL", "http://localhost:8080")

        if not self.api_key:
            raise ValueError(
                "API key is required. "
                "Set LABEL_STUDIO_API_KEY in .env file or pass as parameter."
            )

        self.client = LabelStudio(base_url=self.url, api_key=self.api_key)

    def get_projects(
        self, as_dataframe: bool = True
    ) -> Union[pd.DataFrame, List[Dict]]:
        """Get all projects from Label Studio.

        Parameters
        ----------
        Args:
            as_dataframe: If True, returns DataFrame, otherwise returns list of dicts.

        Returns
        -------
            DataFrame or list with project information.
        """
        try:
            projects: List[Project] = self.client.projects.list().items
            projects

            if as_dataframe:
                return pd.DataFrame(
                    [
                        {
                            "id": p.id,
                            "title": p.title,
                            "description": p.description,
                            "created_by": p.created_by.email,
                            "created_at": p.created_at,
                            "tasks": p.task_number,
                            "tasks_finished": p.finished_task_number,
                        }
                        for p in projects
                    ]
                )

            return [dict(p) for p in projects]

        except Exception as e:
            print(f"Error fetching projects: {e}")

    def get_tasks(
        self, project_id: int, iterator: bool = False
    ) -> Union[List[Dict], Iterator]:
        """
        Get all tasks from a specific project.

        Parameters
        ----------
        Args:
            project_id: ID of the project.

        Returns
        -------
            List of task dictionaries.
        """
        try:
            tasks = self.client.tasks.list(project=project_id)
            if iterator:
                yield tasks
            else:
                return [dict(task) for task in tasks]

        except Exception as e:
            print(f"Error fetching tasks for project {project_id}: {e}")

    def get_annotations(
        self, project_id: int, as_dataframe: bool = True
    ) -> Union[pd.DataFrame, List[Dict]]:

        annotations = self._extract_annotations(project_id)

        if as_dataframe:
            return self._annotations_to_dataframe(annotations)
        else:
            return [self._annotation_to_dict(ann) for ann in annotations]

    def _extract_annotations(self, project_id) -> List[AnnotationData]:

        rectangle_result_type_parser = {
            "rectanglelabels": "rectanglelabels",
            "choices": "choices",
            "textarea": "text",
        }

        annotations = []
        tasks: Iterator[Task] = self.client.tasks.list(project=project_id)
        for task in tasks:

            for ann in task.annotations:

                for result in ann.get("result", {}):

                    img_width, img_height = self._get_img_dimensions(result)
                    value = result.get("value", {})
                    result_type = result.get("type")
                    meta_txt = result.get("meta", {}).get("text", [None])[0]

                    if result_type in rectangle_result_type_parser.keys():

                        for label in value.get(
                            rectangle_result_type_parser[result_type], []
                        ):
                            annotations.append(
                                AnnotationData(
                                    project_id=project_id,
                                    task_id=task.id,
                                    data_source=self._get_data_source(task.data),
                                    annotation_id=ann.get("id"),
                                    img_width=img_width,
                                    img_height=img_height,
                                    area_id=result.get("id"),
                                    ann_type=result_type,
                                    label=label,
                                    meta=meta_txt,
                                    bbox_x=value.get("x"),
                                    bbox_y=value.get("y"),
                                    bbox_width=value.get("width"),
                                    bbox_height=value.get("height"),
                                    rotation=value.get("rotation"),
                                )
                            )
                    elif result_type in ["relation"]:
                        annotations.append(
                            AnnotationData(
                                project_id=project_id,
                                task_id=task.id,
                                data_source=self._get_data_source(task.data),
                                annotation_id=ann.get("id"),
                                ann_type=result_type,
                                relation_from=result.get("from_id"),
                                relation_to=result.get("to_id"),
                            )
                        )
        return annotations

    def _get_img_dimensions(self, result: Dict) -> tuple:
        """Extract image dimensions from task."""
        width = result.get("original_width", None)
        height = result.get("original_height", None)
        return width, height

    def _get_data_source(self, data: Dict) -> str:
        """Extract data source from task."""
        # Common keys for image sources
        for key in ["image", "url", "path", "file"]:
            if key in data:
                if key == "image":
                    return Path(data[key]).name
                else:
                    return data[key]

    def _annotations_to_dataframe(
        self, annotations: List[AnnotationData]
    ) -> pd.DataFrame:
        """Convert annotations to DataFrame."""
        if not annotations:
            return pd.DataFrame()

        data = [
            {field.name: getattr(ann, field.name) for field in fields(ann)}
            for ann in annotations
        ]
        return pd.DataFrame(data)

    def _annotation_to_dict(self, annotations: List[AnnotationData]) -> Dict[str, Any]:
        """Convert AnnotationData to dictionary."""
        return [
            {field.name: getattr(ann, field.name) for field in fields(ann)}
            for ann in annotations
        ]
