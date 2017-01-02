def psched_beh(rx_port, tx_port, sequence, rx, tx, SEQ_RX, SEQ_RX_PORT, SEQ_TX, SEQ_TX_PORT):
    '''|
    | Specify the behavior, describe data processing; there is no notion
    | of clock. Access the in/out interfaces via get() and append()
    | methods. The "psched_beh" function does not return values.
    |________'''

    if rx_port.hasPacket():
        data = rx_port.get()
        tx_port.append(data)

    if rx.hasPacket():
        data = rx.get()
        tx.append(data)
        
