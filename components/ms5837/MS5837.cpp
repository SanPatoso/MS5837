#include "MS5837.h"
#include "MS5837_lib.h"
#include "esphome/core/log.h"

namespace esphome {
namespace ms5837 {

static const char *TAG = "ms5837";

// Si no definiste el constructor inline en el header, podrías hacerlo aquí:
// MS5837::MS5837(uint32_t update_interval)
//   : PollingComponent(update_interval), i2c::I2CDevice(0x76) {}

void MS5837::setup() {
  ESP_LOGCONFIG(TAG, "Inicializando MS5837");
  // Llama a init o begin de la librería original sobre el bus I2C
  if (!this->MS5837_lib::init(this->get_wire())) {
    ESP_LOGE(TAG, "No se pudo inicializar el sensor MS5837");
  }
}

void MS5837::update() {
  ESP_LOGD(TAG, "Leyendo MS5837");
  // Lee los datos
  if (!this->MS5837_lib::read()) {
    ESP_LOGW(TAG, "Fallo en lectura del MS5837");
    return;
  }
  // Recupera temperatura y presión
  float temp = this->MS5837_lib::temperature();
  float pres = this->MS5837_lib::pressure();  // en mbar == hPa

  // Publica en ESPHome
  if (this->temperature_sensor_)
    this->temperature_sensor_->publish_state(temp);
  if (this->pressure_sensor_)
    this->pressure_sensor_->publish_state(pres);
}

}  // namespace ms5837
}  // namespace esphome
