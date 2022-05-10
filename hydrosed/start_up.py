import sys

from dependency_injector.wiring import Provide, inject

from infrastructure.container import Container
from infrastructure.data_source_service.data_source_service import ExternalDataSourceService
from shared import menssage


def wire_modules():
    container = Container()
    container.wire(modules=[sys.modules[__name__]])


@inject
def run_app(chirps_service: ExternalDataSourceService = Provide[Container.chirps_service]):
    try:
        menssage.info("Inicio descarga datos")
        chirps_service.get_data()
        menssage.success("Finalizacion descarga datos")

        menssage.info("Inicio procesamiento de datos")
        chirps_service.process_data()
        menssage.success("Finalizacion procesamiento de datos")
    except Exception as ex:
        menssage.error(f"error {ex}")
