def format_wx_packet(callsign, temperature_c, pressure_hpa):
    """
    Formats proper APRS weather packet.
    """

    latitude = "1156.87N"
    longitude = "07949.25E"

    # Convert temperature to Fahrenheit
    temp_f = round((temperature_c * 9 / 5) + 32)

    # Pressure in tenths of millibars
    pressure_tenths = int(pressure_hpa * 10)

    packet = (
        f"{callsign}>APRS,TCPIP*:!"
        f"{latitude}/{longitude}_"
        f".../...g..."      # Wind placeholders
        f"t{temp_f:03d}"
        f"b{pressure_tenths:05d}"
        f" Station WX Pi"
    )

    return packet
