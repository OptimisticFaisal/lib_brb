class Rules(object):
    def __init__(self):
        self.rule_weight = 1
        self.parent = ""
        self.combinations = []
        self.antecedents_belief_dist = []
        self.consequence_val = []
        self.consequence_belief_dist = []
        self.matching_degree = None
        self.activation_weight = None
        self.individual_matching = None
