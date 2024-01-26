from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
import random



##############################################################

def draw_and_wait(win, stim, duration, keys=None):
    """
    Draws a stimulus on the window, flips the window, waits for a specified duration,
    and optionally waits for a key press.

    :param win: The PsychoPy window object.
    :param stim: The stimulus (or list of stimuli) to draw.
    :param duration: Duration to wait after drawing.
    :param keys: Optional list of keys to wait for. If None, just waits for the duration.
    :return: The key pressed if keys is not None, otherwise None.
    """
    if isinstance(stim, list):
        for s in stim:
            s.draw()
    else:
        stim.draw()

    win.flip()

    if keys:
        return event.waitKeys(keyList=keys, maxWait=duration)
    else:
        core.wait(duration)


def stim(win):
    # stimuli outside loop = stimuli that do not change ###
    stimA_name    = 'Bookbyte'
    stimB_name    = 'BookScouter'
    stimA_left    = visual.ImageStim(win, image='Images/' + stimA_name + '.png', units='height',
                                pos=[-0.4, -0.35], size=[0.4, 0.17], name=stimA_name, interpolate=True)
    stimB_right   = visual.ImageStim(win, image='Images/' + stimB_name + '.png', units='height',
                                pos=[0.4, -0.35], size=[0.4, 0.17], name=stimB_name, interpolate=True)
    isi           = visual.TextStim(win, text='+')
    optionText    = visual.TextStim(win=win, text='Wait for New Prices \n or \n Commit Now', height=0.1,
                                pos=[0, 0], wrapWidth=8, alignHoriz='center', alignVert='center', ori=0.0)
    pickText      = visual.TextStim(win, text='Commit', height=0.1)
    waitText      = visual.TextStim(win, text='Wait', height=0.1)
    chooseText    = visual.TextStim(win, text=str(stimA_name) + ' or ' + str(stimB_name), height=0.1)
    outline_barA  = visual.Rect(win, width=0.2, height=0.8, lineColor=[1, 1, 1], lineWidth=3, autoLog=None,
                                pos=[-0.5, 0.3])
    outline_barB  = visual.Rect(win, width=0.2, height=0.8, lineColor=[1, 1, 1], lineWidth=3, autoLog=None, 
                                pos=[0.5, 0.3])
    change_values = visual.TextStim(win, text='values change', height=0.1, pos=[0, 0], wrapWidth=10)
    Final_value   = visual.TextStim(win, text='new values', height=0.1)
    attempt       = visual.TextStim(win, text='ready')
    highlight_A   = visual.Rect(win, width=0.65, height=1.9, lineWidth=5, lineColor=[1, -1, -1], autoLog=None, 
                                pos=[-0.5,0])
    highlight_B   = visual.Rect(win, width=0.65, height=1.9, lineWidth=5, lineColor=[1, -1, -1], autoLog=None, 
                                pos=[0.5,0])
    miss          = visual.TextStim(win, text='missed', height=0.1)
    chosen       = visual.TextStim(win, text='One Website was \n Picked for You', height=0.1, wrapWidth=6)
    got_it        = visual.TextStim(win, text='hit', height=0.1)
    half          = visual.TextStim(win, text = ' Break \n Press ENTER to continue', height=0.1, pos=[0,0],
                                wrapWidth=10, alignHoriz='center')
    stim = {'stimA_left': stimA_left, 'stimB_right': stimB_right,'isi': isi, 'optionText': optionText,
            'pickText': pickText, 'waitText': waitText, 'chooseText': chooseText, 'outline_barA': outline_barA,
            'outline_barB': outline_barB, 'change_values': change_values, 'Final_value': Final_value,
            'attempt': attempt,'highlight_A': highlight_A, 'highlight_B': highlight_B, 'miss': miss,
            'chosen': chosen, 'got_it': got_it, 'half': half}
    return stim

