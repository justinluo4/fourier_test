import pygame
import numpy as np
from svgpathtools import svg2paths2
paths, attributes, svg_attributes = svg2paths2(r'(full file path here)')


def fourier(iters, sequence, divs): #computes [iters] terms of the discrete fourier series of the cycle sequence
    coefs = []
    final_wave = [0] * divs
    base_wave = [sequence[int(np.floor(n*len(sequence)/divs))] for n in range(divs)]
    remaining = base_wave
    cosine = [np.cos(2 * np.pi * x) for x in np.arange(0, 1, 1 / divs)]
    sine = [np.sin(2 * np.pi * x) for x in np.arange(0, 1, 1 / divs)]
    for iteration in range(iters):
        average = sum([base_wave[n]*cosine[(n*iteration)%divs] for n in range(divs)])/divs
        if iteration != 0:
            average = average*2
        coefs.append(average)
        for n, point in enumerate(cosine):
            final_wave[n] += cosine[(n*iteration)%divs] * average
        average = sum([base_wave[n]*sine[(n*iteration)%divs] for n in range(divs)])/divs
        if iteration != 0:
            average = average*2
        coefs.append(average)
        for n, point in enumerate(sine):
            final_wave[n] += sine[(n*iteration)%divs] * average
    return coefs, final_wave


def display_wave_2d(ywave, xwave, sequencex, sequencey, divs): #Draws the 2d cycle of the fourier series on a dynamically sized window
    screen.fill((0, 0, 0))
    baseline_height = -min(ywave) / (max(ywave) - min(ywave)) * height
    vert_scale = height / (max(ywave) - min(ywave))
    baseline_width = -min(xwave) / (max(xwave) - min(xwave)) * height
    horiz_scale = height / (max(xwave) - min(xwave))
    pygame.draw.circle(screen, (255, 255, 0), (int(baseline_width), int(baseline_height)), 5)
    for i in range(len(sequencex)):
        pygame.draw.circle(screen, (255, 0, 0), (int(sequencex[i] * horiz_scale + baseline_width), int(sequencey[i] * vert_scale + baseline_height)), 5)
    for i in range(divs):
        screen.set_at((int(xwave[i]*horiz_scale + baseline_width), int(ywave[i]*vert_scale + baseline_height)), (255,255,255))

def display_wave(wave, sequence, divs): #1d fourier cycle display (unused)
    screen.fill((0, 0, 0))
    baseline_height = -min(wave) / (max(wave) - min(wave)) * height
    vert_scale = height / (max(wave) - min(wave))
    pygame.draw.line(screen, (100,100,255), (0, baseline_height), (width, baseline_height), 5)
    pygame.draw.line(screen, (100, 100, 100), (0, baseline_height-vert_scale), (width, baseline_height-vert_scale), 5)
    pygame.draw.line(screen, (100, 100, 100), (0, baseline_height+vert_scale), (width, baseline_height+vert_scale), 5)
    for i in range(divs):
        screen.set_at((int(width*i/divs), int(wave[i]*vert_scale + baseline_height)), (255,255,255))


def fixed_display(ywave, xwave, sequencex, sequencey, divs, show_dots = True, show_path = True): #Draws the 2d cycle of the fourier series onto a fixed window
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (50, 255, 50), (int(width / 2), int(height / 2)), 3)
    if show_dots:
        for i in range(len(sequencex)):
            pygame.draw.circle(screen, (100 , 100, 100), (int(sequencex[i]*width/(window_horiz_size*2 )+ width/2), int(sequencey[i]*height/(window_vert_size*2) + height/2)), 2)
    if show_path:
        for i in range(divs):
            screen.set_at((int(xwave[i]*width/(window_horiz_size*2) + width/2), int(ywave[i]*height/(window_vert_size*2) + height/2)), (255,int(255*i/divs),int(255*i/divs)))

