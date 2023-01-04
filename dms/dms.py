import os
import base64

from utils.constants import UPLOAD_DIRECTORY

class SingletonClass(object):
    # Override the default __new__ method to create a single instance of the class
    def __new__(cls):
        # Check if an instance of the class already exists
        if not hasattr(cls, 'instance'):
            # Create a new instance of the class and store it in the instance attribute
            cls.instance = super(SingletonClass, cls).__new__(cls)
            # Initialize the data attribute as an empty dictionary
            cls.instance.data = {}
            cls.instance.selected = None
        # Return the existing instance of the class
        return cls.instance

class DataManagementSystem:
    """Singleton class to manage data storage and retrieval"""
    # A changeable variable of the Singelton storing a configuration dict
    sap_config = {
        'user': '',
        'passwd': '',
        'ashost': '',
        'saprouter': '',
        'msserv': '',
        'sysid': '',
        'group': '',
        'client': '',
        'lang': '',
        'trace': ''
    }
    use_sqlite = False
    
    @classmethod
    def store(cls, key, contents):
        """Save content to file and store path in singleton instance"""
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Store the data infile and store path in singleton instance
        data = contents.encode("utf8").split(b";base64,")[1]
        path = os.path.join(UPLOAD_DIRECTORY, key)
        with open(path, "wb+") as fp:
            fp.write(base64.decodebytes(data))
        singleton_instance.data[key] = path
       
        
    @classmethod
    def load(cls, key) -> str:
        """Get path of ocel from key
        """
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        return singleton_instance.data.get(key)       
        
    @classmethod
    def load_selected(cls) -> str:
        """Get path of selected ocel
        """
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        return singleton_instance.data.get(singleton_instance.selected)

    @classmethod
    def delete(cls, key):
        """NOT IMPLEMENTED: Delete ocel from key and from filesystem"""
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        if key in singleton_instance.data:
            #todo delete file
            del singleton_instance.data[key]
        else:
            raise Warning("Key not found in DataManagement. Cannot delete.")
        
    @classmethod
    def select(cls, key):
        """Set selected ocel"""
        singleton_instance = SingletonClass()
        singleton_instance.selected = key
        
    @classmethod
    def all_keys(cls) -> list[str]:
        """Get all keys stored in singleton instance"""
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        return list(singleton_instance.data.keys())


    @classmethod
    def register(cls, key, path):
        """Store already existing ocel path in singleton instance"""
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Store the data infile and store path in singleton instance
        singleton_instance.data[key] = path