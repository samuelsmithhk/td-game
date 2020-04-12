from critter.critter import Critter


class InvisibleBoss(Critter):
    type = "invisible_boss"

    def is_resistant(self) -> bool:
        return False

    def can_go_invisible(self) -> bool:
        return True
