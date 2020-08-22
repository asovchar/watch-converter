from converter.image import MyImage


class BaseAlgorithm:
    def process(self, img: MyImage) -> MyImage:
        raise NotImplementedError()
