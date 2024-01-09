import os
from typing import Optional

import hopsworks
import hsfs
import pandas as pd

from .types import FeatureGroupConfig


class FeatureStore:
    def __init__(
        self,
        api_key: Optional[str] = None,
        project_name: Optional[str] = os.environ["HOPSWORKS_PROJECT_NAME"],
    ):
        self._api_key = api_key
        if self._api_key is None:
            try:
                self._api_key = os.environ["HOPSWORKS_API_KEY"]
            except KeyError:
                raise KeyError(
                    "No HOPSWORKS_API_KEY provided. Please provide an API key or set the HOPSWORKS_API_KEY environment variable."
                )

        self._project_name = project_name
        if self._project_name is None:
            try:
                self._project_name = os.environ["HOPSWORKS_PROJECT_NAME"]
            except KeyError:
                raise KeyError(
                    "No HOPSWORKS_PROJECT_NAME provided. Please provide a project name or set the HOPSWORKS_PROJECT_NAME environment variable."
                )

        self._fs = self._get_feature_store()

    def write(
        self,
        features: pd.DataFrame,
        feature_group: FeatureGroupConfig,
        online_only: Optional[bool] = True,
    ):
        print(f"Pushing {features} to feature group {feature_group}")

    def _get_feature_store(self) -> hsfs.feature_store.FeatureStore:
        project = hopsworks.login(
            project=self._project_name,
            api_key_value=self._api_key,
        )
        return project.get_feature_store()
