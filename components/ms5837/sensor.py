# components/ms5837/sensor.py
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ID,
    CONF_UPDATE_INTERVAL,
    CONF_TEMPERATURE,
    CONF_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_PRESSURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_HECTOPASCAL,
)

DEPENDENCIES = ['i2c']

# Namespace de nuestro componente
ms5837_ns = cg.esphome_ns.namespace('ms5837')
MS5837Component = ms5837_ns.class_('MS5837', cg.PollingComponent, i2c.I2CDevice
)

# Esquemas de sub-sensores
MS5837_TEMPERATURE_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_CELSIUS,
    device_class=DEVICE_CLASS_TEMPERATURE,
    state_class=STATE_CLASS_MEASUREMENT,
    accuracy_decimals=2,
)
MS5837_PRESSURE_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_HECTOPASCAL,
    device_class=DEVICE_CLASS_PRESSURE,
    state_class=STATE_CLASS_MEASUREMENT,
    accuracy_decimals=2,
)

# Configuración que acepta YAML\
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MS5837Component),
    cv.Optional(CONF_UPDATE_INTERVAL): cv.update_interval,
    cv.Optional(CONF_TEMPERATURE): MS5837_TEMPERATURE_SCHEMA,
    cv.Optional(CONF_PRESSURE): MS5837_PRESSURE_SCHEMA,
}).extend(cv.COMPONENT_SCHEMA).extend(
    # Registrar como dispositivo I2C en la dirección 0x76
    i2c.i2c_device_schema(address=0x76)
)

# Generación de código\async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], config.get(CONF_UPDATE_INTERVAL))
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_TEMPERATURE in config:
        temp = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(temp))
    if CONF_PRESSURE in config:
        pres = await sensor.new_sensor(config[CONF_PRESSURE])
        cg.add(var.set_pressure_sensor(pres))
