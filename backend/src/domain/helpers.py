from src.core import RedFlag, AnonymousRedFlag, UserId


class RedFlagMappingHelper:

    def map_to_anonymous(self, current_user: UserId, red_flag: RedFlag) -> AnonymousRedFlag:
        ...
