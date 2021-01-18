import ElevatorGameFinal as game
import pygame, time, random

game.init(13,60,800,chance=20)
game.setup()
building = game.All((4,4,4,4,4,4,4,4,4,4))

elevators = building.elevators

elevatorDirections = ["up",]*len(elevators)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    building.draw()
    building.update()

    ########code for the elevators goes here
    for elevatorNum in range(len(elevators)):
        elevator = elevators[elevatorNum]
        if elevator.idle:
            if elevator.direction == "up":
                if not elevator.full():
                    floors = building.getFloorsUp()
                else:
                    floors = []
                destinations = []
                for i in floors:
                    if i > elevator.floor:
                        destinations.append(i)
                for person in elevator.people:
                    if person != 0:
                        if person.destination > elevator.floor:
                            destinations.append(person.destination)
                if len(destinations) > 0:
                    floor = min(destinations)
                    elevator.goto(floor)
                else:
                    if not elevator.full():
                        floors = building.getFloorsDown()
                        destinations = []
                        for i in floors:
                            if i > elevator.floor:
                                destinations.append(i)
                        if len(destinations) > 0:
                            elevator.goto(max(destinations))
                        else:
                            elevator.direction = "down"
                    else:
                        elevator.direction = "down"

            #going down (same as up but in reverse)
            else:
                if not elevator.full():
                    floors = building.getFloorsDown()
                else:
                    floors = []
                destinations = []
                for i in floors:
                    if i < elevator.floor:
                        destinations.append(i)
                for person in elevator.people:
                    if person != 0:
                        if person.destination < elevator.floor:
                            destinations.append(person.destination)
                if len(destinations) > 0:
                    floor = max(destinations)
                    elevator.goto(floor)
                else:
                    if not elevator.full():
                        floors = building.getFloorsUp()
                        destinations = []
                        for i in floors:
                            if i < elevator.floor:
                                destinations.append(i)
                        if len(destinations) > 0:
                            elevator.goto(min(destinations))
                        else:
                            elevator.direction = "up"
                    else:
                        elevator.direction = "up"

        #if moving
        else:
            if not elevator.full():
                if elevator.direction == "up":
                    floors = building.getFloorsUp()
                    destinations = []
                    for floor in floors:
                        if floor > elevator.floor and floor < elevator.destination:
                            destinations.append(floor)
                    if len(destinations) > 0:
                        elevator.goto(min(destinations))
                else:
                    floors = building.getFloorsDown()
                    destinations = []
                    for floor in floors:
                        if floor <= elevator.floor and floor > elevator.destination:
                            destinations.append(floor)
                    if len(destinations) > 0:
                        elevator.goto(max(destinations))
                    
            
        
    ########code for the elevators ends here
    time.sleep(0.000)
pygame.quit()





#elevators[elevatorNum].floor --> returns the current floor (once on or above it)
#elevators[elevatorNum].goto(floorNum) --> moves the elevator to floor floorNum. floorNum is an integer. usually you only call function when .idle == True
#elevators[elevatorNum].idle --> returns a bool stating if the elevator has stopped.
#building.getFloorsPressed() --> returns a list of every floor where a person is waiting
#building.getFloorsPressedBool() --> returns a list of whether or not a floor has people waiting (a list of bools)
#building.getButtonsPressed() --> returns the state of each button on each floor in the form  [{"up":False,"down":False},...]
#elevators[elevatorNum].people[personNum].destination --> returns the destination floor of each person in the elevator.
#game.world.floors --> returns the number of floors there are




