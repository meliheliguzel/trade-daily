from dataclasses import dataclass


@dataclass
class PieGraphData:
    VALUES: list
    NAMES: list


@dataclass
class BarGraphData:
    X: list
    Y: list

@dataclass
class ScatterGraphData:
    X: list
    Y: list
