def register_as_triggered(*field_names):
    def decorator(func):
        func._triggers = field_names
        return func
    return decorator
