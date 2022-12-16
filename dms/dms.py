class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance

singleton = SingletonClass()

class DataManagementSystem():
<<<<<<< Updated upstream
  def store_in_dms(data):
    SingletonClass.singleton = data

  def load_from_dms():
    return SingletonClass.singleton

=======
  def store(data):
    SingletonClass.singleton = data

  def load():
    return SingletonClass.singleton
>>>>>>> Stashed changes
