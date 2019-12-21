
#include <stdio.h>
#include <stdlib.h>

#include "common.h"


void failure(char *str, char* filename, int line) {
  fprintf(stderr, "\nERROR: %s at \"%s:%d\"\n", str, filename, line);
  exit(-1);
}

void dot_exec(char *command,  char* filename_base) {
  int pid = fork();
  if(pid) {
    waitpid(pid, NULL, 0);
    return;
  }
  char dot_filename[64], out_filename[64];
  sprintf(dot_filename, "%s.dot", filename_base);
  sprintf(out_filename, "%s.png", filename_base);
  execlp(command, command, "-Tpng", dot_filename, "-o", out_filename, NULL);
}
