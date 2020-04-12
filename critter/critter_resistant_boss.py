from critter.critter import Critter


class ResistantBoss(Critter):
    type = "resistant_boss"

    def is_resistant(self) -> bool:
        return True

    def can_go_invisible(self) -> bool:
        return False
