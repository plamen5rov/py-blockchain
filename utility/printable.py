class Printable:
    def __repr__(self):
        """Prints class as a dictionary"""
        return str(self.__dict__)