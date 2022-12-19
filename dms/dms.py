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
    @classmethod
    def store(cls, key, contents):
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Store the data in the data attribute of the singleton instance
        singleton_instance.data[key] = contents
        
    @classmethod
    def load(cls, key):
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        return singleton_instance.data.get(key)
    
    @classmethod
    def delete(cls, key):
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        if key in singleton_instance.data:
            del singleton_instance.data[key]
        else:
            raise Warning("Key not found in DataManagement. Cannot delete.")
        
    @classmethod
    def select(cls, key):
        singleton_instance = SingletonClass()
        singleton_instance.selected = key
        
    @classmethod
    def all_keys(cls):
        # Get the single instance of the SingletonClass object
        singleton_instance = SingletonClass()
        # Retrieve the data from the data attribute of the singleton instance
        return list(singleton_instance.data.keys())


