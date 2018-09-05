#ifndef ERRORHANDLER_H
#define ERRORHANDLER_H

typedef void (*ErrorHandlerFn) (const char* error_message,
                                void* user_data);

typedef struct ErrorHandler {
  ErrorHandlerFn eh;
  void* user_data;
} ErrorHandler;

void basic_eh(const char* error_message,
              void* user_data);

#endif