#def values(Condition, differences, changes, optionsA, optionsB, optionsC, optionsD):
def values(Condition, differences, changes, options, trialIdx):
    diff = np.repeat(differences, 6)
    change = changes * 4
    # Combine to form a vector
    combination = list(zip(diff, change))
    pick = options[trialIdx]
    if pick is not None:
        # Determine which change/difference combination on this trial
        d, c = combination[pick]
        # Get starting values based on version
        if Condition == "Stable":
            start_range = range(6, 75, 1)
        elif Condition == "Volatile":
            start_range = range(16, 65, 1)
        elif Condition == "NA":
            start_range = range(13, 58, 1)

        First_start = random.choice(start_range)
        Second_start = First_start + d
        
        # Calculate ending values
        First_end = First_start - c
        Second_end = Second_start + c
        
        # Randomly place the options on either the right or the left
        if random.choice(['Right', 'Left']) == 'Right':
            A_start, A_end, B_start, B_end = First_start, First_end, Second_start, Second_end
        else:
            A_start, A_end, B_start, B_end = Second_start, Second_end, First_start, First_end
        
    optionValues = {'combo': pick, 'difference': d, 'change': c, 'optionA': A_start, 'optionB': B_start, 'endA': A_end, 'endB': B_end}
    return optionValues


def visual_bars(win, optionValues):
    # complete the path for calculating changing values
    h_optionA = (int(optionValues['optionA'])/100) * 0.8
    p_optionA = (-0.1 + h_optionA/2)
    h_endA = (int(optionValues['endA'])/100) * 0.8
    p_endA = (-0.1 + h_endA/2)
    h_optionB = (int(optionValues['optionB'])/100) * 0.8
    p_optionB = (-0.1 + h_optionB/2)
    h_endB = (int(optionValues['endB'])/100) * 0.8
    p_endB = (-0.1 + h_endB/2)
    # visual bars
    option_barA = visual.Rect(win=win, width=0.2, height=h_optionA, lineColor=[0, 1, 0],
                              autoLog=None, fillColor=[0, 1, 0], pos=[-0.5, p_optionA])
    option_barB = visual.Rect(win=win, width=0.2, height=h_optionB, lineColor=[0, 1, 0],
                              autoLog=None, fillColor=[0, 1, 0], pos=[0.5, p_optionB])
    end_barA    = visual.Rect(win=win, width=0.2, height=h_endA, lineColor=[0, 1, 0],
                              autoLog=None, fillColor=[0, 1, 0], pos=[-0.5, p_endA])
    end_barB    = visual.Rect(win=win, width=0.2, height=h_endB, lineColor=[0, 1, 0],
                              autoLog=None, fillColor=[0, 1, 0], pos=[0.5, p_endB])
    value_bars = {'option_barA': option_barA, 'option_barB': option_barB, 'end_barA': end_barA, 'end_barB': end_barB,
                  'h_endA': h_endA, 'p_endA': p_endA, 'h_endB': h_endB, 'p_endB': p_endB}
    return value_bars


###### Pick to play or not routine ######
def pickoptions(win, trialClock):
    response = 0
    RT_choice = 0
    win.flip()
    # record responses
    theseKeys = event.waitKeys(keyList=['up', 'down', 'escape'], maxWait=4)
    if theseKeys == ['up']: # pick wait
        response = 1
        RT_choice = trialClock.getTime()
        win.flip()
    if theseKeys == ['down']: # pick pick
        response = 2
        RT_choice = trialClock.getTime()
        win.flip()
    if theseKeys == None: # did not pick
        response = 3
        RT_choice = trialClock.getTime()
        win.flip()   
    choice_1 ={'wait': response == 1, 'commit': response == 2, 'miss': response == 3, 'RT_choice': RT_choice}
    return choice_1


#### precommitment (pick) routine ####
def precomm_pick(win, trialClock):
    response = 0
    RT_precomm = 0
    win.flip()
    # record responses
    theseKeys = event.waitKeys(keyList=['left', 'right', 'escape'], maxWait=3)
    if theseKeys == ['left']: # pick left
        response = 1
        RT_precomm = trialClock.getTime()
        win.flip()
    if theseKeys == ['right']:  # pick right
        response = 2
        RT_precomm = trialClock.getTime()
        win.flip()
    if theseKeys == None: # did not pick
        response = 3
        RT_precomm = trialClock.getTime()
        win.flip()
    choice_2 = {'A': response == 1, 'B': response == 2, 'miss': response == 3, 'RT_precomm': RT_precomm}
    return choice_2


