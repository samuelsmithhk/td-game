from critter.critter import Critter


class BaseBoss(Critter):
    type = "base_boss"

    def is_resistant(self) -> bool:
        return False

    def can_go_invisible(self) -> bool:
        return False
