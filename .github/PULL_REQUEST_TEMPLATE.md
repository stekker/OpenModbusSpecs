## Description

<!-- Describe the device profile you're adding or the changes you're making -->

**Note:** New device profiles should be added to `registry/contrib/` and will be promoted to `registry/stable/` after validation.

## Device Information

- **Manufacturer:**
- **Model:**
- **Protocol:** <!-- modbus_tcp, modbus_rtu, or modbus_udp -->
- **Documentation URL:** <!-- Link to official datasheet/manual -->

## Checklist

- [ ] I have validated the YAML file using `python3 tools/validate.py`
- [ ] The device profile includes all required fields (version, device, registers)
- [ ] Register addresses and data types are verified against official documentation
- [ ] I have tested this profile against real hardware (if applicable)
- [ ] Descriptive names follow snake_case convention
- [ ] Units are specified correctly (SI units preferred)
- [ ] Byte order is documented correctly

## Additional Context

<!-- Add any additional information about the device or special considerations -->
