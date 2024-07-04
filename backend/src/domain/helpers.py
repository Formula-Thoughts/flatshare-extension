from src.core import RedFlag, AnonymousRedFlag, UserId


class RedFlagMappingHelper:

    def map_to_anonymous(self, current_user: UserId, red_flag: RedFlag) -> AnonymousRedFlag:
        return AnonymousRedFlag(
            etag=red_flag.etag,
            partition_key=red_flag.partition_key,
            id=red_flag.id,
            body=red_flag.body,
            property_url=red_flag.property_url,
            votes=len(red_flag.votes),
            voted_by_me=current_user in red_flag.votes,
            date=red_flag.date
        )
