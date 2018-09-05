#ifndef DATA_H
#define DATA_H

#include <string>

#include "../Eigen/Core"
#include "../utils/matrixtype.hpp"

template <typename Derived>
class DataInput {
public:
  Derived* G;

  DataInput(Derived& G) {
    this->G = &G;
  }

};

class DataException {
public:
  explicit DataException(const std::string& msg) : mesg_(msg) {}
  std::string mesg_;
};

#endif
