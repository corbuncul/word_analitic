from app.core.db import Base


class KeyWord(Base):
    pass

    def __repr__(self):
        return f'{self.word}'
