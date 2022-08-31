import re

class PrecedenceAdjustmentSpecification(object):

    def is_satisfied_by(self, value):
        #print(value)
        regex_rules = [
            r'^pa(.*)an$',
            r'^ma(.*)an$',
            r'^ka(.*)an$',
            r'^bra(.*)an$',
        ]

        for rule in regex_rules:
            if re.match(rule, value):
                return True

        return False



