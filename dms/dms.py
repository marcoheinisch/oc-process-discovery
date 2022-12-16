class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance

singleton = SingletonClass()

class DataManagementSystem():
  def store(data):
    SingletonClass.singleton = data

  def load():
    return SingletonClass.singleton