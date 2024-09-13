import pygame
import dumalien
import random

# import the pygame module, so you can use it
import pygame
 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    reddot = pygame.image.load("reddot.png")
    pygame.display.set_icon(reddot)
    pygame.display.set_caption("some dum aliens")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((240,180))

    reddot2 = pygame.image.load("reddot2.png")


    #load some dum aliens
    #dumalienimg=pygame.image.load("dumalien.png")
     
    # define a variable to control the main loop
    running = True

    #gravity
    gravity=.2


    dumalienarr=[]

    #dumalien=myObj.MyObject(dumalienimg,(32,32),(0,0),4,12)
    mydumalien=dumalien.Dumalien((random.random()*(240-32),random.random()*(180-32)),12)
    dumalienarr.append(mydumalien)

    #start obj
    #dumalien.playing=1

    # init time
    t=pygame.time.get_ticks()
    last_flip=0

    #movement framerate
    period=50

    #start at one each to avoid div by 0
    missed=1
    hit=1
    perc=.5

    score=0

    #level
    level=1
    level_dt=0
    time_per_level=10000 #ms

    #game over
    go=False

    #screen states
    dedscreen=False
    scorescreen=False

    #keypress vars
    myChar=''
    keypress_handled=True
    max_chars=3
    highScorePerson=""
    blinker=['_',' ']
    blinker_idx=0
    blink_dt=0
    blink_time=200
    hs_written=False
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type==pygame.KEYUP and scorescreen:
                myChar=''
                if event.key<=90 and event.key>=65:
                    myChar=chr(event.key+32).upper()
                elif event.key>=92 and event.key<=122:
                    myChar=chr(event.key).upper()
                keypress_handled=False
            if event.type==pygame.MOUSEBUTTONUP and go and dedscreen:
                dedscreen=False
            if event.type==pygame.MOUSEBUTTONUP and go!=True:
                mousePos=pygame.mouse.get_pos()
                for mydumalien in dumalienarr:
                    if mousePos[0]>mydumalien.x and mousePos[0]<(mydumalien.x+32) and mousePos[1]>mydumalien.y and mousePos[1]<(mydumalien.y+32):
                        mydumalien.currentAction=mydumalien.actions["EXPLODING"]
                        #mydumalien.x=int((random.random()*(240-32)))
                        #mydumalien.y=int((random.random()*(180-32)))
                        hit+=1
                        perc+=.06
                        if perc>1:
                            perc=1
                        score+=level*100+int((hit/(hit+missed))*100)
                        newAlien=dumalien.Dumalien((random.random()*(240-32),random.random()*(180-32)),12)
                        dumalienarr.append(newAlien)
                        break
                    
        
        if go!=True:
            pt=t
            t=pygame.time.get_ticks()
            dt=t-pt

            level_dt+=dt
            if level_dt>=time_per_level: 
                newAlien=dumalien.Dumalien((random.random()*(240-32),random.random()*(180-32)),12)
                dumalienarr.append(newAlien)
                level_dt=0
                level+=1


            if t-last_flip>period:
                for mydumalien in dumalienarr.copy():
                    mydumalien.vy+=gravity
                    mydumalien.y=mydumalien.y+mydumalien.vy
                    if mydumalien.y>180:
                        missed+=1
                        perc-=.1
                        dumalienarr.remove(mydumalien)
                last_flip=t

            
            screen.fill((0,50,50))
            for mydumalien in dumalienarr.copy(): 
                if mydumalien.currentAction.done != True:
                    mydumalien.update(dt,t)
                    screen.blit(mydumalien.image,(mydumalien.x,mydumalien.y),mydumalien.source_rect)
                else:
                    dumalienarr.remove(mydumalien)
            
            #health bar
            if len(dumalienarr)<level:
                #game over
                if perc>0:
                    newAlien=dumalien.Dumalien((random.random()*(240-32),random.random()*(180-32)),12)
                    dumalienarr.append(newAlien)
                else:
                    perc=0

            #score
            font = pygame.font.SysFont("Arial", 10)
            text = font.render("SCORE: "+ str(score), True, (150,150,150,.1))
            screen.blit(text, (10, 10))


            pygame.draw.rect(screen,(200,200,200),pygame.Rect((220,10),(10,160)), 1)
            if perc<.3:
                pygame.draw.rect(screen,(200,50,50,.5),pygame.Rect((222,12),(6,perc*156)), 0)
            else:
                pygame.draw.rect(screen,(50,200,50,.5),pygame.Rect((222,12),(6,perc*156)), 0)

            if perc<=.001:
                go=True
                dumalienarr=[]
                pygame.draw.rect(screen,(100,100,100,.5),pygame.Rect((4,4),(232,172)), 0)
                text = str("ded.")
                font = pygame.font.SysFont("Arial", 25)
                text = font.render(text, True, (150,100,150))
                screen.blit(text, (10, 8))
                dedscreen=True


        if go and dedscreen!=True:
            scorescreen=True
            screen.fill((0,50,50))

            font = pygame.font.SysFont("Arial", 25)
            text = font.render("SCORE: "+ str(score), True, (150,150,150,.1))
            screen.blit(text, (10, 20))
            
            font = pygame.font.SysFont("Arial", 10)
            text = font.render("HIGH SCORES: ", True, (150,150,150,.1))
            screen.blit(text, (10, 50))

            f=open("highscores.txt","r")
            i=0
            arrHighScores=[]
            lowestHighScore=0
            for line in f:
                i+=1
                arr=line.split(",")
                arrHighScores.append(arr)
                txt=str(arr[0])+": " + str(arr[1]).strip()
                font = pygame.font.SysFont("Arial", 10)
                text = font.render(txt, True, (150,150,150))
                screen.blit(text, (20, 52+10*i))
                lowestHighScore=int(arr[1])
            f.close()
            if score>=lowestHighScore:
                if keypress_handled!=True:
                    if len(highScorePerson)<3:
                        highScorePerson=highScorePerson+myChar
                    keypress_handled=True
                blink_dt+=dt
                if blink_dt>blink_time:
                    blinker_idx=(blinker_idx+1)%len(blinker)
                    blink_dt=0
                    
                font = pygame.font.SysFont("Arial", 10)
                if len(highScorePerson)<3:
                    text = font.render(highScorePerson+blinker[blinker_idx], True, (150,150,150))
                else:
                    text = font.render(highScorePerson, True, (150,150,150))
                    if hs_written==False:
                        f=open("highscores.txt","w")
                        my_hs_written=False
                        for hs_i in range(len(arrHighScores)):
                            if score>=int(arrHighScores[hs_i][1]) and my_hs_written==False:
                                f.write(highScorePerson + "," + str(score)+"\n")
                                my_hs_written=True
                            if hs_i<len(arrHighScores)-1:
                                f.write(arrHighScores[hs_i][0]+","+arrHighScores[hs_i][1])

                        hs_written=True
                        f.close()
                newHsTxt = font.render("HEW HIGH SCORE! Enter Name:", True, (150,150,150))
                screen.blit(newHsTxt, (30,160))
                screen.blit(text, (200,160))

             

        pygame.display.flip()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
