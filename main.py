from fastapi import *
from pydantic import BaseModel
from gigachat import GigaChat

app = FastAPI()

class inputJSON(BaseModel):
    text : str
    num1 : int
    num2 : int

class outputJSON(BaseModel):
    explanation : str
    result : int

giga = GigaChat(
    credentials = " *ключ авторизации* ", # Заменить ключ авторизации
    verify_ssl_certs = False
)

@app.post("/answer", response_model=outputJSON)
def request_to_giga(input: inputJSON):
    prompt = f"{input.num1} {input.num2} {input.text}"

    body = {
        "model" : "GigaChat-2",
        "messages" : [
            {
                "role" : "user",
                "content" : prompt
            },
        ],
        "temperature" : 0.0,
        "functions" : [
            {
                "name" : "test",
                "parameters" : outputJSON.model_json_schema()
            }
        ],
        "function_call": {"name": "test"}
    }

    response = giga.chat(body)
    result = response.choices[0].message.function_call.arguments

    return outputJSON(**result)

