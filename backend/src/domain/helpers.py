from src.core import RedFlag, AnonymousRedFlag


class RedFlagMappingHelper:

    def map_to_anonymous(self, red_flag: RedFlag) -> AnonymousRedFlag:
        ...
