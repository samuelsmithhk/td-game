from critter.critter import Critter


class SpeederBoss(Critter):
    type = "speeder_boss"

    def is_resistant(self) -> bool:
        return False

    def can_go_invisible(self) -> bool:
        return False
