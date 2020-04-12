from critter.critter import Critter


class Invisible(Critter):
    type = "invisible"

    def is_resistant(self) -> bool:
        return False

    def can_go_invisible(self) -> bool:
        return True
