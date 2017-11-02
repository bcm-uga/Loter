#include "errorhandler.h"
#include <iostream>

void basic_eh(const char* error_message,
              void* user_data) {
  std::cout<<"eh : "<<error_message<<std::endl;
}
