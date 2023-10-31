from enum import Enum
from fastapi import FastAPI, Path
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


# реализация пути /
@app.get('/')
def root():
    return {"message": "Welcome to The Vet Clinic Service!"}


# реализация пути /post
@app.post('/post')
def get_post(new_timestamp: Timestamp):
    if new_timestamp.id in post_db:
        raise HTTPException(status_code=409,
                            detail="The specified id already exists.")
    else:
        post_db.append(new_timestamp)
    return new_timestamp

# реализация получения собак по типу
@app.get('/dog')
def get_dogs(kind: DogType):
    return [dog for dog in dogs_db.values() if dog.kind == kind]


# реализация записи собак
@app.post('/dog')
def create_dog(new_dog: Dog):
    if new_dog.pk in dogs_db:
        raise HTTPException(status_code=409,
                            detail="The specified PK already exists.")
    else:
        dogs_db[new_dog.pk] = new_dog
        return new_dog


# реализация получения собаки по id
@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int):
    return dogs_db[pk]


# реализация обновления собаки по id
@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, new_dog: Dog):
    stored_dog_data = dogs_db[pk]
    update_data = new_dog.dict(exclude_unset=True)
    updated_dog = stored_dog_data.copy(update=update_data)
    dogs_db[pk] = jsonable_encoder(updated_dog)
    return updated_dog

