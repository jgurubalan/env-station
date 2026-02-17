# Environmental Data Collection System

Modular environmental data collection system designed for:

- Raspberry Pi (current implementation)
- Future Arduino-based data acquisition
- APRS Weather telemetry integration
- Web dashboard visualization

## Design Principles

- Each sensor operates independently
- Clean structured logging (CSV for history)
- JSON file for latest reading
- Hardware layer separated from transmission layer

## Current Sensors

- BMP280 (Temperature + Pressure)

## Future Expansion

- Humidity sensor
- Rain gauge
- Wind speed/direction
- External microcontroller data input
