#main.py
import sys
import pygame

pygame.init();

colours:dict = {
        "RED": (255,0,0),
        "GREEN": (0,255,0),
        "BLUE": (0,0,255)
};

class Vector2:
    def __init__(self, x:float, y:float) -> None:
        self.x=x;
        self.y=y;
    
    def __str__(self) -> str:
        return str(f"{self.x}, {self.y}");
    def tuple(self) -> tuple[float]:
        return (self.x, self.y)

    def __add__(self, other) -> 'Vector2':
        if (isinstance(other, Vector2)):
            return Vector2(other.x+self.x, other.y+self.y);
        return NotImplemented;
    def __mul__(self, other) -> 'Vector2':
        if (isinstance(other, Vector2)):
            return Vector2(other.x*self.x, other.y*self.y);
        return NotImplemented;


class InputHandler:
    def __init__(self) -> None:
        self.keysdown=None;
    def __del__(self) -> None:
        pass;

    def GetKey(self, key:any, events:list) -> bool:
        """
        Gets key **Click** not hold,\n 
        use self.keysdown[] to access keys held.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
        return False;

    def update(self):
        self.keysdown = pygame.key.get_pressed();

def pixelToScreenSize(window:"MakeScreen", sizePixels:tuple[float,float], asVector:bool=False) -> tuple:
    midpointOfWindowSize:float=(window.windowSize[0]+ window.windowSize[1])/2;
    if not asVector: return ((sizePixels[0]/window.screenSize)*midpointOfWindowSize, (sizePixels[1]/window.screenSize)*midpointOfWindowSize);
    else: return Vector2((sizePixels[0]/window.screenSize)*midpointOfWindowSize, (sizePixels[1]/window.screenSize)*midpointOfWindowSize);

class MakeObject:
    def __init__(
        self, 
        screen, 
        startPos:Vector2=Vector2(0,0), 
        sourceImage:str=None, 
        canCollide:bool=False, 
        size:tuple=(20,20), 
        colour=(0,0,100),
        screenObject=None
    ) -> None:
        self.controler:"CharartorController"=None

        self.screen=screen;
        self.screenObject:"MakeScreen"=screenObject;
        self.pos:Vector2=startPos;
        del startPos;
        self.canCollide=canCollide;
        self.size=size;

        if (not sourceImage):
            del sourceImage;
            pygame.draw.circle(screen, colour, startPos, size[0]);
            self.colour=colour;
        
        if (sourceImage!=None):
            self.frame=pygame.image.load(f"{sourceImage}").convert_alpha();
            del sourceImage;
            self.frame=pygame.transform.scale(self.frame, pixelToScreenSize(self.screenObject, self.size));
            self.rectFrame = self.frame.get_rect();
    
    def update(self) -> None:
        if (not self.frame):
            pygame.draw.circle(self.screen, self.colour, self.pos, self.size);
        else:
            self.screen.blit(self.frame, Vector2.tuple(self.pos));
    
    def move(self, newPos:Vector2) -> dict[Vector2]:
        oldX:float=self.pos.X;
        oldY:float=self.pos.Y;

        xyNew:tuple[float,float] = (pixelToScreenSize(self.screenObject, (newPos.x,newPos.y)));
        self.pos=Vector2(xyNew[0], xyNew[1]);
        return {"newPos":Vector2(xyNew[0],xyNew[1]), "oldPos":Vector2(oldX,oldY)};

    def __del__(self):
        if (self.frame):
            del self.frame;


class CharartorController:
    def __init__(self, charator:MakeObject) -> None:
        self.charator:MakeObject=charator;

    def movePlayer(self, newPos:Vector2)->tuple[Vector2]:
        """
        Moves player.\n
        returns tuple 0=originalpos, 1=newpos(current)
        """
        oldPos=self.charator.pos;
        self.charator.pos=newPos;
        return (oldPos, newPos);


class MakeScreen:
    fullScreenResultion:tuple[int]=(pygame.display.Info().current_w, pygame.display.Info().current_h);

    def __init__(self, widthHeight:tuple[int], screenSize:int) -> None:
        self.windowSize:tuple[int]=widthHeight;
        self.screenSize=screenSize
        self.window=pygame.display.set_mode(widthHeight);

    def update(self, screencolour):
        pygame.display.flip();
        self.window.fill(screencolour);


def main(argc:int, argv:list[str]) -> int:
    global colours;
    running:bool = True;

    screen=MakeScreen(MakeScreen.fullScreenResultion, 1000);
    #screen=MakeScreen((500,500), 1000);
    player=MakeObject(screen.window, startPos=(50,50), size=(50,50), colour=colours["RED"], sourceImage="sprites/sprite.png", screenObject=screen);
    player.controler=CharartorController(charator=player);
    playerInput=InputHandler();
    player.controler.movePlayer(Vector2(200,200));

    #main loop
    while (running):
        # events and input first
        playerInput.update();
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running=False;
                break;
        
        #logic
        if (playerInput.keysdown[pygame.K_UP]):
            print("Up arrow key is being held down");
        if (playerInput.GetKey(pygame.K_ESCAPE, events)):
            print("Esc clicked");

        # render last
        player.update();
        screen.update(colours["GREEN"]);
    
    return 0;

if (__name__=="__main__"): 
    exitCode:int = main(len(sys.argv), sys.argv);
    pygame.quit();
    sys.exit(exitCode);