#!/usr/bin/env python3
"""
Base module for data storage
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}  # ✅ Ensure DATA dictionary exists


class Base:
    """ Base model for persistent storage """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Base instance """
        s_class = self.__class__.__name__
        if s_class not in DATA:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at'):
            self.created_at = datetime.strptime(
                kwargs['created_at'], TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()

        if kwargs.get('updated_at'):
            self.updated_at = datetime.strptime(
                kwargs['updated_at'], TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Check object equality """
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert object to JSON format """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            result[key] = value.strftime(TIMESTAMP_FORMAT) if isinstance(
                value, datetime) else value
        return result

    @classmethod
    def load_from_file(cls):
        """ Load all objects from file storage """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"

        if s_class not in DATA:
            DATA[s_class] = {}  # ✅ Ensure class name exists in DATA

        if not path.exists(file_path):
            return  # ✅ No file exists yet, skip loading

        with open(file_path, 'r') as f:
            try:
                objs_json = json.load(f)
                for obj_id, obj_json in objs_json.items():
                    DATA[s_class][obj_id] = cls(**obj_json)
            except json.JSONDecodeError:
                DATA[s_class] = {}  # ✅ Handle file corruption gracefully

    @classmethod
    def save_to_file(cls):
        """ Save all objects to file storage """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"

        if s_class not in DATA:
            DATA[s_class] = {}  # ✅ Prevent KeyError

        objs_json = {obj_id: obj.to_json(
            True) for obj_id, obj in DATA[s_class].items()}

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """ Save the current object to storage """
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()

        if s_class not in DATA:
            DATA[s_class] = {}

        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """ Remove the object from storage """
        s_class = self.__class__.__name__
        if s_class in DATA and self.id in DATA[s_class]:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ Count all objects in the database """
        s_class = cls.__name__
        return len(DATA.get(s_class, {}))  # ✅ Prevent KeyError

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """ Return all objects """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """ Retrieve an object by its ID """
        s_class = cls.__name__
        return DATA.get(s_class, {}).get(id)  # ✅ Prevent KeyError

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """ Search for objects matching attributes """
        s_class = cls.__name__

        if s_class not in DATA:
            return []  # ✅ Prevent KeyError

        def _search(obj):
            for k, v in attributes.items():
                if getattr(obj, k, None) != v:  # ✅ Prevent AttributeError
                    return False
            return True

        return list(filter(_search, DATA[s_class].values()))
