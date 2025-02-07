from browser import window, alert

audioContext = None
envelop = None

def fade_out(osc, envelop):
    t = audioContext.currentTime
    envelop.gain.setTargetAtTime(0, t, 0.02)
    osc.stop(t + 0.08)


def playTone(freq,
             time=0,
             length=None,
             gain_value=1,
             wave=None,
             type="sine"):
    global audioContext, envelop
    #alert('play tone')

    if audioContext is None:
        audioContext = window.AudioContext.new()

    envelop = audioContext.createGain()
    envelop.connect(audioContext.destination)
    envelop.gain.value = gain_value

    osc = audioContext.createOscillator()
    t = audioContext.currentTime + time

    envelop.gain.setValueAtTime(0, t)
    attackTime = 0.1
    envelop.gain.linearRampToValueAtTime(gain_value, t + attackTime)
    if length is not None:
        releaseTime = length / 10
        envelop.gain.linearRampToValueAtTime(0, t + length - releaseTime)

    osc.connect(envelop)

    if wave is not None:
        osc.setPeriodicWave(wave)
    else:
        osc.type = type

    osc.frequency.value = freq
    #alert(f'ready to start')
    if time == 0:
        osc.start()
    else:
        currentTime = audioContext.currentTime
        osc.start(currentTime + time)
        if length is not None:
            osc.stop(currentTime + time + length)

    return osc, envelop