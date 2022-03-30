from typing import List

from interfaces.imaging.imaging_object import ImagingObject
from migration.procedure.community_procedure import CommunityProcedure
from migration.steps.asbtract_step import AbstractStep
from services.imaging.transaction_service import TransactionService


class CommunityCreationStep(AbstractStep):

    def __int__(self):

        self.__community_procedure = CommunityProcedure()

        self.__transaction_service = TransactionService()
        self.__file_dir = self.workspace_util.merge_file("SQL Communities/")

    def get_name(self) -> str:
        """
        Get the name of the step
        :return:
        """
        return "Community Creation Step"

    def generate_monoliths_report(self):
        """
        Genrate the monolith report including all the communities above a certain threshold
        :return: None
        """
        # Build headers adding a community property
        headers_mono = ImagingObject.get_headers()
        headers_mono.append("Community")

        nodes = self.__community_procedure.get_all_nodes_as_imaging_object()
        value_map: List[List] = list()

        for n in nodes:
            community_val = self.__community_procedure.get_object_community(n.get_node())
            single_value_list = n.get_values()
            single_value_list.append(community_val)

            value_map.append(single_value_list)

        self.generate_excel("Object by Communities", self.__file_dir, headers_mono, value_map)

    def generate_transactions_silos(self):
        """
        Bind transaction
        :return:
        """
        # Build headers adding a community
        headers_mono = ImagingObject.get_headers()
        headers_mono.append("Communities")

        valu

        # Get the transaction by communities
        transaction_map = self.__community_procedure.get_transactions_by_communities()
        for community in transaction_map.keys():
            # List transaction
            transaction_imaging = self.__transaction_service.node_to_imaging_transaction()

    def launch_detection(self):
        """
        Launching the detection of community
        :return:
        """
        self.__community_procedure.detect()

    def launch(self):
        """
        Launch the steps
        :return:
        """
        self.launch_detection()

        self.generate_monoliths_report()