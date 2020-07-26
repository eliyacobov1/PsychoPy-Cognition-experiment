import os
import time
import random
import csv
import datetime
import psychopy

# The time period for each of the trial types
SOUND_PERIOD = 0.2
IMAGE_PERIOD = 0.4
FIXATION_PERIOD = 0.1

NUM_TRIALS = 20  # The number of trials

directory = '.\pics'  # directory of the experiment's images

# Trial type names
SPACE_PRESSED = 'Space'
FIXATION_APPEARANCE = 'Fixation'
IMAGE_APPEARANCE = 'Image'
SOUND_PLAYED = 'Sound'

# The number of times each sound will be played
NUM_SOUND_1 = 15
NUM_SOUND_2 = 5

# array to contain documentation details of the experiment
exp_log = []

temp = [os.path.join(directory, filename) for filename in os.listdir(directory)]

images = [visual.ImageStim(win, image=temp[i], pos=(0, 0),
                           size=(1.8, 1)) for i in range(len(temp))]

fixation = visual.ShapeStim(
    win=win, name='polygon', vertices='cross',
    size=(0.09, 0.09),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
    fillColor=[1, 1, 1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)

sound_1 = sound.Sound('./440.wav', secs=1.0, stereo=True, hamming=True)
sound_2 = sound.Sound('./500.wav', secs=1.0, stereo=True, hamming=True)

sounds = [item for sublist in [[sound_1 for i in range(NUM_SOUND_1)],
                               [sound_2 for i in range(NUM_SOUND_2)]] for item in sublist]

welcome_text = visual.TextStim(win=win, name='text',
                               text='Press Space to start',
                               font='Arial',
                               pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                               color='white', colorSpace='rgb', opacity=1,
                               languageStyle='LTR',
                               depth=0.0)

end_text = visual.TextStim(win=win, name='text',
                           text='Experiment Ended!\nPress ESC to exit',
                           font='Arial',
                           pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                           color='white', colorSpace='rgb', opacity=1,
                           languageStyle='LTR',
                           depth=0.0)

continueRoutine = True

welcome_text.setAutoDraw(True)  # The initial screen
win.flip(True)

while True:  # Wait for the user to hit space
    pressed_key = event.getKeys()
    if pressed_key:
        if pressed_key[0] == 'space':
            break

welcome_text.setAutoDraw(False)
win.flip(True)
time.sleep(2)

# while continueRoutine:
start_time = time.clock()  # initiate experiment timer

for i in range(NUM_TRIALS):  # start the loop to display images
    if i % len(images) == 0:
        # Shuffle at the beginning of the experiment
        # and each time all images were displayed
        random.shuffle(temp)
        random.shuffle(sounds)

    time_before = time.clock() if i != 0 else start_time
    fixation.setAutoDraw(True)  # display fixation
    win.flip(True)
    time.sleep(FIXATION_PERIOD)
    fixation.setAutoDraw(False)
    time_after = time.clock()
    exp_log.append([FIXATION_APPEARANCE, time_before - start_time,
                    time_after - start_time])

    pressed_key = event.getKeys()  # Get the key pressed
    if pressed_key:  # if there was an actual key pressed:
        if pressed_key[0] == 'space':
            time_before = time.clock()
            exp_log.append([SPACE_PRESSED, time_before - start_time,
                            time_before - start_time])

    time_before = time.clock()
    images[i % len(images)].setAutoDraw(True)  # display image
    win.flip(True)

    sound_start = time.clock()  # The time when the sound starts playing
    sound_timing = float(random.randint(50, 150)) / 1000
    time.sleep(sound_timing)
    sounds[i % len(images)].play()
    time.sleep(SOUND_PERIOD)
    sounds[i % len(images)].stop()
    sound_end = time.clock()
    exp_log.append([SOUND_PLAYED, sound_start - start_time,
                    sound_end - start_time])

    time.sleep(IMAGE_PERIOD - (SOUND_PERIOD + sound_timing))
    images[i % len(images)].setAutoDraw(False)
    win.flip(True)
    time_after = time.clock()
    exp_log.append([IMAGE_APPEARANCE, time_before - start_time,
                    time_after - start_time])

    if i == NUM_TRIALS - 1:
        time.sleep(1)

        end_text.setAutoDraw(True)  # The initial screen
        win.flip(True)

        while not defaultKeyboard.getKeys(keyList=["escape"]):
            pass

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        break

# write the final documentation csv file
date = str(datetime.datetime.now().strftime("%y%b%d_%H_%M_%S"))
with open('./results_' + date + '.csv',
          'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Trial type", "Start Time(Sec)", "End Time(Sec)"])
    for log_entry in exp_log:
        writer.writerow(log_entry)

win.close()
core.quit()
