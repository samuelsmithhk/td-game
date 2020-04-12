from critter.critter import Critter


class Speeder(Critter):
    type = "speeder"

    def is_resistant(self) -> bool:
        return False

    def can_go_invisible(self) -> bool:
        return False
