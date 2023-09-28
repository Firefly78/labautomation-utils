from __future__ import annotations

import re
from enum import Enum, auto


class ConversionError(Exception):
    pass


class CoordinateSystem(Enum):
    IdxNumMajor = auto()
    IdxAlphaMajor = auto()
    IdxRowColumn = auto()
    NamedZeroPadded = auto()
    Named = auto()


class PlateIndexConverterFactory:
    @staticmethod
    def Build(**kwargs):
        """Build an object for handling coordinate conversion

        Args:
            plateDim (tuple): Plate dimension (X-axis, Y-axis)
            srcFormat (CoordinateSystem): Source coordinate format
            targetFormat (CoordinateSystem): Target coordinate format

        Returns:
            _type_: PlateIndexConverter object
        """
        return PlateIndexConverter(**kwargs)


class PlateIndexConverter:
    def __init__(self, **kwargs):
        self.plateDimX = kwargs["plateDim"][0]
        self.plateDimY = kwargs["plateDim"][1]
        self.srcFormat = kwargs["srcFormat"]
        self.targetFormat = kwargs["targetFormat"]

    class Converter:
        @staticmethod
        def FromCoord(coord, info: PlateIndexConverter):
            raise NotImplementedError

        @staticmethod
        def ToCoord(coord, info: PlateIndexConverter):
            raise NotImplementedError

    class IdxNumMajor(Converter):
        @staticmethod
        def FromCoord(coord, info: PlateIndexConverter):
            if info.plateDimX * info.plateDimY <= coord:
                raise ConversionError
            return coord  # Default format

        @staticmethod
        def ToCoord(coord, info: PlateIndexConverter):
            return coord  # Default format

    class IdxAlphaMajor(Converter):
        @staticmethod
        def FromCoord(coord, info: PlateIndexConverter):
            if info.plateDimX * info.plateDimY <= coord:
                raise ConversionError
            N, M = coord % info.plateDimY, coord // info.plateDimY
            return N * info.plateDimX + M

        @staticmethod
        def ToCoord(coord, info: PlateIndexConverter):
            N, M = coord % info.plateDimX, coord // info.plateDimX
            return N * info.plateDimY + M

    class IdxRowColumn(Converter):
        @staticmethod
        def FromCoord(coord, info: PlateIndexConverter):
            return coord[0] + info.plateDimX * coord[1]

        @staticmethod
        def ToCoord(coord, info: PlateIndexConverter):
            N, M = coord % info.plateDimX, coord // info.plateDimX
            return (N, M)

    class NamedZeroPadded(Converter):
        @staticmethod
        def FromCoord(coord, info: PlateIndexConverter):
            pattern = r"^([A-Z]+)([0-9]+)$"
            m = re.search(pattern, coord)
            alpha = m.group(1)
            num = m.group(2)
            return (ord(alpha) - 65) * info.plateDimX + int(num) - 1

        @staticmethod
        def ToCoord(coord, info: PlateIndexConverter):
            N, M = coord % info.plateDimX, coord // info.plateDimX
            return chr(M + 65) + f"{N+1:02}"

    class Named(Converter):
        @staticmethod
        def FromCoord(coord, info: PlateIndexConverter):
            pattern = r"^([A-Z]+)([0-9]+)$"
            m = re.search(pattern, coord)
            alpha = m.group(1)
            num = m.group(2)
            return (ord(alpha) - 65) * info.plateDimX + int(num) - 1

        @staticmethod
        def ToCoord(coord, info: PlateIndexConverter):
            N, M = coord % info.plateDimX, coord // info.plateDimX
            return chr(M + 65) + f"{N+1}"

    def Convert(self, coord):
        isList = isinstance(coord, list)
        if not isList:
            coord = [coord]

        lookup: dict[CoordinateSystem, PlateIndexConverter.Converter] = {
            CoordinateSystem.IdxNumMajor: PlateIndexConverter.IdxNumMajor,
            CoordinateSystem.IdxAlphaMajor: PlateIndexConverter.IdxAlphaMajor,
            CoordinateSystem.IdxRowColumn: PlateIndexConverter.IdxRowColumn,
            CoordinateSystem.NamedZeroPadded: PlateIndexConverter.NamedZeroPadded,
            CoordinateSystem.Named: PlateIndexConverter.Named,
        }

        new_coord = list()
        for i in coord:
            coord_ = lookup[self.srcFormat].FromCoord(i, self)
            new_coord.append(lookup[self.targetFormat].ToCoord(coord_, self))

        if not isList:
            return new_coord[0]
        return new_coord
