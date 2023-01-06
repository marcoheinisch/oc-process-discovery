import os
import base64
from pm4py.objects.ocel.obj import OCEL
import pm4py

from utils.constants import UPLOAD_DIRECTORY
import shutil

class SingletonClass(object):
    # Override the default __new__ method to create a single instance of the class
    def __new__(cls):
        # Check if an instance of the class already exists
        if not hasattr(cls, 'instance'):
            # Create a new instance of the class and store it in the instance attribute
            cls.instance = super(SingletonClass, cls).__new__(cls)
            # Initialize the data attribute as an empty dictionary
            cls.instance.data = {}
            cls.instance.selected = 'example_order_process.jsonocel'
        # Return the existing instance of the class
        return cls.instance

class DataManagementSystem:
    @classmethod
    def __add_version_control(cls, key):
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        list_key = key + '_filter_list'
        # Start the list with the original log (and then append new, filtered logs)
        # Store a separate filtering-list per log
        list_values = [singleton_instance.data[key]]
        singleton_instance.data[list_key] = list_values

    @classmethod
    def store_version_control(cls, key, ocel):
        list_key = key + '_filter_list'
        filter_list = cls.__load(list_key)
        filter_list.append(ocel)
    @classmethod
    def load_version_control(cls, key) -> OCEL:
        list_key = key + '_filter_list'
        filter_list = cls.__load(list_key)
        loaded = filter_list[len(filter_list) - 1]
        if type(loaded) is OCEL:
            return loaded
        return pm4py.read_ocel(loaded)

    @classmethod
    def store(cls, key, content):
        """Save content to file and store path in singleton instance"""
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Store the data infile and store path in singleton instance
        data = content.encode("utf8").split(b";base64,")[1]
        path = os.path.join(UPLOAD_DIRECTORY, key)
        with open(path, "wb+") as fp:
            fp.write(base64.decodebytes(data))
        singleton_instance.data[key] = path
        # Add version control for future filtering
        cls.__add_version_control(key)
        
    @classmethod
    def __load(cls, key):
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        return singleton_instance.data.get(key)
        
    @classmethod
    def __load_selected(cls) -> OCEL:
        """Get path of selected ocel
        """
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        return cls.load_version_control(singleton_instance.selected)

    @classmethod
    def get_ocel(cls) -> OCEL:
        return cls.__load_selected()
        
    @classmethod
    def select(cls, key):
        """Set selected ocel"""
        singleton_instance = SingletonClass()
        singleton_instance.selected = key
        
    @classmethod
    def all_upload_keys(cls) -> list[str]:
        """Get all keys stored in singleton instance"""
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        funct = lambda x: UPLOAD_DIRECTORY in x[1]
        return dict(list(filter(funct, singleton_instance.data.items()))).keys()

    @classmethod
    def register(cls, key, path):
        """Store already existing ocel path in singleton instance"""
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Store the data infile and store path in singleton instance
        singleton_instance.data[key] = path
        # Add version control for future filtering
        if UPLOAD_DIRECTORY in path:
            cls.__add_version_control(key)

    @staticmethod
    def reset_to_original(key):
        singleton_instance = SingletonClass()
        list_key = key + '_filter_list'
        singleton_instance.data[list_key] = [singleton_instance.data[list_key][0]]

    @classmethod
    def rollback(cls):
        singleton_instance = SingletonClass()
        list_key = singleton_instance.selected + '_filter_list'
        filter_list = cls.__load(list_key)
        if len(filter_list) > 1:
            filter_list.pop()

    @classmethod
    def rollback_all(cls):
        singleton_instance = SingletonClass()
        list_key = singleton_instance.selected + '_filter_list'
        filter_list = cls.__load(list_key)
        while len(filter_list) > 1:
            filter_list.pop()

    def clear(self):
        if os.path.exists("data/uploads"):
            shutil.rmtree("data/uploads")
        SingletonClass().data = {}
        os.mkdir("data/uploads")
        shutil.copy("data/resources/initial/example_order_process.jsonocel",
                    "data/uploads/example_order_process.jsonocel")
        self.register("example_order_process.jsonocel", "data/uploads/example_order_process.jsonocel")
        self.select("example_order_process.jsonocel")

    def delete_selected(self):
        singleton_instance = SingletonClass()
        if len(self.all_upload_keys()) == 1:
            raise Exception
        else:
            key = singleton_instance.selected
            data = singleton_instance.data
            list_key = key + '_filter_list'
            del data[list_key]
            os.remove(data[key])
            del data[key]
            for key in data.keys():
                self.select(key)
                break









