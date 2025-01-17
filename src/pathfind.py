from typing import List, Tuple
from collections import namedtuple, deque

from .exception import OutOfBoundsError, NoPossiblePath

Coord = namedtuple("Coord", "x y") 

class Map(object):
    """
    The 2D game map of passable and blocked coordinates 
    together with the start coordinate (P) and end 
    coordinate (Q).

    ...

    Attributes
    ----------
    array : List[str]
        The game map as a 2D array.
    y_extent : int
        The size of the game map in the y extent. 
    x_extent : int
        The size of the game map in the y extent. 
    p : Coord
        The start coordinate. 
    q : Coord
        The end coordinate. 
    """
    def __init__(self, array: str, p: Coord, q: Coord):
        self.array = list(map(lambda x: x.split(), array.split("\n")))
        self.y_extent = len(self.array)
        self.x_extent = len(self.array[0])
        self._validate_coord(p)
        self.p = p
        self._validate_coord(q)
        self.q = q

    def _validate_coord(self, coord: Coord):
        """
        Validate whether a given coordinate is valid i.e. resides
        within the map. 

            Parameters:
                    coord (Coord): The coord to check. 
            Returns:
                    bool: Whether or not the coordinate is valid. 
        """
        errors = []
        if coord.y < 0:
            errors.append("y coordinate must not be negative")
        if coord.x < 0:
            errors.append("x coordinate must not be negative")
        if coord.y >= self.y_extent:
            errors.append(f"y coordinate must be maximum {self.y_extent-1}")
        if coord.x >= self.x_extent:
            errors.append(f"x coordinate must be maximum {self.x_extent-1}")
        
        if len(errors) > 0:
            raise OutOfBoundsError(f"Invalid coordinate ({coord.x}, {coord.y}): {errors})")
    
    def _is_passable(self, coord: Coord) -> bool:
        """
        Find whether a coordinate is passable.

            Parameters:
                    coord (Coord): The coord to check. 
            Returns:
                    bool: Whether or not the coordinate is passable. 
                          Return False if the coordinate is out of the bounds
                          of the map.  
        """
        try:
            self._validate_coord(coord)
            return self.array[coord.y][coord.x] != "#"
        except OutOfBoundsError:
            return False

    def _get_neighbours(self, coord: Coord):
        """
        Get the passable neighbours of the given coord. 

            Parameters:
                    coord (Coord): The coord for which to get neighbours. 
            Returns:
                    [Coord]: An iterator of neighbour coords.  
        """
        for x, y in [(coord.x-1, coord.y), (coord.x+1, coord.y), (coord.x, coord.y-1), (coord.x, coord.y+1)]:
            neighbour = Coord(x=x, y=y)
            if self._is_passable(neighbour):
                yield neighbour
    
    def get_shortest_path(self) -> int:
        """
        Perform a breadth-first search to find the shortest path between
        the P and Q coordinates via passable squares. 

            Returns:
                    int: The number of steps in the shortest path between P and Q. 
        """
        if self.p == self.q:
            return 0
        visited = set([self.p])
        queue = deque([(self.p, 0)])

        while len(queue) > 0:
            coord, steps = queue.popleft()
            for neighbour in self._get_neighbours(coord):
                if neighbour == self.q:
                    return steps + 1
                if neighbour not in visited:
                    queue.append((neighbour, steps + 1))
                    visited.add(neighbour)
        
        raise NoPossiblePath("Not possible to reach Q from P")


def pathfind(array: str, p: Coord, q: Coord):
    """
    Find the shortest path between coordinates P and Q in the given 2D array map.

        Parameters:
                array: String input of 2D map. 
                p: The start coordinate. 
                q: The end coordinate. 
        
        Returns:
                int: The number of steps in the shortest path between P and Q. 
    """
    grid_map = Map(array, p, q)
    return grid_map.get_shortest_path()

