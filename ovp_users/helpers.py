from django.conf import settings

def get_settings(string="OVP_USERS"):
  return getattr(settings, string, {})

def import_from_string(name):
  components = name.split('.')
  mod = __import__(components[0])
  for comp in components[1:]:
    mod = getattr(mod, comp)
  return mod
