import unittest

from labautomation_utils.coordconversion import (
    CoordinateSystem,
    PlateIndexConverterFactory,
)


class CoordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.plateDim = (12, 8)

    def test_IdxAlphaMajor_To(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.IdxNumMajor,
            targetFormat=CoordinateSystem.IdxAlphaMajor,
        )
        A = [0, 12, 5, 22]
        B = [0, 1, 40, 81]
        for a, b in zip(A, B):
            with self.subTest(i=(a, b)):
                b2 = conv.Convert(a)
                self.assertEqual(b, b2)

    def test_IdxAlphaMajor_From(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.IdxAlphaMajor,
            targetFormat=CoordinateSystem.IdxNumMajor,
        )
        A = [0, 12, 5, 22]
        B = [0, 1, 40, 81]
        for a, b in zip(A, B):
            with self.subTest(i=(b, a)):
                a2 = conv.Convert(b)
                self.assertEqual(a, a2)

    def test_IdxRowColumn_To(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.IdxNumMajor,
            targetFormat=CoordinateSystem.IdxRowColumn,
        )
        A = [0, 12, 5, 22]
        B = [(0, 0), (0, 1), (5, 0), (10, 1)]
        for a, b in zip(A, B):
            with self.subTest(i=(a, b)):
                b2 = conv.Convert(a)
                self.assertEqual(b, b2)

    def test_IdxRowColumn_From(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.IdxRowColumn,
            targetFormat=CoordinateSystem.IdxNumMajor,
        )
        A = [0, 12, 5, 22]
        B = [(0, 0), (0, 1), (5, 0), (10, 1)]
        for a, b in zip(A, B):
            with self.subTest(i=(b, a)):
                a2 = conv.Convert(b)
                self.assertEqual(a, a2)

    def test_NamedZeroPadded_To(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.IdxNumMajor,
            targetFormat=CoordinateSystem.NamedZeroPadded,
        )
        A = [0, 12, 5, 22]
        B = ["A01", "B01", "A06", "B11"]
        for a, b in zip(A, B):
            with self.subTest(i=(a, b)):
                b2 = conv.Convert(a)
                self.assertEqual(b, b2)

    def test_NamedZeroPadded_From(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.NamedZeroPadded,
            targetFormat=CoordinateSystem.IdxNumMajor,
        )
        A = [0, 12, 5, 22]
        B = ["A01", "B01", "A06", "B11"]
        for a, b in zip(A, B):
            with self.subTest(i=(b, a)):
                a2 = conv.Convert(b)
                self.assertEqual(a, a2)

    def test_Named_To(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.IdxNumMajor,
            targetFormat=CoordinateSystem.Named,
        )
        A = [0, 12, 5, 22]
        B = ["A1", "B1", "A6", "B11"]
        for a, b in zip(A, B):
            with self.subTest(i=(a, b)):
                b2 = conv.Convert(a)
                self.assertEqual(b, b2)

    def test_Named_From(self):
        conv = PlateIndexConverterFactory.Build(
            plateDim=self.plateDim,
            srcFormat=CoordinateSystem.Named,
            targetFormat=CoordinateSystem.IdxNumMajor,
        )
        A = [0, 12, 5, 22]
        B = ["A1", "B1", "A6", "B11"]
        for a, b in zip(A, B):
            with self.subTest(i=(b, a)):
                a2 = conv.Convert(b)
                self.assertEqual(a, a2)


if __name__ == "__main__":
    unittest.main()
