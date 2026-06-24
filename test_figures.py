from figures import *
FIGURES = [Circle,Rectangle, Trapeze, Cube, Cylinder, Sphere]
while True:
    for indices, figura in enumerate(FIGURES):
        print(f"{indices + 1}. {figura.__name__}")
    print("0. Exit")
    question_guest = int(input("What do you want to choose: "))
    if question_guest == 0:
        break
    figures = FIGURES[question_guest -1 ]()
    figures.enter_data()
    figures.show_result()