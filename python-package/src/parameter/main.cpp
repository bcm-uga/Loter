#include <iostream>

#include "parameter.h"

/****************
 * TEST FILE
*:**************/
struct Test: Parameter<Test> {
  int a;
  int b;
  float f;
  std::string s;

  Test() {
    a = 1;
    DECLARE_FIELD(a, Test);
    DECLARE_FIELD(b, Test);
    DECLARE_FIELD(f, Test);
    DECLARE_FIELD(s, Test);
  };
};

int main() {
  Test t;

  t.Set("b", "3.1");
  t.f = 3.2f;
  t.Set("s", "test");

  std::cout << t.a << std::endl;
  std::cout << t.b << std::endl;
  std::cout << t.f << std::endl;
  std::cout << t.s << std::endl;
  std::cout << t.Get("b") << std::endl;

  return 0;
}
