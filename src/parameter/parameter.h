#ifndef PARAMETER_H
#define PARAMETER_H

#include <string>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <sstream>
#include <map>

template <typename STRUC>
struct Field {
  virtual void set(STRUC& s, const std::string& value) const = 0;
  virtual std::string get(STRUC& s) const = 0;
  virtual ~Field() = 0;
};

template <typename STRUC>
Field<STRUC>::~Field() {}

template <typename STRUC, typename T>
struct FieldImpl: public Field<STRUC> {
  typedef T STRUC::* MemberPtr;

  FieldImpl(MemberPtr memberPtr) {
    memberPtr_ = memberPtr;
  }

  ~FieldImpl() {}

  virtual void set(STRUC& s, const std::string& value) const {
    char c;
    T tmp;
    std::istringstream iss(value);
    iss >> tmp;

    if(iss.fail()) {
      iss.clear();
      throw std::runtime_error(std::string("Unable to convert " + value));
    }

    s.*memberPtr_ = tmp;

    if(iss.get(c)) {
      std::cerr << "Convert " + value + " to " << s.*memberPtr_ << std::endl;
    }
  }

  virtual std::string get(STRUC& s) const {
    std::ostringstream stm;

    stm << s.*memberPtr_;
    return stm.str();
  }

 private:
  MemberPtr memberPtr_;
};

template <typename STRUC>
class FieldMap {
 private:
  typedef std::map<std::string, Field<STRUC>*> FieldMapType;
  FieldMapType fieldmap_;

 public:
  ~FieldMap() {
    for(typename FieldMapType::const_iterator it = fieldmap_.begin(); it != fieldmap_.end(); ++it) {
      delete it->second;
    }
  }

  template <typename T>
  void bind(const std::string& key, T (STRUC::*member)) {
    fieldmap_[key] = new FieldImpl<STRUC, T>(member);
  }

  void Set(STRUC& s, const std::string& key, const std::string& value) {
    typename FieldMapType::const_iterator it = fieldmap_.find(key);

    if(it == fieldmap_.end()) {
      throw std::runtime_error(std::string("No field named ") + key);
    }
    it->second->set(s, value);
  }

  std::string Get(STRUC& s, const std::string& key) {
    typename FieldMapType::const_iterator it = fieldmap_.find(key);

    if(it == fieldmap_.end()) {
      throw std::runtime_error(std::string("No field named ") + key);
    }

    return it->second->get(s);
  }
};


template <typename STRUC>
struct Parameter {
 public:
  virtual void Set(const std::string& key, const std::string& value) {
    this->fm_.Set(dynamic_cast<STRUC&>(*this), key, value);
  }

  virtual std::string Get(const std::string& key) {
    return this->fm_.Get(dynamic_cast<STRUC&>(*this), key);
  }

  virtual ~Parameter() = 0;

 protected:
  FieldMap<STRUC> fm_;
};

template <typename STRUC>
Parameter<STRUC>::~Parameter() {}

#define DECLARE_FIELD(FieldName, STRUC) this->fm_.bind(#FieldName, &STRUC::FieldName)
#endif
