from __future__ import absolute_import, division
from psychopy import gui, visual, core, event, data, logging, sound
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
import random
import time
import pandas as pd
from pandas import DataFrame
import Task_helper as helper

########### Set up the task for the desired version ###########

### task associated with precommitment 1 ###

difference = [4, 12, 20, 28]
changes = [13, 9, 3, -3, -9, -13]
Condition = "NA"

### task associated with precommitment 2 ###

## Stable condition 
#difference = [1, 7, 13, 19]
#changes = [6, 3, 1, -1, -3, -6]
#Condition = "Stable"

## Volatile condition
#difference = [1, 7, 13, 19]
#changes = [16, 13, 11, -11, -13, -16]
#Condition = "Volatile"

########### Basic experiment settings ###########

### Store info about the experiment session ###
expName = 'PreComm_Task'  # from the Builder filename that created this script
expInfo = {'participant':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = time.strftime("%d%m%Y")  # data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

### Ensure that relative paths start from the same directory as this script ###
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expName, expInfo['participant'], expInfo['date'])

# use an ExperimentHandler to handle saving data
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None, originPath=None,
    savePickle=True, saveWideText=True, dataFileName=filename)

###### Setup the Window #######
win = visual.Window(
    size=(2560, 1440), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True)

# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
print('measured frame rate: ')
print(expInfo['frameRate'])
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0  # couldn't get a reliable measure so guess

#function to check for escape throughout the experiment 
def check_for_escape():
    if 'escape' in event.getKeys():
        core.quit()

###############################
##### Task-specific setup #####

### Task parameters ####
nTrials = 96  # number of trials
rewardAmount = 0  # cumulative reward amount
response = 0
length = 0.62
increase = 0.1
stim = helper.stim(win)

###### set clocks #######
# create clock and timer
globalClock = core.Clock()  # this tracks all of the time of the experiment
trialClock = core.Clock()

# Set up the different options to be picked from (new for each participant)
options = []
for _ in range(4):
    numbers = list(range(0, 24))
    random.shuffle(numbers)
    options.extend(numbers)

print(options)
##############################
###### Begin experiment ######
##############################


#Start with the welcome screen 
start = visual.TextStim(win, text= 'Welcome! \n Press ENTER to begin task', height= 0.1,
                        pos=[0, 0], wrapWidth=10, alignHoriz='center')
start.draw()
win.flip()
event.waitKeys(keyList=['return'])
globalClock.reset()

