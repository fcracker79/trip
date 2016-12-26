import typing

import abc


class VersionNode(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def version_name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def dependencies(self) -> typing.Set['VersionNode']:
        pass
