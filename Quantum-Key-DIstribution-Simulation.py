import numpy as np

def sendsignal(nbits):
    sender_bases = np.random.randint(0, 2, nbits, dtype=np.uint8)
    sender_states = np.random.randint(0, 2, nbits, dtype=np.uint8)+2*sender_bases
    return sender_bases, sender_states

def eavesdrop(eavesdropping, sender_bases, sender_states, nbits):
    if eavesdropping:
        eavesdropper_bases = np.random.randint(0, 2, nbits, dtype=np.uint8)
        if len(sender_bases)!=nbits:
            raise ValueError("eavesdropper_bases is different in length to sender_bases")
        eavesdropper_states = np.where(eavesdropper_bases==sender_bases, sender_states, np.random.randint(2*eavesdropper_bases, 2+2*eavesdropper_bases, dtype=np.uint8))
        return eavesdropper_bases, eavesdropper_states
    return sender_bases, sender_states

def receive_signal(eavesdropper_bases, eavesdropper_states, nbits):
    receiver_bases = np.random.randint(0, 2, nbits, dtype=np.uint8)
    if len(eavesdropper_bases)!=nbits:
        raise ValueError("receiver_bases is different in length to eavesdropper_bases")
    receiver_states = np.where(receiver_bases==eavesdropper_bases, eavesdropper_states, np.random.randint(2*receiver_bases, 2+2*receiver_bases, dtype=np.uint8))
    return receiver_bases, receiver_states

def recognise_error(sender_bases, sender_states, receiver_bases, receiver_states):
    errors = 0
    for i in range(len(sender_bases)):
        if sender_bases[i]==receiver_bases[i] and sender_states[i]!=receiver_states[i]:
            errors+=1
    if errors>0:
        print("Eavesdropper detected: ", errors, " errors")
    return errors

def generate_key(errors, sender_bases, sender_states, receiver_bases, receiver_states, error_bound):
    if errors>error_bound:
        print("No key generated - error count exceeds threshold")
        return None, None, None
    sender_key = np.extract(sender_bases==receiver_bases, sender_states)
    receiver_key = np.extract(sender_bases==receiver_bases, receiver_states)
    if np.array_equal(sender_key, receiver_key):
        key = sender_key
    else:
        key=None
    if sender_key.size == 0 or receiver_key.size == 0:
        print("No key established - no matching bases or error threshold too high")
    return sender_key, receiver_key, key
