import sys
from dependency_injector.wiring import Provide, inject

from infrastructure.container import Container


def wire_modules():
    container = Container()
    container.wire(modules=[sys.modules[__name__]])


@inject
def run_app(chirps_service=Provide[Container.chirps_service]):
    chirps_service.get_data()
