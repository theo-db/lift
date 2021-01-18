import pygame, time, random, numpy

def init(floors,heightOfFloor,screenWidth,chance=50):
    global numberOfFloors, floorHeight, width, height, screen, prob
    pygame.init()
    numberOfFloors = floors
    floorHeight = heightOfFloor
    width = screenWidth
    height = numberOfFloors * floorHeight
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Lift game")
    prob = chance

class World:
    def __init__(self,floors,floorHeight,laneWidth):
        self.floors = floors
        self.floorHeight = floorHeight
        self.maxHeight = (floors-1)*floorHeight
        self.laneWidth = 70
        self.colour = (0,0,0)
        self.personWidth = 15
        self.font = pygame.font.SysFont("gillsansultra", 30)
        #self.image = pygame.transform.scale(pygame.image.load("person2.png"),(4,7))

    def draw(self):
        floorCount = world.floors-1
        for y in range(self.floorHeight, self.floors * self.floorHeight, self.floorHeight):
            pygame.draw.line(screen,self.colour,(0,y),(width,y))
            label = self.font.render(str(floorCount), 1,(37,48,32))
            screen.blit(label,(10,y - world.floorHeight))
            floorCount -= 1
        label = self.font.render(str(floorCount), 1,(37,48,32))
        screen.blit(label,(10,height - world.floorHeight))
            
world = 0 
def setup():
    global world
    world = World(numberOfFloors,floorHeight,70)


class Elevator:
    def __init__(self, capacity, xPosition):
        self.floor = 0
        self.capacity = capacity
        self.height = self.floor * world.floorHeight
        self.floor = 0
        self.onFloor = True
        self.direction = "up"
        self.moving = False
        self.floorsPressed = [False,]*world.floors
        self.people = []
        self.destination = 0
        self.wait = 0
        self.speed = 1
        self.timeStopped = 50
        self.colour = (37,48,32)
        self.xpos = xPosition
        self.prepareToMove = False
        self.width = capacity * world.personWidth
        self.peopleEntering = 0
        self.font = pygame.font.SysFont("arialblack",8)
        self.idle = False

    def update(self):
        if self.prepareToMove and self.wait == 0 and self.peopleEntering == 0:
            self.moving = True
            self.prepareToMove = False
        
        if self.wait == 0 and self.moving and self.destination != self.floor:
            if self.direction == "up":
                self.height = min(world.maxHeight, self.height + self.speed)
            elif self.direction == "down":
                self.height = max(0, self.height - self.speed)

            if self.height % world.floorHeight == 0:
                self.floor = int(self.height/world.floorHeight)

            if self.floor == self.destination:
                self.moving = False
                self.wait = self.timeStopped


        if self.wait > 0:
            self.wait -= 1

        if not self.moving and self.peopleEntering == 0 and self.wait == 0:
            self.idle = True
        else:
            self.idle = False

    def draw(self):
        pygame.draw.rect(screen,self.colour,(self.xpos, height - self.height, self.width, -world.floorHeight+1))

        #draw numbers
        xpos = self.xpos*1
        ypos = height - self.height - world.floorHeight
        for floor in range(world.floors):
            if self.floorsPressed[floor]:
                colour = (0,255,0)
            else:
                colour = (90,90,90)
            
            label = self.font.render(str(floor),1,colour)
            screen.blit(label,(xpos, ypos))
            if floor < 10:
                xpos += 12
            else:
                xpos += 18
            if xpos > self.width + self.xpos - 20:
                xpos = self.xpos*1
                ypos += 10


    def goto(self, floorNum):
        '''only to be called when not moving'''
        self.prepareToMove = True
        if floorNum > self.floor:
            self.direction = "up"
            self.destination = floorNum
        elif floorNum < self.floor:
            self.direction = "down"
            self.destination = floorNum
        else:
            self.prepareToMove = False

    def full(self):
        space = 0
        for person in self.people:
            if person == 0:
                space += 1
        if space == 0:
            return True
        else:
            return False



class Person:
    def __init__(self,floor,destination):
        self.floor = floor
        self.destination = destination
        self.elevator = None
        if self.floor > self.destination:
            self.button = "down"
        else:
            self.button = "up"
        self.y = height - (self.floor * world.floorHeight) + 10
        self.x = random.randint(5,world.laneWidth-5)
        self.waiting = True
        self.entering = False
        self.travelling = False
        self.leaving = False

    def draw(self):
        pygame.draw.rect(screen,(0,0,0),(self.x-2,self.y-12,4,-7))
        #screen.blit(world.image,(self.x-2,self.y-12))


