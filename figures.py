from abc import ABC, abstractmethod
import math
class Figure(ABC):
    @abstractmethod
    def get_name(self):
        pass
    @abstractmethod
    def enter_data(self):
        pass
    @abstractmethod
    def show_result(self):
        pass

class Figures2D(Figure):
    @abstractmethod
    def calculate_area(self):
        pass
    @abstractmethod
    def calculate_perimeter(self):
        pass

class Figures3D(Figure):
    @abstractmethod
    def calculate_volume(self):
        pass
    @abstractmethod
    def calculate_surface_area(self):
        pass

class Circle(Figures2D):
    def __init__(self):
        self.name = 'Circle'
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
        print(f'The area of ​​the circle is:{self.area:.2f}\nThe perimeter of the circle is:{self.perimeter:.2f}')
        
class Rectangle(Figures2D):
    def __init__(self):
        self.name = 'Rectangle'
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
        print(f'The area of the rectangles is: {self.area:.2f}\nThe perimeter of the rectangles is:{self.perimeter:.2f}')

class Trapeze(Figures2D):
    def __init__(self):
        self.name = 'Trapeze'
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
        print(f'The area of the trapeze is: {self.area:.2f}\nThe perimeter of the trapeze is:{self.perimeter:.2f}')
class Cube(Figures3D):
    def __init__(self):
        self.name = 'Cube'
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

    def show_result(self):
        print(f'The volume of the Cube is: {self.volume:.2f}\nThe diagonal of the Cube is: {self.diagonal:.2f}\nThe surface area is: {self.surface_area:.2f}')

class Cylinder(Figures3D):
    def __init__(self):
        self.name = 'Cylinder'
        self.height = None
        self.radio = None

    def get_name(self):
        print(self.name)

    def enter_data(self):
        self.height = float(input('Enter de data heigth: '))
        self.radio = float(input('Enter de data radio: '))

    def calculate_volume(self):
        self.volume = math.pi  * self.radio ** 2 * self.height

    def calculate_surface_area(self):
        self.superface_area = 2 * math.pi * self.radio ** 2 + 2 * math.pi * self.radio * self.height

    def show_result(self):
        print(f'The volume of Cylinder is: {self.volume:.2f}\nThe superface area of Cylinder is: {self.superface_area:.2f}')
class Sphere(Figures3D):
    def get_name(self):
        pass
    def enter_data(self):
        pass
    def show_result(self):
        pass
    def calculate_volume(self):
        pass
    def calculate_surface_area(self):
        pass