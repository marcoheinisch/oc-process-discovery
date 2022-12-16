class SingletonClass(object):
  # Override the default __new__ method to create a single instance of the class
  def __new__(cls):
    # Check if an instance of the class already exists
    if not hasattr(cls, 'instance'):
      # Create a new instance of the class and store it in the instance attribute
      cls.instance = super(SingletonClass, cls).__new__(cls)
    # Return the existing instance of the class
    return cls.instance

# Create a singleton instance of the SingletonClass
singleton = SingletonClass()

class DataManagementSystem():
  # Store data in the singleton instance of the SingletonClass
  def store(data):
    SingletonClass.singleton = data

  # Load data from the singleton instance of the SingletonClass
  def load():
    return SingletonClass.singleton
