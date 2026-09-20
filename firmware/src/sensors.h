#pragma once
#include "config.h"

void sensors_init();
void sensors_power_on();
void sensors_power_off();
void sensors_read_all(PayloadType0x01* payload);
