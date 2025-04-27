#pragma once
#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "MS5837.h"

namespace esphome {
namespace ms5837 {

class MS5837Component : public PollingComponent {
 public:
  explicit MS5837Component(uint32_t update_interval = 60000)
    : PollingComponent(update_interval) {}

  void setup() override {
    if (!this->sensor_.init()) {
      ESP_LOGE("ms5837", "No se pudo inicializar el MS5837");
    }
  }

  void update() override {
    this->sensor_.read();
    if (this->temperature_sensor_) {
      this->temperature_sensor_->publish_state(this->sensor_.temperature());
    }
    if (this->pressure_sensor_) {
      this->pressure_sensor_->publish_state(this->sensor_.pressure());
    }
  }

  void set_temperature_sensor(sensor::Sensor *sensor) {
    this->temperature_sensor_ = sensor;
  }
  void set_pressure_sensor(sensor::Sensor *sensor) {
    this->pressure_sensor_ = sensor;
  }

 protected:
  MS5837 sensor_;
  sensor::Sensor *temperature_sensor_{nullptr};
  sensor::Sensor *pressure_sensor_{nullptr};
};

}  // namespace ms5837
}  // namespace esphome
