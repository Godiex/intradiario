class ProjectConfig:
    def __init__(
        self,
        projects,
        parameterization,
        summary_info,
        time_series_info,
        logPath,
        delta_time=88000
    ):
        self.projects = projects
        self.parameterization = parameterization
        self.summary_info = summary_info
        self.time_series_info = time_series_info
        self.logPath = logPath
        self.delta_time = delta_time


class ProjectParameters:
    stations = []


class ProjectParams:
    basin_name = ""
    central = ""
    project_parameters = ProjectParameters()
