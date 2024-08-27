class DatabaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MatchNotFoundError(DatabaseError):
    def __init__(self, match_uuid: str):
        super().__init__(f"Match with ID {match_uuid} not found.")
