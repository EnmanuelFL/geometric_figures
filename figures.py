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
            ("Área", self.area, "cm²"),
            ("Perímetro", self.perimeter, "cm"),
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
            ("Volumen", self.volume, "cm³"),
            ("Área superficial", self.surface_area, "cm²"),
        ]
        results.extend(self._extra_results())
        return results

    def _extra_results(self):
        return []


class Circle(Figures2D):
    name = "Círculo"
    PARAMETERS = [{"name": "radio", "label": "Radio", "unit": "cm"}]
    DESCRIPTION = "Figura 2D perfectamente redonda; todos los puntos de su borde equidistan del centro."
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
    name = "Rectángulo"
    PARAMETERS = [
        {"name": "base", "label": "Base", "unit": "cm"},
        {"name": "height", "label": "Altura", "unit": "cm"},
    ]
    DESCRIPTION = "Figura plana con cuatro lados rectos y cuatro ángulos rectos."
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
    name = "Trapecio"
    PARAMETERS = [
        {"name": "base", "label": "Base mayor (B)", "unit": "cm"},
        {"name": "base_minior", "label": "Base menor (b)", "unit": "cm"},
        {"name": "height", "label": "Altura", "unit": "cm"},
        {"name": "lado1", "label": "Lado 1", "unit": "cm"},
        {"name": "lado2", "label": "Lado 2", "unit": "cm"},
    ]
    DESCRIPTION = "Figura de cuatro lados con un par de lados paralelos (las bases)."
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
    name = "Polígono regular"
    PARAMETERS = [
        {"name": "sides", "label": "Número de lados (n)", "unit": ""},
        {"name": "side", "label": "Longitud del lado", "unit": "cm"},
    ]
    DESCRIPTION = "Figura 2D con n lados iguales y n ángulos iguales."
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
    name = "Sector circular"
    PARAMETERS = [
        {"name": "radio", "label": "Radio", "unit": "cm"},
        {"name": "angle", "label": "Ángulo", "unit": "°"},
    ]
    DESCRIPTION = "Porción de un círculo delimitada por dos radios y el arco entre ellos."
    FORMULA = "A = (θ/360)·π·r²   |   Arco = (θ/360)·2·π·r"

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
        return [("Longitud de arco", self.arc, "cm")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the circular sector is: {self.area:.2f}\nThe arc length is: {self.arc:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Annulus(Figures2D):
    name = "Anillo"
    PARAMETERS = [
        {"name": "radio", "label": "Radio exterior (R)", "unit": "cm"},
        {"name": "radio_inner", "label": "Radio interior (r)", "unit": "cm"},
    ]
    DESCRIPTION = "Región entre dos círculos concéntricos, como un anillo."
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

    def validate(self):
        if self.radio_inner >= self.radio:
            return "El radio interior debe ser menor que el radio exterior."
        return None

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the annulus is: {self.area:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Cube(Figures3D):
    name = "Cubo"
    PARAMETERS = [{"name": "sides", "label": "Lado", "unit": "cm"}]
    DESCRIPTION = "Sólido con seis caras cuadradas idénticas."
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
        print(f'El volumen del cubo es: {self.volume:.2f}\nLa diagonal del cubo es: {self.diagonal:.2f}\nEl área superficial es: {self.surface_area:.2f}')


class Cylinder(Figures3D):
    name = "Cilindro"
    PARAMETERS = [
        {"name": "height", "label": "Altura", "unit": "cm"},
        {"name": "radio", "label": "Radio", "unit": "cm"},
    ]
    DESCRIPTION = "Sólido con dos bases circulares unidas por una superficie curva."
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
    name = "Esfera"
    PARAMETERS = [{"name": "radio", "label": "Radio", "unit": "cm"}]
    DESCRIPTION = "Figura 3D perfectamente redonda; todos los puntos de su superficie equidistan del centro."
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
    name = "Pirámide rectangular"
    PARAMETERS = [
        {"name": "base", "label": "Largo de la base", "unit": "cm"},
        {"name": "width", "label": "Ancho de la base", "unit": "cm"},
        {"name": "height", "label": "Altura", "unit": "cm"},
    ]
    DESCRIPTION = "Sólido con base rectangular y caras triangulares que se unen en un vértice."
    FORMULA = "V = (1/3)·l·a·h   |   A = l·a + l·s₁ + a·s₂"

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
    name = "Cono"
    PARAMETERS = [
        {"name": "radio", "label": "Radio", "unit": "cm"},
        {"name": "height", "label": "Altura", "unit": "cm"},
    ]
    DESCRIPTION = "Sólido con base circular que se estrecha hasta un punto."
    FORMULA = "V = (1/3)·π·r²·h   |   A = π·r·(r + g),  g = √(r² + h²)"

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
        return [("Generatriz", self.slant, "cm")]

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the cone is: {self.volume:.2f}\nThe surface area is: {self.surface_area:.2f}')


class RectangularPrism(Figures3D):
    name = "Prisma rectangular"
    PARAMETERS = [
        {"name": "length", "label": "Largo", "unit": "cm"},
        {"name": "width", "label": "Ancho", "unit": "cm"},
        {"name": "height", "label": "Altura", "unit": "cm"},
    ]
    DESCRIPTION = "Sólido con seis caras rectangulares, como una caja."
    FORMULA = "V = l·a·h   |   A = 2·(l·a + l·h + a·h)"

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
    name = "Triángulo"
    PARAMETERS = [
        {"name": "base", "label": "Base", "unit": "cm"},
        {"name": "height", "label": "Altura", "unit": "cm"},
        {"name": "lado1", "label": "Lado a", "unit": "cm"},
        {"name": "lado2", "label": "Lado b", "unit": "cm"},
        {"name": "lado3", "label": "Lado c", "unit": "cm"},
    ]
    DESCRIPTION = "Figura 2D de tres lados; lados iguales (equilátero), dos iguales (isósceles) o todos distintos (escaleno)."
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
            return "Equilátero"
        if a == b or b == c or a == c:
            return "Isósceles"
        return "Escaleno"

    def validate(self):
        sides = sorted([self.lado1, self.lado2, self.lado3])
        if sides[0] + sides[1] <= sides[2]:
            return "Estas longitudes de lado no forman un triángulo válido."
        return None

    def _extra_results(self):
        return [("Tipo", self._triangle_type(), "")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the triangle is: {self.area:.2f}\nThe perimeter is: {self.perimeter:.2f}\nType: {self._triangle_type()}')


class Ellipse(Figures2D):
    name = "Elipse"
    PARAMETERS = [
        {"name": "semi_major", "label": "Semieje mayor (a)", "unit": "cm"},
        {"name": "semi_minor", "label": "Semieje menor (b)", "unit": "cm"},
    ]
    DESCRIPTION = "Figura 2D ovalada definida por dos ejes perpendiculares."
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
            return "El semieje mayor (a) debe ser mayor o igual que el semieje menor (b)."
        return None

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the ellipse is: {self.area:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Rhombus(Figures2D):
    name = "Rombo"
    PARAMETERS = [
        {"name": "diag_major", "label": "Diagonal mayor (D)", "unit": "cm"},
        {"name": "diag_minor", "label": "Diagonal menor (d)", "unit": "cm"},
    ]
    DESCRIPTION = "Cuatro lados iguales; las diagonales se cruzan en ángulo recto."
    FORMULA = "A = D·d / 2   |   lado = √((D/2)² + (d/2)²)   |   P = 4·lado"

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
        return [("Lado", self.side, "cm")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the rhombus is: {self.area:.2f}\nThe side is: {self.side:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Parallelogram(Figures2D):
    name = "Paralelogramo"
    PARAMETERS = [
        {"name": "base", "label": "Base", "unit": "cm"},
        {"name": "height", "label": "Altura", "unit": "cm"},
        {"name": "angle", "label": "Ángulo", "unit": "°"},
    ]
    DESCRIPTION = "Figura de cuatro lados con dos pares de lados paralelos."
    FORMULA = "A = b·h   |   P = 2·b + 2·h / sen(θ)"

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
            return "El ángulo debe estar entre 0 y 180 grados."
        return None

    def _extra_results(self):
        return [("Lado", self.side, "cm")]

    def show_result(self):
        self.calculate_area()
        self.calculate_perimeter()
        print(f'The area of the parallelogram is: {self.area:.2f}\nThe side is: {self.side:.2f}\nThe perimeter is: {self.perimeter:.2f}')


class Torus(Figures3D):
    name = "Toro"
    PARAMETERS = [
        {"name": "major_radius", "label": "Radio mayor (R)", "unit": "cm"},
        {"name": "minor_radius", "label": "Radio menor (r)", "unit": "cm"},
    ]
    DESCRIPTION = "Figura 3D con forma de anillo (como una rosquilla) generada al girar un círculo alrededor de un eje."
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
            return "El radio mayor (R) debe ser mayor que el radio menor (r)."
        return None

    def show_result(self):
        self.calculate_volume()
        self.calculate_surface_area()
        print(f'The volume of the torus is: {self.volume:.2f}\nThe surface area is: {self.surface_area:.2f}')


class Tetrahedron(Figures3D):
    name = "Tetraedro"
    PARAMETERS = [{"name": "side", "label": "Lado", "unit": "cm"}]
    DESCRIPTION = "Sólido con cuatro caras triangulares, como una pirámide triangular."
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
