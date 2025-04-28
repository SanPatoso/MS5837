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

# Usa el namespace global: la clase C++ es MS5837 en global (no está en un namespace propio) :contentReference[oaicite:0]{index=0}
MS5837Component = cg.esphome_ns.class_(
    'MS5837', cg.PollingComponent, i2c.I2CDevice
)

# Schema para los dos sensores
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

CONFIG_SCHEMA = cv.Schema({
    # Obligatorio el id para poder instanciar la clase C++
    cv.GenerateID(): cv.declare_id(MS5837Component),
    # Intervalo de lectura (por defecto 60s si no se indica)
    cv.Optional(CONF_UPDATE_INTERVAL, default='60s'): cv.update_interval,
    # Sub-sensores opcionales
    cv.Optional(CONF_TEMPERATURE): MS5837_TEMPERATURE_SCHEMA,
    cv.Optional(CONF_PRESSURE): MS5837_PRESSURE_SCHEMA,
}).extend(
    cv.COMPONENT_SCHEMA
).extend(
    # Dirección I2C fija del MS5837
    i2c.i2c_device_schema(address=0x76)
)

async def to_code(config):
    # Creamos la instancia C++
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_UPDATE_INTERVAL])
    # Registro como componente y dispositivo I2C
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    # Si hay petición de temperatura, creamos y enlazamos
    if CONF_TEMPERATURE in config:
        temp = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(temp))

    # Si hay petición de presión, creamos y enlazamos
    if CONF_PRESSURE in config:
        pres = await sensor.new_sensor(config[CONF_PRESSURE])
        cg.add(var.set_pressure_sensor(pres))
