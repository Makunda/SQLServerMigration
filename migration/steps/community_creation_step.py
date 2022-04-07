from typing import List

from interfaces.imaging.imaging_object import ImagingObject
from interfaces.imaging.imaging_transaction import ImagingTransaction
from logger import Logger
from migration.interfaces.imaging_community import ImagingCommunity
from migration.procedures.community_procedure import CommunityProcedure
from migration.services.community_service import CommunityService
from migration.steps.asbtract_step import AbstractStep
from services.imaging.transaction_service import TransactionService


class CommunityCreationStep(AbstractStep):

    def __init__(self):
        super().__init__()
        self.__logger = Logger.get_logger("Community Creation Step")
        self.__community_procedure = CommunityProcedure()
        self.__community_service = CommunityService()

        self.__transaction_service = TransactionService()
        self.__file_dir = self.workspace_util.merge_file("SQL Communities/")

    def get_name(self) -> str:
        """
        Get the name of the step
        :return:
        """
        return "Community Creation Step"

    def generate_community_report(self):
        """
        Generate the monolith report including the list of the communities
        :return:
        """
        headers_com = ImagingCommunity.get_headers()
        value_list: List[List] = list()

        communities = self.__community_service.get_communities_map(self.get_application())
        for com in communities.keys():
            community_obj = self.__community_service.node_to_imaging_community(self.get_application(), com, communities[com])
            value_list.append(community_obj.get_values())

        self.generate_excel("Community Details", self.__file_dir, headers_com, value_list)
        self.__logger.info("Community details report has been generated")

    def generate_monoliths_report(self):
        """
        Generate the monolith report including all the communities above a certain threshold
        :return: None
        """
        # Build headers adding a community property
        headers_mono = ImagingObject.get_headers()
        headers_mono.append("Community")

        self.__logger.info("Retrieving Objects with associated communities.")
        nodes = self.__community_procedure.get_all_nodes_as_imaging_object()
        self.__logger.info("{} Objects retrieved.".format(len(nodes)))

        value_map: List[List] = list()

        for (i, n) in enumerate(nodes):
            if i % 50 == 0:
                self.__logger.info("Processing monolith {} on {}.".format(i, len(nodes)))

            community_val = self.__community_procedure.get_object_community(n.get_node())
            single_value_list = n.get_values()
            single_value_list.append(community_val)

            value_map.append(single_value_list)

        self.generate_excel("Objects by Communities", self.__file_dir, headers_mono, value_map)
        self.__logger.info("Monoliths report has been generated")

    def generate_transactions_silos(self) -> None:
        """
        Build the Transaction / Community Silo report
        :return: None
        """
        # Build headers adding a community
        headers_mono = ImagingTransaction.get_headers()
        headers_mono.append("Communities")

        value_map: List[List] = list()

        # Get the transaction by communities
        self.__logger.info("Retrieving list of transactions in the application.")
        transaction_map = self.__community_procedure.get_transactions_by_communities()
        self.__logger.info("{} Transactions retrieved.".format(len(transaction_map.keys())))

        for (i, transaction) in enumerate(transaction_map.keys()):
            if i % 50 == 0:
                self.__logger.info("Processing transaction {} on {}.".format(i, len(transaction_map.keys())))

            # List transaction
            imaging_transaction = self.__transaction_service.node_to_imaging_transaction(transaction)
            communities = self.__transaction_service.get_prop_value_list_in_transaction(transaction,
                                                                                        self.__community_procedure.get_community_property())

            single_value_list = imaging_transaction.get_values()
            single_value_list.append(communities)

            value_map.append(single_value_list)

        self.generate_excel("Transactions by Communities", self.__file_dir, headers_mono, value_map)
        self.__logger.info("Communities report has been generated")

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
        self.__logger.info("Database Community discovery..")
        self.launch_detection()

        self.__logger.info("Generating Monoliths report..")
        self.generate_monoliths_report()

        self.__logger.info("Generating Transaction per Silo reports..")
        self.generate_transactions_silos()

        self.__logger.info("Generating Community Details report..")
        self.generate_community_report()

