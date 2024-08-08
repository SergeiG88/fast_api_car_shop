from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

# Загрузка данных из JSON файла
with open('data/cars.json', 'r', encoding='utf-8') as f:
    cars = json.load(f)

# Модель данных для Pydantic
class Car(BaseModel):
    id: int
    make: str
    model: str
    year: int
    price: int
    description: str
    features: List[str]
    image: str

@app.get("/")
def home_page():
    return {"message_1": "Приветствую вас в данном Fast API приложении",
            "message_2": "http://127.0.0.1:8000/cars",
            "message_3": "http://127.0.0.1:8001/cars/{id}",
            "message_4": "http://127.0.0.1:8001/docs"
            }

@app.get("/cars", response_model=List[Car])
async def get_cars():
    return cars

@app.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: int):
    car = next((car for car in cars if car["id"] == car_id), None)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@app.post("/cars", response_model=Car)
async def add_car(car: Car):
    if any(existing_car["id"] == car.id for existing_car in cars):
        raise HTTPException(status_code=400, detail="Car with this ID already exists")
    cars.append(car.dict())
    with open('data/cars.json', 'w', encoding='utf-8') as f:
        json.dump(cars, f, ensure_ascii=False, indent=4)
    return car

@app.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: int, updated_car: Car):
    car_index = next((index for (index, car) in enumerate(cars) if car["id"] == car_id), None)
    if car_index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    cars[car_index] = updated_car.dict()
    with open('data/cars.json', 'w', encoding='utf-8') as f:
        json.dump(cars, f, ensure_ascii=False, indent=4)
    return updated_car

@app.delete("/cars/{car_id}", response_model=Car)
async def delete_car(car_id: int):
    car_index = next((index for (index, car) in enumerate(cars) if car["id"] == car_id), None)
    if car_index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    deleted_car = cars.pop(car_index)
    with open('data/cars.json', 'w', encoding='utf-8') as f:
        json.dump(cars, f, ensure_ascii=False, indent=4)
    return deleted_car

