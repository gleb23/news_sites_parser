from syntan import Syntan

__author__ = 'gleb23'

class Executor(object):
    def __init__(self, source):
        self.source = source
    def execute(self):
        flowTree = Syntan(self.source).parse()
        for instruction in flowTree.block.instructions:
            instruction.execute()