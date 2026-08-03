from abc import ABC, abstractmethod
import math


class Figure(ABC):
    PARAMETERS = []
    DESCRIPTION = ""
    FORMULA = ""

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def enter_data(self):
        pass

    @abstractmethod
    def show_result(self):
        pass

    def get_display_name(self):
        return self.name

    def get_parameters(self):
        return list(self.PARAMETERS)

    def get_description(self):
        return self.DESCRIPTION

    def get_formula(self):
        return self.FORMULA

    def set_values(self, values):
        for param in self.PARAMETERS:
            setattr(self, param["name"], float(values[param["name"]]))

    def get_values(self):
        return {param["name"]: getattr(self, param["name"]) for param in self.PARAMETERS}

    def validate(self):
        return None


class Figures2D(Figure):
    @abstractmethod
    def calculate_area(self):
        pass

    @abstractmethod
    def calculate_perimeter(self):
        pass

    def calculate_results(self):
        self.calculate_area()
        self.calculate_perimeter()
        results = [
            ("Area", self.area, "cm²"),
            ("Perimeter", self.perimeter, "cm"),
        ]
        results.extend(self._extra_results())
        return results

    def _extra_results(self):
        return []


class Figures3D(Figure):
    @abstractmethod
    def calculate_volume(self):
        pass

    @abstractmethod
    def calculate_surface_area(self):
        pass

    def calculate_results(self):
        self.calculate_volume()
        self.calculate_surface_area()
        results = [
            ("Volume", self.volume, "cm³"),
            ("Surface Area", self.surface_area, "cm²"),
        ]
        results.extend(self._extra_results())
        return results

    def _extra_results(self):
        return []


class Circle(Figures2D):
    name = "Circle"
    PARAMETERS = [{"name": "radio", "label": "Radius", "unit": "cm"}]
    DESCRIPTION = "Perfectly round 2D shape; every point on its edge is equally far from the center."
    FORMULA = "A = π·r²   |   P = 2·π·r"

    def __init__(self):
        self.radio = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.radio = float(input(f'enter the data:'))

    def calculate_area(self):
        self.area = math.pi * self.radio ** 2

    def calculate_perimeter(self):
        self.perimeter = 2 * self.radio * math.pi

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the circle is: {self.area:.2f}\nThe perimeter of the circle is: {self.perimeter:.2f}')


class Rectangle(Figures2D):
    name = "Rectangle"
    PARAMETERS = [
        {"name": "base", "label": "Base", "unit": "cm"},
        {"name": "height", "label": "Height", "unit": "cm"},
    ]
    DESCRIPTION = "Flat shape with four straight sides and four right angles."
    FORMULA = "A = b·h   |   P = 2·(b + h)"

    def __init__(self):
        self.base = None
        self.height = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.base = float(input(f'enter the data base:'))
        self.height = float(input(f'enter the data height:'))

    def calculate_area(self):
        self.area = self.base * self.height

    def calculate_perimeter(self):
        self.perimeter = 2 * (self.base + self.height)

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the rectangle is: {self.area:.2f}\nThe perimeter of the rectangle is: {self.perimeter:.2f}')


class Trapeze(Figures2D):
    name = "Trapeze"
    PARAMETERS = [
        {"name": "base", "label": "Base (major)", "unit": "cm"},
        {"name": "base_minior", "label": "Base (minor)", "unit": "cm"},
        {"name": "height", "label": "Height", "unit": "cm"},
        {"name": "lado1", "label": "Side 1", "unit": "cm"},
        {"name": "lado2", "label": "Side 2", "unit": "cm"},
    ]
    DESCRIPTION = "Four-sided shape with one pair of parallel sides (the bases)."
    FORMULA = "A = (B + b)·h / 2   |   P = B + b + l₁ + l₂"

    def __init__(self):
        self.base = None
        self.base_minior = None
        self.height = None
        self.lado1 = None
        self.lado2 = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.base = float(input(f'enter the data base: '))
        self.base_minior = float(input(f'enter the data base minior: '))
        self.height = float(input(f'enter the data height: '))
        self.lado1 = float(input(f'enter the data lado1: '))
        self.lado2 = float(input(f'enter the data lado2: '))

    def calculate_area(self):
        self.area = (self.base + self.base_minior) * self.height / 2

    def calculate_perimeter(self):
        self.perimeter = self.base + self.base_minior + self.lado1 + self.lado2

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the trapeze is: {self.area:.2f}\nThe perimeter of the trapeze is: {self.perimeter:.2f}')


