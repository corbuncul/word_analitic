from app.core.db import Base


class StopWord(Base):
    pass

    def __repr__(self):
        return f'{self.word}'
