"""Module implements custom exceptions for error handling for the A* GUI project

Author: Suvrat Jain <suvrat_jain@outlook.com>
"""
class Error(Exception):
    """Parent class for custom errors"""
    pass
class TooManyObstaclesError(Error):
    pass
class InvalidCoordinateError(Error):
    pass