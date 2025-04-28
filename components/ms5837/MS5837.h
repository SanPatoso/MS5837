// components/ms5837/MS5837.h
#pragma once

#include "esphome.h"
#include "MS5837_lib.h"  // la librería original, renombrada

namespace esphome {
namespace ms5837 {

class MS5837 : public PollingComponent, public i2c::I2CDevice public MS5837_lib {
 public:
  Sensor *temperature_sensor_{nullptr};
  Sensor *pressure_sensor_{nullptr};

  // Constructor: el intervalo por defecto lo toma de tu YAML
  MS5837(uint32_t update_interval) : PollingComponent(update_interval) {}

  // Estas son las funciones que tu sensor.py invoca
  void set_temperature_sensor(Sensor *sensor) { temperature_sensor_ = sensor; }
  void set_pressure_sensor(Sensor *sensor) { pressure_sensor_ = sensor; }

  // Se llama 1 vez al arrancar
  void setup() override {
    // Inicializa el bus I2C y la librería
    this->MS5837_lib::begin(this->get_wire());
  }

  // Se llama cada update_interval
  void update() override {
    // Lee del sensor
    this->MS5837_lib::read();
    float temp = this->MS5837_lib::temperature();
    float pres = this->MS5837_lib::pressure();

    // Publica los estados
    if (temperature_sensor_)
      temperature_sensor_->publish_state(temp);
    if (pressure_sensor_)
      pressure_sensor_->publish_state(pres);
  }
};

}  // namespace ms5837
}  // namespace esphome
