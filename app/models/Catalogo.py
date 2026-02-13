# Modelo generico de catalogo - representa un registro de cualquier tabla de catalogo


class Catalogo:
    def __init__(self, id_value=None, **kwargs):
        self.id = id_value
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<Catalogo(id={self.id})>"
