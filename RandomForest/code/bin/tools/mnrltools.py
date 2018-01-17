# MNRL stuff
import mnrl

# Make MNRL chains for HSCompile + Hyperscan
# This function uses one STE per feature
# def make_hsc_chains(chains):
#
#     # Make a new MNRL Network called chains
#     mnrl_network = mnrl.MNRLNetwork('chains')
#
#     for chain in chains:
#
#         report_code = chain.chain_id_
#         previous_id = None
#
#         # Go through each state in the chain
#         for i, state in enumerate(chain.nodes_):
#
#             # Make the first node an enable-on START node that doesn't report
#             if i == 0:
#
#                               # symbols, enable = MNRLDefs.ENABLE_ON_ACTIVATE_IN,
#                               #     id=<id>, report=<False>, latched=<False>,
#                               #         reportId=<None>, attributes={}
#                 #node = mnrl_network.addHState(

# Make MNRL chains for CPU/GPU
# This function uses one STE per feature, and includes inequalities (GT, or LTEQ) and floating point thresholds
def make_mnrl_chains(chains):

    # Make a new MNRL Network called Chains
    mnrl_network = mnrl.MNRLNetwork('chains')

    for chain in chains:

        report_code = chain.chain_id_
        previous_id = None

        # Go through each state in the chain..
        for i, state in enumerate(chain.nodes_):

            # Make the first node an enable-on START node that doesn't report
            if i == 0:
                node = mnrl_network.addPFPState(state.feature_,
                                                state.threshold_,
                                                greaterThan=state.gt_,
                                                reportId=report_code,
                                                report=False,
                                                enable=mnrl.MNRLDefs.ENABLE_ON_START_AND_ACTIVATE_IN)

            # Make the last node report
            elif i == (len(chain.nodes_) - 1):
                node = mnrl_network.addPFPState(state.feature_,
                                                state.threshold_,
                                                greaterThan=state.gt_,
                                                reportId=report_code,
                                                report=True)

            # Make all others neither report nor start
            else:
                node = mnrl_network.addPFPState(state.feature_,
                                                state.threshold_,
                                                greaterThan=state.gt_,
                                                report=False)

            # previous node -> current node
            if i > 0:
                mnrl_network.addConnection((previous_id,
                                            mnrl.MNRLDefs.PFP_STATE_OUTPUT),
                                           (node.id,
                                            mnrl.MNRLDefs.PFP_STATE_INPUT))

            # Set previous id for next iteration
            previous_id = node.id

    return mnrl_network