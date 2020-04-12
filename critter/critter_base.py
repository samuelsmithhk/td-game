from critter.critter import Critter


class Base(Critter):
    type = "base"

    def is_resistant(self) -> bool:
        return False

    def can_go_invisible(self) -> bool:
        return False
