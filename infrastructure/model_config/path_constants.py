from infrastructure.model_config.project_path import ProjectPath


class ProjectPathConstants:
    def __init__(self):
        self.base_path = ProjectPath().get_path_of_system()
        self.path_hydstra_config = f'{self.base_path}\\00_Metadata\\_config\\Hydstra-config.json'
        self.path_ideam_config = f'{self.base_path}\\00_Metadata\\_config\\Ideam-config.json'
        self.path_siata_config = f'{self.base_path}\\00_Metadata\\_config\\Siata-config.json'
        self.path_chirps_config = f'{self.base_path}\\00_Metadata\\_config\\Chirps-config.json'
        self.path_project_config = f'{self.base_path}\\00_Metadata\\_config\\Projects-config.json'
        self.path_project_params_config = f'{self.base_path}\\00_Metadata\\_config\\ProjectsParams.json'
