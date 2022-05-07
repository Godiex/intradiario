

class DataSourceConfig(object):
    def __init__(self, files_name):
        super().__init__()
        self.files_name = files_name


class HydstraConfig(DataSourceConfig):

    def __init__(self, files_name, hydron_path):
        DataSourceConfig.__init__(self, files_name)
        self.hydron_path = hydron_path


class ExternalDataSourceConfig(DataSourceConfig):
    def __init__(self, files_name, server_url, output_path):
        DataSourceConfig.__init__(self, files_name)
        self.server_url = server_url
        self.output_path = output_path


class ChirpsConfig(ExternalDataSourceConfig):

    def __init__(self, files_name, server_url, output_path):
        ExternalDataSourceConfig.__init__(self, files_name, server_url, output_path)


class IdeamConfig(ExternalDataSourceConfig):

    def __init__(self, files_name, server_url, output_path):
        ExternalDataSourceConfig.__init__(self, files_name, server_url, output_path)


class SiataConfig(ExternalDataSourceConfig):

    def __init__(self, files_name, server_url, output_path):
        ExternalDataSourceConfig.__init__(self, files_name, server_url, output_path)