def draw_arm(x_coefs, y_coefs, t): #Draws the arm at a certain time
    cur_x = 0
    cur_y = 0
    for i in range(len(x_coefs)//2):
        c1 = x_coefs[2*i]
        c2 = x_coefs[2 * i+1]
        c3 = y_coefs[2 * i]
        c4 = y_coefs[2 * i+1]
        arm1theta = np.arctan((c3 - c2) / (c1 + c4))
        arm1len = (c1 + c4) / (2 * np.cos(arm1theta))
        arm2theta = np.arctan((c3 + c2) / (c1 - c4))
        arm2len = (c1 - c4) / (2 * np.cos(arm2theta))
        pygame.draw.line(screen, (255, 255, 255), (int(cur_x * width / (window_horiz_size * 2) + width / 2),
                                                   int(cur_y * height / (window_vert_size * 2) + height / 2)), (
                         int((cur_x + arm1len * np.cos(arm1theta+ i*t)) * width / (window_horiz_size * 2) + width / 2),
                         int((cur_y + arm1len * np.sin(arm1theta+ i*t)) * height / (window_vert_size * 2) + height / 2)), 1)
        cur_x += arm1len * np.cos(arm1theta+ i*t)
        cur_y += arm1len * np.sin(arm1theta+ i*t)
        pygame.draw.line(screen, (255, 255, 255), (int(cur_x * width / (window_horiz_size * 2) + width / 2),
                                                   int(cur_y * height / (window_vert_size * 2) + height / 2)), (
                         int((cur_x + arm2len * np.cos(arm2theta- i*t)) * width / (window_horiz_size * 2) + width / 2),
                         int((cur_y + arm2len * np.sin(arm2theta- i*t)) * height / (window_vert_size * 2) + height / 2)), 1)
        cur_x += arm2len * np.cos(arm2theta- i*t)
        cur_y += arm2len * np.sin(arm2theta- i*t)

# initialize all parameters
clock = pygame.time.Clock()
divisions = 5000
width = 1000
height = 1000
rpm = 2
window_horiz_size = 10
window_vert_size = 10
screen = pygame.display.set_mode((width,height))
# sequence1 = [1,2,3,2,1,-1,-2,-3,-2,-1,0]
sequencex = []
sequencey = []
skip = []
n = 1
show_path = True
show_dots = True
time = 0
paused = 1
redpath = paths[0]

file_divs = 1000


for i in range(1, file_divs+1):
    point = redpath.point(i/file_divs)
    sequencex.append(point.real/50 - 3)
    sequencey.append(point.imag/50 - 3)
cx, xwave = fourier(n, sequencex, divisions)
cy, ywave = fourier(n, sequencey, divisions)
while(True): # main loop
    #tick the clock and display the arm & cycle
    dt = clock.tick(60)
    time += rpm*dt/(3000*np.pi) * paused
    fixed_display(ywave, xwave, sequencex, sequencey, divisions, show_dots, show_path)
    draw_arm(cx, cy, time)

    for event in pygame.event.get(): # keyboard events
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN: # add point into sequence at mouse position when clicked
            mx, my = pygame.mouse.get_pos()
            sequencex.append((mx - width/2)*(window_horiz_size*2)/width)
            sequencey.append((my - height / 2) * (window_vert_size * 2)/width)
            cx, xwave = fourier(n, sequencex, divisions)
            cy, ywave = fourier(n, sequencey, divisions)



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # remove one term of the fourier series
                print("left")
                n -= 1
                cx, xwave = fourier(n, sequencex, divisions)
                cy, ywave = fourier(n, sequencey, divisions)
                #display_wave(xwave, sequencex, divisions)
                print(n)
                print(cx)
                print(cy)
            if event.key == pygame.K_RIGHT: # add a term to the fourier series
                print("right")
                n += 1
                cx, xwave = fourier(n, sequencex, divisions)
                cy, ywave = fourier(n, sequencey, divisions)
                #display_wave(xwave, sequencex, divisions)
                print(n)
                print(cx)
                print(cy)
            if event.key == pygame.K_BACKSPACE: # remove the last point of the sequence
                sequencex = sequencex[:-1]
                sequencey = sequencey[:-1]
                cx, xwave = fourier(n, sequencex, divisions)
                cy, ywave = fourier(n, sequencey, divisions)
                # display_wave(xwave, sequencex, divisions)
                print(n)
                print(cx)
                print(cy)
            if event.key == pygame.K_DELETE: # remove the first point of the sequence
                sequencex = sequencex[1:]
                sequencey = sequencey[1:]
                cx, xwave = fourier(n, sequencex, divisions)
                cy, ywave = fourier(n, sequencey, divisions)
                #display_wave(xwave, sequencex, divisions)
                print(n)
                print(cx)
                print(cy)
            if event.key == pygame.K_UP: # toggle the input sequence display
                show_dots = (show_dots == False)
                # display_wave(xwave, sequencex, divisions)
            if event.key == pygame.K_DOWN: # toggle the cycle display
                show_path = (show_path == False)
            if event.key == pygame.K_MINUS: # slow animation
                rpm = rpm * 0.8
            if event.key == pygame.K_EQUALS: # speed up animation
                rpm = rpm / 0.8
            if event.key == pygame.K_p: # pause
                if paused == 0:
                    paused = 1
                else:
                    paused = 0
            if event.key == pygame.K_0: # reverse animation
                paused = paused * -1
                # display_wave(xwave, sequencex, divisions)

    pygame.display.update()


