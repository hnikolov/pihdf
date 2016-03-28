def hsd_custom_beh(rx_port_flds, tx_port_flds):
    '''|
    | Specify the behavior, describe data processing; there is no notion
    | of clock. Access the in/out interfaces via get() and append()
    | methods. The "hsd_custom_beh" function does not return values.
    |________'''

    if rx_port_flds.hasPacket():
        data = rx_port_flds.get()
        tx_port_flds.append(data)

