import sys
from dependency_injector.wiring import Provide, inject

from infrastructure.container import Container
from infrastructure.data_source_service.data_source_service import ExternalDataSourceService


def wire_modules():
    container = Container()
    container.wire(modules=[sys.modules[__name__]])


@inject
def run_app(chirps_service: ExternalDataSourceService = Provide[Container.chirps_service]):
    chirps_service.get_data()
    chirps_service.process_data()
