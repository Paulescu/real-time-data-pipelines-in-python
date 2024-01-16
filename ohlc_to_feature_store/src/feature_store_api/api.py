import os
from typing import Optional, Dict, Any
import logging

import hopsworks
import hsfs
import pandas as pd

from .types import FeatureGroupConfig

logger = logging.getLogger()

class FeatureGroup:

    def __init__(
        self,
        feature_group: hsfs.feature_group.FeatureGroup,
    ):  
        self._fg = feature_group
        
    def write(
        self,
        value: Dict[str, Any],
        keys: Optional[list] = None,
        online_only: Optional[bool] = True,
    ):
        # If `keys` is prvovided, only keep these in the value
        _value = {k: value[k] for k in keys} if keys else value
        
        # Convert the value to a Pandas DataFrame
        df = pd.DataFrame.from_records([_value])

        # Write the DataFrame to the feature group
        logger.info(f'Writing {df} to feature group {self._fg}')
        if online_only:
            self._fg.insert(df, write_options={"start_offline_backfill": False})
        else:
            raise NotImplementedError("Offline writing not implemented yet")

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

    def get_or_create_feature_group(self, feature_group_config: FeatureGroupConfig) -> FeatureGroup:
        """
        Creates a feature group in the feature store if it does not exist, otherwise returns the existing feature group.
        """
        logger.info(f"Creating feature group {feature_group_config}")
        
        fg = self._fs.get_or_create_feature_group(
            name=feature_group_config.name,
            version=feature_group_config.version,
            description=feature_group_config.description,
            primary_key=feature_group_config.primary_key,
            event_time=feature_group_config.event_time,
            online_enabled=feature_group_config.online_enabled
        )

        logger.info(f"Created feature group {fg}")

        return FeatureGroup(fg)
    
    def _get_feature_store(self) -> hsfs.feature_store.FeatureStore:
        project = hopsworks.login(
            project=self._project_name,
            api_key_value=self._api_key,
        )
        return project.get_feature_store()
