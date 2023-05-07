import typing

class SnapchatMarketingBase(object):
    def __init__(self) -> None:
        self.id: typing.Union[str, None, int] = None
    
    def __hash__(self) -> int:
        class_name = type(self).__name__
        return hash((class_name, self.id))
    
    def __dict__(self) -> typing.Dict[str, typing.Any]: # type: ignore
        return {
            k: getattr(self, k)
            for k in self.__class__.__annotations__.keys()
        }