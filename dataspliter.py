
import splitfolders

splitfolders.ratio('fishdata', output="seperated_data",
    seed=1337, ratio=(.8, .1, .1), group_prefix=None, move=False)