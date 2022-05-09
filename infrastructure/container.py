from dependency_injector import containers, providers

from infrastructure.data_source_service.chirps_service import ChirpsService
from infrastructure.model_config.model_config_service import ModelConfigService
from infrastructure.model_config.path_constants import ProjectPathConstants


class Container(containers.DeclarativeContainer):
    project_path_constants = providers.Singleton(ProjectPathConstants)

    model_config = providers.Singleton(
        ModelConfigService,
        project_path_constants
    )
    chirps_service = providers.Singleton(
        ChirpsService,
        model_config
    )