# First trial loop
for trialIdx in range(nTrials):
    # clear events from previous trial/ prevents a click from the previous trial to be counted on this trial
    event.clearEvents()
    trialClock.reset()
    # Variables that need to be zeroed out each trial
    RT_choice = 0  # RT for decision to either precommit or wait
    RT_play = 0  # RT to press space in play condition on mid_clock (from square onset)
    RT_precomm = 0  # RT for decision of either left or right in commit clock
    RT_late = 0  # RT to press space if late in play condition on trial_clock (from initial trial onset)
    RT_trialClock_play = 0  # RT to press space in play condition on trial_clock (from initial trial onset)
    cents = 0 # amount of money you will earn on this trial
    loosing_win = 0   # if you loose MID but get money
    # Variables for record keeping (will be in csv file)
    blank = str(length)  # amount of time the white square is on the screen
    isi_time = 0  # isi interval changes each trial
    lost_type = 0  # if you get endA or endB if you fail in the play condition
    space = 0  # if press space during MID time
    no_space = 0  # if do not press space during MID
    early = 0 # if press space too early in MID
    # start with the cross before each trial
    helper.draw_and_wait(win, stim['isi'], 1)
    # pick the book cover image to appear on the screen
    cover_number = random.choice(range(1, 99, 1))
    book = visual.ImageStim(win, image='Books/' + str(cover_number) + '.png', units='height',
                            pos=[0, 0], size=[0.4, 0.8], interpolate=True)
    helper.draw_and_wait(win, book, 1)
    check_for_escape()
    # start with the cross before each trial
    helper.draw_and_wait(win, stim['isi'], 1)
    optionValues = helper.values(Condition, difference, changes, options, trialIdx)
    # stimuli that need to change for each trial
    # option A is on the left side of screen
    pickoptionA   =   visual.TextStim(win=win, text=optionValues['optionA'], name='optionA',
                                  pos=[-0.5, -0.3], rgb=None, color=(1, 1, 1), colorSpace='rgb')
    # option B is on the right side of screen
    pickoptionB   =   visual.TextStim(win=win, text=optionValues['optionB'], name='optionB',
                                  pos=[0.5, -0.3], rgb=None, color=(1, 1, 1), colorSpace='rgb')
    endoptionA    =   visual.TextStim(win=win, text=optionValues['endA'], name='endA',
                                 pos=[-0.5, -0.3], rgb=None, color=(1, 1, 1), colorSpace='rgb')
    endoptionB    =   visual.TextStim(win=win, text=optionValues['endB'], name='endB',
                                 pos=[0.5, -0.3], rgb=None, color=(1, 1, 1), colorSpace='rgb')
    # prepare to start routine "pick options"
    value_bars = helper.visual_bars(win, optionValues)
    # Draw the trial screen
    stim['optionText'].draw()
    for item in [stim['outline_barA'], stim['outline_barB'], value_bars['option_barA'], value_bars['option_barB'], 
                pickoptionA, pickoptionB, stim['stimA_left'], stim['stimB_right']]:
        item.setAutoDraw(True)
    # pick options routine
    check_for_escape()
    pickChoice = helper.pickoptions(win, trialClock)
    RT_choice = pickChoice['RT_choice']
    # if choose to play ('wait') on this trial
    if pickChoice['wait']:
        # screen to show that play was chosen
        choice = 'wait'
        helper.draw_and_wait(win, stim['waitText'], 1.5)
        # start play routine with fixation cross
        helper.draw_and_wait(win, stim['isi'], 1)
        check_for_escape()
        # show the values changing to the new values first
        helper.draw_and_wait(win, stim['change_values'], 1)
        for item in [value_bars['option_barA'], value_bars['option_barB'], pickoptionA, pickoptionB]:
            item.setAutoDraw(False)
        # show the values change in bar
        values_change = helper.values_change(win, optionValues)
        # show progressive change of values
        bars_change = helper.progressive(win, values_change)
        check_for_escape()
        # show the final values and the one that you earn on this trial
        for item in [values_change['step6_barA'], values_change['step6_barB'], endoptionA, endoptionB]:
            item.setAutoDraw(True)
        helper.draw_and_wait(win, stim['Final_value'], 1.5)
        stim['attempt'].draw()  # wait screen that will say "ready"
        if event.getKeys(keyList='space'):
            early = 1
        win.flip()
        core.wait(2)
        if event.getKeys(keyList='space'):
            early = 1
        check_for_escape()
        # pick the amount of time the fixation cross will be on the screen before white square
        timing_list = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        isi_time = random.choice(timing_list)
        stim['isi'].draw()
        win.flip()
        if event.getKeys(keyList='space'):
            early = 1
        core.wait(isi_time)
        if event.getKeys(keyList='space'):
            early = 1
        # run the mid routine
        play_mid = helper.play_mid(win, trialClock, length)
        RT_play = play_mid['RT_play']
        RT_trialClock_play = play_mid['RT_trialClock_play']
        space = play_mid['press_hit']
        no_space = play_mid['press_miss']
        win.flip()
        core.wait(1)
        check_for_escape()
        # if do not pick within the allowed time (you "lost" the game)
        if play_mid['miss'] or early == 1:
            response = 'miss'
            # increase the amount of time the white square will be on the screen next time
            length += increase
            # start the press_late routine to see if tried but pressed late
            press_late = helper.press_late(win, trialClock)
            RT_late = press_late['RT_late']
            win.flip()
            # if you loose the game, one of the two options will be randomly chosen
            potentials = [optionValues['endA'], optionValues['endB']]
            loosing_win = random.choice(potentials)
            # indicate on the screen that you did not hit
            helper.draw_and_wait(win, stim['miss'], 1)
            # calculate the amount of money that will be earned if you lost
            cents = loosing_win
            win.flip()
            core.wait(2)
            # indicate that one is chosen for you
            helper.draw_and_wait(win, stim['chosen'], 1)
            check_for_escape()
            # the next two division loops vary based on which of the two end options were randomly chosen for you
            if loosing_win == optionValues['endA']:
                lost_type = 'endA'
                cents = optionValues['endA']
                win.flip()
                core.wait(0.5)
                check_for_escape()
                # highlight the option that you got
                stim['highlight_A'].setAutoDraw(True)
                win.flip()
                core.wait(2)
                reward_amountA = str(optionValues['endA'])
                # show on the screen the amount that you earned
                winning_textA = visual.TextStim(win, text='Get \n' + str(reward_amountA) + '  points!',
                                                wrapWidth=4, height=0.1, pos=[0, 0])
                helper.draw_and_wait(win, winning_textA, 1)
                # nonstring record for the cumulative reward amount record
                money = optionValues['endA']
                # clear the screen
                for item in [stim['stimA_left'], stim['stimB_right'], stim['outline_barB'], stim['outline_barA'], endoptionA,
                            values_change['step6_barA'], values_change['step6_barB'], endoptionB, stim['highlight_A']]:
                    item.setAutoDraw(False)
            elif loosing_win == optionValues['endB']:
                lost_type = 'endB'
                cents = optionValues['endB']
                win.flip()
                core.wait(0.5)
                check_for_escape()
                # highlight the option that you got
                stim['highlight_B'].setAutoDraw(True)
                win.flip()
                core.wait(2)
                reward_amountB = str(optionValues['endB'])
                # show on the screen the amount that you earned
                winning_textB = visual.TextStim(win, text='Get \n' + str(reward_amountB) + '  points!',
                                                wrapWidth=4, height=0.1, pos=[0, 0])
                helper.draw_and_wait(win, winning_textB, 1)
                # nonstring record for the cumulative reward amount record
                money = optionValues['endB']
                # clear the screen
                for item in [stim['stimA_left'], stim['stimB_right'], stim['outline_barB'], stim['outline_barA'], endoptionA,
                            values_change['step6_barA'], values_change['step6_barB'], endoptionB, stim['highlight_B']]:
                    item.setAutoDraw(False)
        # if hit the white square in the allocated time
        if play_mid['hit'] and early == 0:
            response = 'hit'
            check_for_escape()
            # remove time of the length if you get a hit
            length -= increase
            # tell them that it was a hit
            helper.draw_and_wait(win, stim['got_it'], 1)
            # now have the ability to choose which one they want
            stim['chooseText'].draw()
            hit_pick = helper.hit_pick(win, trialClock)
            RT_hitChoice = hit_pick['RT_hitChoice']
            # if choose second B
            if hit_pick['B']:  # if choose the end B option after winning
                response = 'hit_pickB'
                check_for_escape()
                cents = optionValues['endB']
                stim['highlight_B'].setAutoDraw(True)
                win.flip()
                core.wait(0.5)
                reward_amountB = str(optionValues['endB'])
                # show on the screen the amount that you earned
                winning_textB = visual.TextStim(win, text='Get \n' + str(reward_amountB) + '  points!',
                                               wrapWidth=4, height=0.1, pos=[0, 0])
                # nonstring record for the cumulative reward amount record
                money = optionValues['endB']
                helper.draw_and_wait(win, winning_textB, 2)
                # clear the screen
                for item in [values_change['step6_barA'], values_change['step6_barB'], endoptionA, endoptionB, 
                            stim['outline_barB'], stim['outline_barA'], stim['stimA_left'], stim['stimB_right'], stim['highlight_B']]:
                    item.setAutoDraw(False)
                check_for_escape()
            elif hit_pick['A']:  # if choose the end A option after winning
                response = 'hit_pickA'
                check_for_escape()
                cents = optionValues['endA']
                stim['highlight_A'].setAutoDraw(True)
                win.flip()
                core.wait(0.5)
                reward_amountA = str(optionValues['endA'])
                # show on the screen the amount that you earned
                winning_textA = visual.TextStim(win, text='Get \n' + str(reward_amountA) + '  points!',
                                               wrapWidth=4, height=0.1, pos=[0, 0])
                # nonstring record for the cumulative reward amount record
                money = optionValues['endA']
                helper.draw_and_wait(win, winning_textA, 2)
                # clear the screen
                for item in [values_change['step6_barA'], values_change['step6_barB'], endoptionA, endoptionB, 
                            stim['outline_barB'], stim['outline_barA'], stim['stimA_left'], stim['stimB_right'], stim['highlight_A']]:
                    item.setAutoDraw(False)
                check_for_escape()
            elif hit_pick['miss']:  # if did not pick an option after winning
                response = 'hit_pick_miss'
                check_for_escape()
                cents = 0
                win.flip()
                core.wait(1)
                helper.draw_and_wait(win, stim['miss'], 1)
                miss_text = visual.TextStim(win, text='Receive no Points', height=0.1, pos=[0, 0])
                helper.draw_and_wait(win, miss_text, 1)
                money = 0
                for item in [values_change['step6_barA'], values_change['step6_barB'], endoptionA, endoptionB, 
                            stim['outline_barB'], stim['outline_barA'], stim['stimA_left'], stim['stimB_right']]:
                    item.setAutoDraw(False)
                check_for_escape()
    # if choose to precommit on this trial
    elif pickChoice['commit']:
        # indicate that pick was chosen for this trial
        choice = 'commit'
        check_for_escape()
        # indicate that you choose to commit
        helper.draw_and_wait(win, stim['pickText'], 1.5)
        # state the two stimuli (websites) that you are picking between
        stim['chooseText'].draw()
        # run the pick (precommitment) routine from helper to record options chosen
        precomm = helper.precomm_pick(win, trialClock)
        RT_precomm = precomm['RT_precomm']
        if precomm['B']: # if choose to precommit to the B option
            response = 'precomm_B'
            check_for_escape()
            cents = optionValues['endB']
            win.flip()
            core.wait(0.5)
            # remove the option values
            for item in [pickoptionA, pickoptionB, value_bars['option_barA'], value_bars['option_barB']]:
                item.setAutoDraw(False)
            # highlight that you choose to commit to B
            stim['highlight_B'].setAutoDraw(True)
            # show progressive change of values
            values_change = helper.values_change(win, optionValues)
            bars_change = helper.progressive(win, values_change)
            # show the final values and the one that you earn on this trial
            stim['Final_value'].draw()
            endoptionA.draw()
            value_bars['end_barA'].draw()
            endoptionB.draw()
            value_bars['end_barB'].draw()
            win.flip()
            core.wait(1.8)
            reward_amountB = str(optionValues['endB'])
            # show on the screen the amount that you earned
            winning_textB = visual.TextStim(win, text='Get \n' + str(reward_amountB) + '  points!',
                                            height=0.1, pos=[0, 0])
            check_for_escape()
            winning_textB.draw()
            endoptionA.draw()
            value_bars['end_barA'].draw()
            endoptionB.draw()
            value_bars['end_barB'].draw()
            # nonstring record for the cumulative reward amount record
            money = optionValues['endB']
            win.flip()
            core.wait(1)
            # clear the screen
            for item in [stim['highlight_B'], stim['stimA_left'], stim['stimB_right'], stim['outline_barA'], 
                        stim['outline_barB']]:
                item.setAutoDraw(False)
        elif precomm['A']: # if choose to precommit to the right option
            response = 'precomm_A'
            check_for_escape()
            cents = optionValues['endA']
            win.flip()
            core.wait(0.5)
            # remove the option values
            for item in [pickoptionA, pickoptionB, value_bars['option_barA'], value_bars['option_barB']]:
                item.setAutoDraw(False)
            # highlight that you choose to commit to A
            stim['highlight_A'].setAutoDraw(True)
            win.flip()
            # show progressive change of values
            values_change = helper.values_change(win, optionValues)
            bars_change = helper.progressive(win, values_change)
            # show the final values and the one that you earn on this trial
            check_for_escape()
            stim['Final_value'].draw()
            endoptionA.draw()
            value_bars['end_barA'].draw()
            endoptionB.draw()
            value_bars['end_barB'].draw()
            win.flip()
            core.wait(1.8)
            reward_amountA = str(optionValues['endA'])
            # show on the screen the amount that you earned
            winning_textA = visual.TextStim(win, text='Get \n' + str(reward_amountA) + '  points!',
                                            height=0.1, pos=[0, 0])
            winning_textA.draw()
            endoptionA.draw()
            value_bars['end_barA'].draw()
            endoptionB.draw()
            value_bars['end_barB'].draw()
            # nonstring record for the cumulative reward amount record
            money = optionValues['endA']
            win.flip()
            core.wait(1)
            # clear the screen
            for item in [stim['highlight_A'], stim['stimA_left'], stim['stimB_right'], stim['outline_barA'], 
                        stim['outline_barB']]:
                item.setAutoDraw(False)
        # if you fail to pick one of the options after choosing to precommit
        elif precomm['miss']:
            check_for_escape()
            response = 'precomm_miss'
            helper.draw_and_wait(win, stim['miss'], 1.5)
            cents = 0
            miss_text = visual.TextStim(win, text='Received no money', height=0.1, pos=[0, 0])
            check_for_escape()
            helper.draw_and_wait(win, miss_text, 1)
            money = 0
            # clear the screen
            for item in [value_bars['option_barA'], value_bars['option_barB'], pickoptionA, pickoptionB, 
                        stim['stimA_left'], stim['stimB_right'], stim['outline_barA'], stim['outline_barB']]:
                item.setAutoDraw(False)
    # if you missed choosing to either pick or play
    elif pickChoice['miss']:
        choice = 'miss'
        helper.draw_and_wait(win, stim['miss'], 1.5)
        check_for_escape()
        cents = 0
        miss_text = visual.TextStim(win, text='Received no money', height=0.1, pos=[0, 0])
        helper.draw_and_wait(win, miss_text, 1)
        money = 0
        # clear the screen
        for item in [value_bars['option_barA'], value_bars['option_barB'], pickoptionA, pickoptionB, 
                    stim['stimA_left'], stim['stimB_right'], stim['outline_barA'], stim['outline_barB']]:
            item.setAutoDraw(False)
        check_for_escape()
    # update earnings
    rewardAmount += money

    # log data
    thisExp.addData('TrialNumber', trialIdx+1)
    thisExp.addData('Condition', Condition)
    thisExp.addData('OptionA', optionValues['optionA'])
    thisExp.addData('OptionB', optionValues['optionB'])
    thisExp.addData('EndA', optionValues['endA'])
    thisExp.addData('EndB', optionValues['endB'])
    thisExp.addData('combination', optionValues['combo'])
    thisExp.addData('difference', optionValues['difference'])
    thisExp.addData('change', optionValues['change'])
    thisExp.addData('Choice_RT', RT_choice)
    thisExp.addData('Choice_Wait', choice == 'wait')
    thisExp.addData('Choice_Commit', choice == 'commit')
    thisExp.addData('Choice_Miss', choice == 'miss')
    thisExp.addData('Press_hit', space)
    thisExp.addData('Play_RT', RT_play)
    thisExp.addData('RT_trialClock_play', RT_trialClock_play)
    thisExp.addData('ITI_play', isi_time)
    thisExp.addData('Square_timing', blank)
    thisExp.addData('Press_miss', no_space)
    thisExp.addData('Play_win_A', response == 'hit_pickA')
    thisExp.addData('Play_win_B', response == 'hit_pickB')
    thisExp.addData('Late_RT', RT_late)
    thisExp.addData('Play_lost', response == 'lost_game')
    thisExp.addData('Play_lost_chosenA', lost_type == 'endA')
    thisExp.addData('Play_lost_chosenB', lost_type == 'endB')
    thisExp.addData('Precomm_RT', RT_precomm)
    thisExp.addData('Precomm_B', response == 'precomm_B')
    thisExp.addData('Precomm_A', response == 'precomm_A')
    thisExp.addData('Precomm_miss', response == 'precomm_miss')
    thisExp.addData('Earnings', money)
    thisExp.nextEntry()
# end of trial loop


# show earnings on entire block (divided by 4 for better money earnings)
check_for_escape()
money_value = (rewardAmount/400.00)
rounded_value = round(money_value, 2)
print(rounded_value)
moneyontrial = visual.TextStim(win, text='Checkout. \n You received $' + str(rounded_value)
                                        + '\n for selling your books!', height=0.1)
moneyontrial.draw()
win.flip()
# right now need to press enter to end the experiment
event.waitKeys(keyList=['return'])


###########################
##### Close-out steps #####

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()

# end the experiment
thisExp.abort()
# close the window
win.close()
# end the experiment
core.quit()