#### RT play routine ####
def play_mid(win, trialClock, length):
    midClock = core.Clock()
    midClock.reset()
    response = 0
    hit = 0
    RT_play = 0
    RT_trialClock_play = 0
    #MID_square
    square = visual.Rect(win=win, width=0.5, height=0.5, autoLog=None, fillColor='white', pos=[0,0])
    square.draw()
    win.flip()
    core.wait(0.2)
    while midClock.getTime() < length:
        theseKeys = event.getKeys(keyList=['space', 'escape'])
        if len(theseKeys) > 0:
            if 'space' in theseKeys:  # hit
                hit = 1
                RT_play = midClock.getTime()
                RT_trialClock_play = trialClock.getTime()
                response = 1
                win.flip()
            else:  # did not pick
                hit = 2
                response = 2
                RT_play = midClock.getTime()
                RT_trialClock_play = trialClock.getTime()
                win.flip()
    if response == 0:
        response = 2
        hit = 2
        win.flip()
    choice_3 = {'hit': response == 1, 'miss': response == 2, 'early': response == 3, 'press_hit': hit == 1,
                'press_miss': hit == 2, 'RT_play': RT_play, 'RT_trialClock_play': RT_trialClock_play}
    return choice_3


#### routine that allows you to pick an option after you win RT game ###
def hit_pick(win, trialClock):
    response = 0
    RT_hitChoice = 0
    win.flip()
    theseKeys = event.waitKeys(keyList=['left', 'right', 'escape'], maxWait=3)
    if theseKeys == ['left']: # pick left
        response = 1
        RT_precomm = trialClock.getTime()
        win.flip()
    if theseKeys == ['right']:  # pick right
        response = 2
        RT_precomm = trialClock.getTime()
        win.flip()
    if theseKeys == None: # did not pick
        response = 3
        RT_precomm = trialClock.getTime()
        win.flip()
    choice_3 = {'A': response == 1, 'B': response == 2, 'miss': response == 3, 'RT_hitChoice': RT_hitChoice}
    return choice_3


### Routine to record if you press the space bar late and do not win the MID play option ###
def press_late(win, trialClock):
    response = 0
    RT_late = 0
    choice_4 = 0
    # record responses
    theseKeys = event.getKeys(keyList=['space', 'escape'])
    if len(theseKeys) > 0:
        if 'space' in theseKeys:  # pick right
            response = 1
            RT_late = trialClock.getTime()
            win.flip()
        else:  # did not pick
            response = 2
            RT_late = trialClock.getTime()
            win.flip()
    if response == 0:
        response = 2
        RT_late = trialClock.getTime()
    choice_4 = {'late_press': response == 1, 'not_late': response == 2, 'RT_late': RT_late}
    return choice_4

def values_change(win, optionValues):
    bars = {}

    for option in ['A', 'B']:
        h_steps = []
        p_steps = []

        optionStart = int(optionValues[f'option{option}'])
        optionEnd = int(optionValues[f'end{option}'])

        for i in range(6):
            difference = optionEnd - optionStart
            step_height = ((optionStart + (difference / 6 * i)) / 100) * 0.8
            h_steps.append(step_height)
            p_steps.append(-0.1 + step_height / 2)

        x_pos = -0.5 if option == 'A' else 0.5
        for i in range(6):
            bar = visual.Rect(win=win, width=0.2, height=h_steps[i], lineColor=[0, 1, 0],
                              autoLog=None, fillColor=[0, 1, 0], pos=[x_pos, p_steps[i]])
            bars[f'step{i+1}_bar{option}'] = bar

    return bars

### Progressive movement of the bars arranged in values_change ###
def progressive(win, values_change):
    values_change['step1_barA'].draw()
    values_change['step1_barB'].draw()
    win.flip()
    core.wait(0.2)
    values_change['step2_barA'].draw()
    values_change['step2_barB'].draw()
    win.flip()
    core.wait(0.2)
    values_change['step3_barA'].draw()
    values_change['step3_barB'].draw()
    win.flip()
    core.wait(0.2)
    values_change['step4_barA'].draw()
    values_change['step4_barB'].draw()
    win.flip()
    core.wait(0.2)
    values_change['step5_barA'].draw()
    values_change['step5_barB'].draw()
    win.flip()
    core.wait(0.2)
    values_change['step6_barA'].draw()
    values_change['step6_barB'].draw()
    win.flip()
    core.wait(0.2)



