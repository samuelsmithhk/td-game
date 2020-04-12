from critter.critter import Critter


class Resistant(Critter):
    type = "resistant"

    def is_resistant(self) -> bool:
        return True

    def can_go_invisible(self) -> bool:
        return False
