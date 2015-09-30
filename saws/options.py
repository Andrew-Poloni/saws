# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import unicode_literals
from __future__ import print_function
from enum import Enum
import os
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
from awscli.customizations.emr.constants import LIST_CLUSTERS_ACTIVE_STATES, \
    LIST_CLUSTERS_TERMINATED_STATES, LIST_CLUSTERS_FAILED_STATES
from .data_util import DataUtil


class AwsOptions(object):
    """Encapsulates AWS command options such as ec2 running states.

    Some options can be obtained from the awscli, while others cannot.
    For example:
        Option: --ec2-state completions are not found in the awscli
            Completions for --ec2-state should be added to data/OPTIONS.txt
        Option: --cluster-states are found in the awscli
            See get_cluster_states()

    Attributes:
        * all_commands: A list of all commands, sub_commands, options, etc
            from data/SOURCES.txt.
        * EC2_STATE_OPT: A string representing the option for ec2 states
        * CLUSTER_STATE_OPT: A string representing the option for cluster states
        * ec2_states: A list of the possible EC2 instance states.
        * cluster_states: A list of the possible cluster states.
        * options_map: A dict mapping of options keywords and
            options to complete
        * log_exception: A callable log_exception from SawsLogger.
    """

    class OptionType(Enum):
        """Enum specifying the command type.

        Attributes:
            * EC2_STATES: An int representing ec2 running states.
            * CLUSTER_STATES: An int representing cluster running states.
        """

        NUM_TYPES = 2
        EC2_STATES, CLUSTER_STATES = range(NUM_TYPES)

    OPTIONS_DIR = os.path.dirname(os.path.realpath(__file__))
    OPTIONS_PATH = os.path.join(OPTIONS_DIR, 'data/OPTIONS.txt')

    def __init__(self,
                 all_commands,
                 log_exception):
        """Initializes AwsResources.

        Args:
            * all_commands: A list of all commands, sub_commands, options, etc
                from data/SOURCES.txt.
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        self.all_commands = all_commands
        self.EC2_STATE_OPT = '--ec2-state'
        self.CLUSTER_STATE_OPT = '--cluster-states'
        self.option_headers = [self.make_header(self.EC2_STATE_OPT)]
        self.ec2_states = []
        self.cluster_states = []
        self.data_util = DataUtil()
        self.header_to_type_map = self.data_util.create_header_to_type_map(
            headers=self.option_headers,
            data_type=self.OptionType)
        self.ec2_states, _ = DataUtil().get_data(self.OPTIONS_PATH,
                                                 self.header_to_type_map,
                                                 self.OptionType)
        self.get_cluster_states()
        self.options_map = dict(zip([self.EC2_STATE_OPT,
                                     self.CLUSTER_STATE_OPT],
                                    [self.ec2_states,
                                     self.cluster_states]))
        self.log_exception = log_exception

    def make_header(self, option):
        """Creates the header string in OPTIONS.txt from the given option.

        Args:
            * option: A string that represents an option.

        Returns:
            A string that represents the header in OPTIONS.txt for the
                given option.
        """
        return option + ': '

    def get_cluster_states(self):
        """Gets all the cluster states from the official AWS CLI.

        Args:
            * None.

        Returns:
            None.

        Raises:
            Exception: An error occurred doing xxx.
        """
        self.cluster_states.extend(LIST_CLUSTERS_ACTIVE_STATES)
        self.cluster_states.extend(LIST_CLUSTERS_TERMINATED_STATES)
        self.cluster_states.extend(LIST_CLUSTERS_FAILED_STATES)
