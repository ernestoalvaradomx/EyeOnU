import requests

from src.models.rawFrameModel import RawFrame

class RawFrameServiceMock:
    def __init__(self):
        self.imageTestId = 0
        self.urls = [
            'https://images.mubicdn.net/images/film/25580/cache-33736-1568750405/image-w1280.jpg?size=800x',
            'https://media.glamour.mx/photos/6660c97a58a6da682679023d/16:9/w_2560%2Cc_limit/bad-boys-con-will-smith-fecha-de-estreno.jpg',
            'https://i.ytimg.com/vi/r7jbePATC-U/maxresdefault.jpg'
        ]
        self.rawFrameList = self.getImagesTest()

    def getImagesTest(self) -> list[RawFrame]:
        rawFrameList = []
        for url in self.urls:
            img = requests.get(url).content
            rawFrameList.append(RawFrame(pixels=img))
        return rawFrameList
    
    def captureFrame(self) -> RawFrame:
        rawFrame = self.rawFrameList[self.imageTestId]
        self.imageTestId += 1
        if self.imageTestId >= len(self.urls):
            self.imageTestId = 0
        return rawFrame