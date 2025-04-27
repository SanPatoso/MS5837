import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID, CONF_UPDATE_INTERVAL

DEPENDENCIES = ['i2c']

# Creamos el espacio de nombres y referenciamos la clase C++
ms5837_ns = cg.esphome_ns.namespace('ms5837')
MS5837Component = ms5837_ns.class_(
    'MS5837Component', cg.PollingComponent)

# Definimos la configuración válida en YAML
CONF_TEMPERATURE = 'temperature'
CONF_PRESSURE = 'pressure'

MS5837_TEMPERATURE_SCHEMA = sensor.sensor_schema(
    unit_of_measurement='°C',
    device_class=sensor.DEVICE_CLASS_TEMPERATURE,
    accuracy_decimals=2,
)
MS5837_PRESSURE_SCHEMA = sensor.sensor_schema(
    unit_of_measurement='hPa',
    device_class=sensor.DEVICE_CLASS_PRESSURE,
    accuracy_decimals=2,
)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MS5837Component),
    cv.Optional(CONF_UPDATE_INTERVAL): cv.update_interval,
    cv.Optional(CONF_TEMPERATURE): MS5837_TEMPERATURE_SCHEMA,
    cv.Optional(CONF_PRESSURE): MS5837_PRESSURE_SCHEMA,
}).extend(cv.COMPONENT_SCHEMA)

# Función que traduce la configuración a llamadas de generación de código
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], config.get(CONF_UPDATE_INTERVAL))
    await cg.register_component(var, config)

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))
    if CONF_PRESSURE in config:
        sens = await sensor.new_sensor(config[CONF_PRESSURE])
        cg.add(var.set_pressure_sensor(sens))

