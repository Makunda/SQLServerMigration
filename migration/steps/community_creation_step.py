from migration.procedure.community_procedure import CommunityProcedure
from migration.steps.asbtract_step import AbstractStep


class CommunityCreationStep(AbstractStep):
    def get_name(self) -> str:
        """
        Get the name of the step
        :return:
        """
        return "Community Creation Step"

    def launch(self):
        """
        Launch the steps
        :return:
        """
        community_procedure = CommunityProcedure()
        community_procedure.detect()