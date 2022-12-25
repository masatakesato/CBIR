try:
    from .serializerimpl_umgspack import Serializer
except:
    from .serializerimpl_msgpack import Serializer