class All:
    def __init__(self,elevators):
        self.elevators = []
        self.elevatorSlots = []
        personCount = 0
        for elevator in elevators:
            self.elevators.append(Elevator(elevator,personCount*world.personWidth + 100))
            self.elevatorSlots.append([0,]*elevator)
            personCount += elevator
        self.people = []
        self.font = pygame.font.SysFont("arialblack",8)
        self.transported = 0
        self.directionButtons = []
        self.count = 0

    def draw(self):
        screen.fill((255,255,255))
        world.draw()

        #draw up/down buttons
        self.directionButtons = []
        for i in range(world.floors):
            self.directionButtons.append({"up":False,"down":False})
            
        for person in self.people:
            if person.waiting:
                self.directionButtons[person.floor][person.button] = True

        for floor in range(world.floors):
            if self.directionButtons[floor]["up"]: colourUp = (0,255,0)
            else: colourUp = (90,90,90)

            if self.directionButtons[floor]["down"]: colourDown = (0,255,0)
            else: colourDown = (90,90,90)
            
            labelUp = self.font.render("up",1,colourUp)
            labelDown = self.font.render("down",1,colourDown)
            screen.blit(labelUp,(70,height - world.floorHeight*floor - world.floorHeight + 10))
            screen.blit(labelDown,(70,height - world.floorHeight*floor - world.floorHeight + 20))

        label = self.font.render(str(self.transported),1,(0,0,0))
        screen.blit(label,(width - 100,10))
                
        #draw elevators and people
        for elevator in self.elevators:
            elevator.draw()
        for person in self.people:
            person.draw()

        pygame.display.flip()

    def update(self):
        #randomly add people to each floor
        if random.randint(0,prob) == 0:
            floor = random.randrange(0,world.floors)
            destinations = list(range(world.floors))
            del destinations[floor]
            destination = random.choice(destinations)
            self.people.append(Person(floor,destination))

        for elevatorNum in range(len(self.elevators)):
            elevator = self.elevators[elevatorNum]
            elevator.update()

            #unload and take on more people if stopped
            if not elevator.moving:
                for person in self.people:
                    if person.waiting and person.floor == elevator.floor and 0 in self.elevatorSlots[elevatorNum]:
                        self.elevatorSlots[elevatorNum][self.elevatorSlots[elevatorNum].index(0)] = person
                        person.waiting = False
                        person.entering = True
                        person.elevator = elevatorNum
                        elevator.peopleEntering += 1

                    if person.travelling and elevator.floor == person.destination and not elevator.moving and person.elevator == elevatorNum:
                        self.elevatorSlots[elevatorNum][self.elevatorSlots[elevatorNum].index(person)] = 0
                        person.travelling = False
                        person.leaving = True

            else:
                #if the elevator is moving, set each person's y value to match the elevator's
                for person in self.elevatorSlots[elevatorNum]:
                    if person != 0:
                        person.y = height - elevator.height + 10

        #make a list of the index of each person to delete
        peopleToDelete = []                    
        for person in self.people:
            if person.entering:
                xposSlot = self.elevators[person.elevator].xpos + self.elevatorSlots[person.elevator].index(person) * world.personWidth + world.personWidth/2
                person.x += xposSlot/100
                if person.x > xposSlot:
                    person.x = xposSlot
                    person.entering = False
                    person.travelling = True
                    self.elevators[person.elevator].peopleEntering -= 1
            if person.leaving:
                person.x += 1
                if person.x > width:
                    person.leaving = False
                    peopleToDelete.append(self.people.index(person))
                    self.transported += 1

        #delete each person who has exited the screen
        peopleToDelete = numpy.array(peopleToDelete)
        for i in peopleToDelete:
            del self.people[i]
            peopleToDelete -= 1

        #feed data about the people in each elevator to the Elevator object
        for elevatorNum in range(len(self.elevatorSlots)):
            self.elevators[elevatorNum].people = self.elevatorSlots[elevatorNum]
            self.elevators[elevatorNum].floorsPressed = [False,]*world.floors
            for person in self.elevators[elevatorNum].people:
                if person != 0:
                    if person.travelling:
                        self.elevators[elevatorNum].floorsPressed[person.destination] = True

        self.count+=1
        if self.count == 10000:
            print(self.transported)

    def getFloorsPressed(self):
        pressed = []
        for floor in range(world.floors):
            if self.directionButtons[floor]["up"] or self.directionButtons[floor]["down"]:
                pressed.append(floor)
        return pressed

    def getFloorsPressedBool(self):
        pressed = [False,]*world.floors
        for floor in range(world.floors):
            pressed[floor] = self.directionButtons[floor]["up"] or self.directionButtons[floor]["down"]
        return pressed

    def getButtonsPressed(self):
        return self.directionButtons

    def getFloorsUp(self):
        pressed = []
        for floorNum in range(len(self.directionButtons)):
            if self.directionButtons[floorNum]["up"]:
                pressed.append(floorNum)
        return pressed

    def getFloorsDown(self):
        pressed = []
        for floorNum in range(len(self.directionButtons)):
            if self.directionButtons[floorNum]["down"]:
                pressed.append(floorNum)
        return pressed
            

if __name__ == "__main__":
    init(14,60,500)
    setup()
    building = All((5,10,7))
    count = 1
    d = 1

    class count:
        def __init__(self,e):
            self.e = e
            self.c = random.randrange(0,world.floors)
            self.d = random.choice((1,-1))
        def move(self):
            if building.elevators[self.e].idle:
                building.elevators[self.e].goto(self.c)
                self.c += self.d
                if self.c == world.floors:
                    self.d = -1
                    self.c = world.floors-1
                if self.c == -1:
                    self.d = 1
                    self.c = 0
            

    e1 = count(0)
    e2 = count(1)
    e3 = count(2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        building.draw()
        building.update()
        e1.move()
        e2.move()
        e3.move()
        time.sleep(0.005)
    
                    
                            

    










