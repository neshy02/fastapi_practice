from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

weather_city = {
    'Murmansk': -30,
    'Paris': 20,
    'Moscow': 14,
    'SPB': 10,
    'Tokio': 35
}

class NewCity(BaseModel):
    city: str
    temp: int | float



@app.post('/weather/')
async def new_city(payload: NewCity):
    name = payload.city
    temp = payload.temp

    weather_city[name.title()] = temp

    return {
        'status': 'Город успешно добавлен',
        'added': {name.title(): temp}
    }

@app.get('/weather/{city}')
async def get_weather(
    city: str,
    units: Annotated[
        str, 
        Query( 
            pattern="^(celsius|farenheit)$",    
            description="Введите celсsius или farenheit",
            title='Единицы измерения температуры'
        )
    ] = 'celsius'
):
    city = city.title()

    if city not in weather_city:
        raise HTTPException(status_code=404, detail='Ваш город был захвачен инопланетянами, данные отсуствуют!')

    temp_c = weather_city[city]

    if units.lower() == 'farenheit':
        temp_f = (temp_c * 9/5) + 32
        return {'city': city, 'temp': temp_f, 'units': 'Farenheit'}

    return {'city': city, 'temp': temp_c, 'units': 'Celsius'}



