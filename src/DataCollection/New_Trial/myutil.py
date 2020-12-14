from NumericStringParser import *
import re

# Math Expression Evaluator
NSP = NumericStringParser()

# Datasize checker
class DatasizeInputChecker():

    def __init__(self, input_str = ""):
        self.input = input_str

    def check(self, input = ""):
        if input == "":
            input = self.input

        pattern = re.compile("^[1-9](d{0,3})[G,M,K]_\d{1,3}$")
        return pattern.match(input)

DSRCHECKER = DatasizeInputChecker()