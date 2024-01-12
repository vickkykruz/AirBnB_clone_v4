#!/usr/bin/python3
"""
This is a sript that contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
        }


class FileStorage:
    """ This is a method that serializes instances to a JSON file &
    deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """This is a all method that returns the dictionary __objects """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """ This is a method that sets in __objects the obj with key
        <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """ This is a method that serializes __objects to the JSON file
        (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict(False)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """ This is a method that deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception as ex:
            pass

    def delete(self, obj=None):
        """ This is a method that delete obj from __objects if it’s
        inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """ This is a method that retrieve call reload() method for
        deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """ This is a method that retrieves all the data"""
        if cls in classes.values() and id and type(id) == str:
            d_obj = self.all(cls)
            for key, value in d_obj.items():
                if key.split(".")[1] == id:
                    return value
        return None

    def count(self, cls=None):
        """ This is a method that counts object/data """
        data = self.all(cls)
        if cls in classes.values():
            data = self.all(cls)
        return len(data)