class RegularPolygon(Figures2D):
    name = "Regular Polygon"
    PARAMETERS = [
        {"name": "sides", "label": "Number of sides (n)", "unit": ""},
        {"name": "side", "label": "Side length", "unit": "cm"},
    ]
    DESCRIPTION = "2D shape with n equal sides and n equal angles."
    FORMULA = "A = n·s² / (4·tan(π/n))   |   P = n·s"

    def __init__(self):
        self.sides = None
        self.side = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.sides = float(input('enter the number of sides (n): '))
        self.side = float(input('enter the side length: '))

    def calculate_area(self):
        self.area = (self.sides * self.side ** 2) / (4 * math.tan(math.pi / self.sides))

    def calculate_perimeter(self):
        self.perimeter = self.sides * self.side

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the regular polygon is: {self.area:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class CircularSector(Figures2D):
    name = "Circular Sector"
    PARAMETERS = [
        {"name": "radio", "label": "Radius", "unit": "cm"},
        {"name": "angle", "label": "Angle", "unit": "°"},
    ]
    DESCRIPTION = "Slice of a circle bounded by two radii and the arc between them."
    FORMULA = "A = (θ/360)·π·r²   |   Arc = (θ/360)·2·π·r"

    def __init__(self):
        self.radio = None
        self.angle = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.radio = float(input('enter the radius: '))
        self.angle = float(input('enter the angle in degrees: '))

    def calculate_area(self):
        self.area = (self.angle / 360) * math.pi * self.radio ** 2

    def calculate_perimeter(self):
        self.arc = (self.angle / 360) * 2 * math.pi * self.radio
        self.perimeter = self.arc + 2 * self.radio

    def _extra_results(self):
        return [("Arc Length", self.arc, "cm")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the circular sector is: {self.area:.2f}\nThe arc length is: {self.arc:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Annulus(Figures2D):
    name = "Annulus"
    PARAMETERS = [
        {"name": "radio", "label": "Outer radius (R)", "unit": "cm"},
        {"name": "radio_inner", "label": "Inner radius (r)", "unit": "cm"},
    ]
    DESCRIPTION = "Region between two concentric circles, like a ring."
    FORMULA = "A = π·(R² − r²)   |   P = 2·π·(R + r)"

    def __init__(self):
        self.radio = None
        self.radio_inner = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.radio = float(input('enter the outer radius: '))
        self.radio_inner = float(input('enter the inner radius: '))

    def calculate_area(self):
        self.area = math.pi * (self.radio ** 2 - self.radio_inner ** 2)

    def calculate_perimeter(self):
        self.perimeter = 2 * math.pi * (self.radio + self.radio_inner)

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the annulus is: {self.area:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Cube(Figures3D):
    name = "Cube"
    PARAMETERS = [{"name": "sides", "label": "Side", "unit": "cm"}]
    DESCRIPTION = "Solid with six identical square faces."
    FORMULA = "V = s³   |   A = 6·s²"

    def __init__(self):
        self.sides = None
        self.diagonal = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.sides = float(input(f'enter the data sides: '))

    def calculate_volume(self):
        self.volume = self.sides ** 3
        self.diagonal = self.sides * math.sqrt(3)

    def calculate_surface_area(self):
        self.surface_area = 6 * self.sides ** 2

    def _extra_results(self):
        return [("Diagonal", self.diagonal, "cm")]

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the Cube is: {self.volume:.2f}\nThe diagonal of the Cube is: {self.diagonal:.2f}\nThe surface area is: {self.surface_area:.2f}')


class Cylinder(Figures3D):
    name = "Cylinder"
    PARAMETERS = [
        {"name": "height", "label": "Height", "unit": "cm"},
        {"name": "radio", "label": "Radius", "unit": "cm"},
    ]
    DESCRIPTION = "Solid with two circular bases joined by a curved surface."
    FORMULA = "V = π·r²·h   |   A = 2·π·r·(r + h)"

    def __init__(self):
        self.height = None
        self.radio = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.height = float(input('Enter the data height: '))
        self.radio = float(input('Enter the data radius: '))

    def calculate_volume(self):
        self.volume = math.pi * self.radio ** 2 * self.height

    def calculate_surface_area(self):
        self.surface_area = 2 * math.pi * self.radio ** 2 + 2 * math.pi * self.radio * self.height

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the Cylinder is: {self.volume:.2f}\nThe surface area of the Cylinder is: {self.surface_area:.2f}')


class Sphere(Figures3D):
    name = "Sphere"
    PARAMETERS = [{"name": "radio", "label": "Radius", "unit": "cm"}]
    DESCRIPTION = "Perfectly round 3D shape; every point on its surface is equally far from the center."
    FORMULA = "V = (4/3)·π·r³   |   A = 4·π·r²"

    def __init__(self):
        self.radio = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.radio = float(input('Enter the data radius: '))

    def calculate_volume(self):
        self.volume = (4 / 3) * math.pi * self.radio ** 3

    def calculate_surface_area(self):
        self.surface_area = 4 * math.pi * self.radio ** 2

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the Sphere is: {self.volume:.2f}\nThe surface area of the Sphere is: {self.surface_area:.2f}')


class RectangularPyramid(Figures3D):
    name = "Rectangular Pyramid"
    PARAMETERS = [
        {"name": "base", "label": "Base length", "unit": "cm"},
        {"name": "width", "label": "Base width", "unit": "cm"},
        {"name": "height", "label": "Height", "unit": "cm"},
    ]
    DESCRIPTION = "Solid with a rectangular base and triangular faces meeting at an apex."
    FORMULA = "V = (1/3)·l·w·h   |   A = l·w + l·s₁ + w·s₂"

    def __init__(self):
        self.base = None
        self.width = None
        self.height = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.base = float(input('enter the base length: '))
        self.width = float(input('enter the base width: '))
        self.height = float(input('enter the height: '))

    def calculate_volume(self):
        self.volume = (1 / 3) * self.base * self.width * self.height

    def calculate_surface_area(self):
        slant_length = math.sqrt((self.width / 2) ** 2 + self.height ** 2)
        slant_width = math.sqrt((self.base / 2) ** 2 + self.height ** 2)
        self.surface_area = self.base * self.width + self.base * slant_length + self.width * slant_width

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the rectangular pyramid is: {self.volume:.2f}\nThe surface area is: {self.surface_area:.2f}')


class Cone(Figures3D):
    name = "Cone"
    PARAMETERS = [
        {"name": "radio", "label": "Radius", "unit": "cm"},
        {"name": "height", "label": "Height", "unit": "cm"},
    ]
    DESCRIPTION = "Solid with a circular base that tapers to a point."
    FORMULA = "V = (1/3)·π·r²·h   |   A = π·r·(r + s),  s = √(r² + h²)"

    def __init__(self):
        self.radio = None
        self.height = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.radio = float(input('enter the radius: '))
        self.height = float(input('enter the height: '))

    def calculate_volume(self):
        self.volume = (1 / 3) * math.pi * self.radio ** 2 * self.height

    def calculate_surface_area(self):
        self.slant = math.sqrt(self.radio ** 2 + self.height ** 2)
        self.surface_area = math.pi * self.radio * (self.radio + self.slant)

    def _extra_results(self):
        return [("Slant Height", self.slant, "cm")]

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the cone is: {self.volume:.2f}\nThe surface area is: {self.surface_area:.2f}')


class RectangularPrism(Figures3D):
    name = "Rectangular Prism"
    PARAMETERS = [
        {"name": "length", "label": "Length", "unit": "cm"},
        {"name": "width", "label": "Width", "unit": "cm"},
        {"name": "height", "label": "Height", "unit": "cm"},
    ]
    DESCRIPTION = "Solid with six rectangular faces, like a box."
    FORMULA = "V = l·w·h   |   A = 2·(l·w + l·h + w·h)"

    def __init__(self):
        self.length = None
        self.width = None
        self.height = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.length = float(input('enter the length: '))
        self.width = float(input('enter the width: '))
        self.height = float(input('enter the height: '))

    def calculate_volume(self):
        self.volume = self.length * self.width * self.height

    def calculate_surface_area(self):
        self.surface_area = 2 * (self.length * self.width + self.length * self.height + self.width * self.height)

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the rectangular prism is: {self.volume:.2f}\nThe surface area is: {self.surface_area:.2f}')


class Triangle(Figures2D):
    name = "Triangle"
    PARAMETERS = [
        {"name": "base", "label": "Base", "unit": "cm"},
        {"name": "height", "label": "Height", "unit": "cm"},
        {"name": "lado1", "label": "Side a", "unit": "cm"},
        {"name": "lado2", "label": "Side b", "unit": "cm"},
        {"name": "lado3", "label": "Side c", "unit": "cm"},
    ]
    DESCRIPTION = "Three-sided 2D shape; sides equal (equilateral), two equal (isosceles) or all different (scalene)."
    FORMULA = "A = b·h / 2   |   P = a + b + c"

    def __init__(self):
        self.base = None
        self.height = None
        self.lado1 = None
        self.lado2 = None
        self.lado3 = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.base = float(input('enter the base: '))
        self.height = float(input('enter the height: '))
        self.lado1 = float(input('enter side a: '))
        self.lado2 = float(input('enter side b: '))
        self.lado3 = float(input('enter side c: '))

    def calculate_area(self):
        self.area = self.base * self.height / 2

    def calculate_perimeter(self):
        self.perimeter = self.lado1 + self.lado2 + self.lado3

    def _triangle_type(self):
        a, b, c = self.lado1, self.lado2, self.lado3
        if a == b == c:
            return "Equilateral"
        if a == b or b == c or a == c:
            return "Isosceles"
        return "Scalene"

    def validate(self):
        sides = sorted([self.lado1, self.lado2, self.lado3])
        if sides[0] + sides[1] <= sides[2]:
            return "These side lengths do not form a valid triangle."
        return None

    def _extra_results(self):
        return [("Type", self._triangle_type(), "")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the triangle is: {self.area:.2f}\nThe perimeter is: {self.perimeter:.2f}\nType: {self._triangle_type()}')


class Ellipse(Figures2D):
    name = "Ellipse"
    PARAMETERS = [
        {"name": "semi_major", "label": "Semi-major axis (a)", "unit": "cm"},
        {"name": "semi_minor", "label": "Semi-minor axis (b)", "unit": "cm"},
    ]
    DESCRIPTION = "Oval 2D shape defined by two perpendicular axes."
    FORMULA = "A = π·a·b   |   P ≈ π(a+b)·(1 + 3h/(10+√(4−3h))), h = ((a−b)/(a+b))²"

    def __init__(self):
        self.semi_major = None
        self.semi_minor = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.semi_major = float(input('enter the semi-major axis: '))
        self.semi_minor = float(input('enter the semi-minor axis: '))

    def calculate_area(self):
        self.area = math.pi * self.semi_major * self.semi_minor

    def calculate_perimeter(self):
        h = ((self.semi_major - self.semi_minor) / (self.semi_major + self.semi_minor)) ** 2
        self.perimeter = math.pi * (self.semi_major + self.semi_minor) * (
            1 + (3 * h) / (10 + math.sqrt(4 - 3 * h))
        )

    def validate(self):
        if self.semi_major < self.semi_minor:
            return "Semi-major axis (a) must be greater than or equal to semi-minor axis (b)."
        return None

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the ellipse is: {self.area:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Rhombus(Figures2D):
    name = "Rhombus"
    PARAMETERS = [
        {"name": "diag_major", "label": "Major diagonal (D)", "unit": "cm"},
        {"name": "diag_minor", "label": "Minor diagonal (d)", "unit": "cm"},
    ]
    DESCRIPTION = "Four equal sides; diagonals cross at right angles."
    FORMULA = "A = D·d / 2   |   side = √((D/2)² + (d/2)²)   |   P = 4·side"

    def __init__(self):
        self.diag_major = None
        self.diag_minor = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.diag_major = float(input('enter the major diagonal: '))
        self.diag_minor = float(input('enter the minor diagonal: '))

    def calculate_area(self):
        self.area = self.diag_major * self.diag_minor / 2

    def calculate_perimeter(self):
        self.side = math.sqrt((self.diag_major / 2) ** 2 + (self.diag_minor / 2) ** 2)
        self.perimeter = 4 * self.side

    def _extra_results(self):
        return [("Side", self.side, "cm")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the rhombus is: {self.area:.2f}\nThe side is: {self.side:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Parallelogram(Figures2D):
    name = "Parallelogram"
    PARAMETERS = [
        {"name": "base", "label": "Base", "unit": "cm"},
        {"name": "height", "label": "Height", "unit": "cm"},
        {"name": "angle", "label": "Angle", "unit": "°"},
    ]
    DESCRIPTION = "Four-sided shape with two pairs of parallel sides."
    FORMULA = "A = b·h   |   P = 2·b + 2·h / sin(θ)"

    def __init__(self):
        self.base = None
        self.height = None
        self.angle = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.base = float(input('enter the base: '))
        self.height = float(input('enter the height: '))
        self.angle = float(input('enter the angle in degrees: '))

    def calculate_area(self):
        self.area = self.base * self.height

    def calculate_perimeter(self):
        self.side = self.height / math.sin(math.radians(self.angle))
        self.perimeter = 2 * self.base + 2 * self.side

    def validate(self):
        if self.angle >= 180:
            return "Angle must be between 0 and 180 degrees."
        return None

    def _extra_results(self):
        return [("Side", self.side, "cm")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the parallelogram is: {self.area:.2f}\nThe side is: {self.side:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Torus(Figures3D):
    name = "Torus"
    PARAMETERS = [
        {"name": "major_radius", "label": "Major radius (R)", "unit": "cm"},
        {"name": "minor_radius", "label": "Minor radius (r)", "unit": "cm"},
    ]
    DESCRIPTION = "3D ring shape (like a donut) made by rotating a circle around an axis."
    FORMULA = "V = 2·π²·R·r²   |   A = 4·π²·R·r"

    def __init__(self):
        self.major_radius = None
        self.minor_radius = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.major_radius = float(input('enter the major radius: '))
        self.minor_radius = float(input('enter the minor radius: '))

    def calculate_volume(self):
        self.volume = 2 * math.pi ** 2 * self.major_radius * self.minor_radius ** 2

    def calculate_surface_area(self):
        self.surface_area = 4 * math.pi ** 2 * self.major_radius * self.minor_radius

    def validate(self):
        if self.major_radius <= self.minor_radius:
            return "Major radius (R) must be greater than minor radius (r)."
        return None

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the torus is: {self.volume:.2f}\nThe surface area is: {self.surface_area:.2f}')


class Tetrahedron(Figures3D):
    name = "Tetrahedron"
    PARAMETERS = [{"name": "side", "label": "Side", "unit": "cm"}]
    DESCRIPTION = "Solid with four triangular faces, like a triangular pyramid."
    FORMULA = "V = a³ / (6·√2)   |   A = √3·a²"

    def __init__(self):
        self.side = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.side = float(input('enter the side: '))

    def calculate_volume(self):
        self.volume = self.side ** 3 / (6 * math.sqrt(2))

    def calculate_surface_area(self):
        self.surface_area = math.sqrt(3) * self.side ** 2

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the tetrahedron is: {self.volume:.2f}\nThe surface area is: {self.surface_area:.2f}')
