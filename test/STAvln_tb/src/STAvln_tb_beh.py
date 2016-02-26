def STAvln_tb_beh(rx16, tx16, rx32, tx32, rx64, tx64, ipg_rx16, ipg_tx16):
    '''|
    | Specify the behavior, describe data processing; there is no notion
    | of clock. Access the in/out interfaces via get() and append()
    | methods. The "STAvln_tb_beh" function does not return values.
    |________'''

    if rx16.hasPacket():
        data16 = rx16.get()
        tx16.append(data16)

    if rx32.hasPacket():
        data32 = rx32.get()
        tx32.append(data32)

    if rx64.hasPacket():
        data64 = rx64.get()
        tx64.append(data64)


