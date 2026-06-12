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

class Cylinder(Figures3D):
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