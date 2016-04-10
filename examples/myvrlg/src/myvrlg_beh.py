def myvrlg_beh(rx_hs, tx_hs):
    '''|
    | Specify the behavior, describe data processing; there is no notion
    | of clock. Access the in/out interfaces via get() and append()
    | methods. The "myvrlg_beh" function does not return values.
    |________'''

    if rx_hs.hasPacket():
        data = rx_hs.get()
        tx_hs.append(data)

