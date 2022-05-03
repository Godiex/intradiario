from pathlib import Path


class ProjectPath:
    __develop_path = "\\\\epm-file02\\DATALAKE\\Hydrosed_intradiario\\03_Desarrollo"
    __test_path = "\\\\epm-file02\\DATALAKE\\Hydrosed_intradiario\\04_Pruebas"
    __production_path = "\\\\epm-file02\\DATALAKE\\Hydrosed_intradiario"
    __local_path = "D:\Documentos\Trabajo\Ceiba\EPM"

    __environments = {
        "develop": "DESARROLLO",
        "test": "PRUEBAS",
        "production": "PRODUCCION"
    }

    def get_path_of_system(self):
        for value in self.__environments.values():
            if Path(f"C:/{value}").exists():
                return self.get_path_for_env(value)
        return self.__local_path

    def get_path_for_env(self, env: str) -> str:
        if env == self.__environments['develop']:
            return self.__develop_path
        elif env == self.__environments['test']:
            return self.__test_path
        elif env == self.__environments['production']:
            return self.__production_path
