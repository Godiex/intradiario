from infrastructure.model_config.data_source_config_model import ChirpsConfig
from infrastructure.model_config.path_constants import ProjectPathConstants
from shared.json_utils import parse_to_dictionary


class ModelConfigService:
    def __init__(self, project_path_constants: ProjectPathConstants):
        self.project_path_constants = project_path_constants

    def get_config_chirps(self) -> ChirpsConfig:
        chirps_path = self.project_path_constants.path_chirps_config
        chirps_config = parse_to_dictionary(chirps_path)
        return ChirpsConfig(
            chirps_config["files_name"],
            chirps_config["server_url"],
            chirps_config["output_path"]
        )
