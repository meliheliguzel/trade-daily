class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def reset(cls) -> None:
        if cls in cls._instances:
            instance = cls._instances[cls]
            if hasattr(instance, "close_connection"):
                try:
                    instance.close_connection()
                except Exception:
                    pass
            del cls._instances[cls]
