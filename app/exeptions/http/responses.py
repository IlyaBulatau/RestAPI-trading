from app.exeptions.http.shemas import Desciption, UserExeptionResponse

from typing import Any


class ResponseGenerator:
    
    def __init__(self, *args, title: str, status_code: int, descriptions: tuple[str, str]):
        self.title = title
        self.status_code = status_code
        self.description = descriptions
        self.args = args

    def generate_response(self, schema: UserExeptionResponse | Any = UserExeptionResponse):
        if self.args:
            text = self.description[1].format(*self.args)
        else:
            text = self.description[1]

        description = Desciption(
            field=self.description[0],
            text=text
        )

        return dict(schema(title=self.title, status=self.status_code, description=dict(description)))
        

