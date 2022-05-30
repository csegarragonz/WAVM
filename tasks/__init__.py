from invoke import Collection

from . import criu
from . import dev
from . import docker

ns = Collection(
    criu,
    dev,
    docker,
)
