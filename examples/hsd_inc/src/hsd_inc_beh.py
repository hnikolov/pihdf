def hsd_inc_beh(rxd, txd):
    '''|
    | Specify the behavior, describe data processing; there is no notion
    | of clock. Access the in/out interfaces via get() and append()
    | methods. The "hsd_inc_beh" function does not return values.
    |________'''

    if rxd.hasPacket():
        data = rxd.get() + 1
        txd.append(data)

