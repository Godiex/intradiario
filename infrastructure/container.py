from dependency_injector import containers, providers

from infrastructure.chirps_service import ChirpsService
from infrastructure.model_config import ModelConfig
from infrastructure.project_path_constants import ProjectPathConstants


class Container(containers.DeclarativeContainer):
    project_path_constants = providers.Singleton(ProjectPathConstants)
    model_config = providers.Singleton(
        ModelConfig,
        project_path_constants
    )
    chirps_service = providers.Singleton(
        ChirpsService,
        model_config
    )

