/* Last changed Time-stamp: <2009-03-17 17:15:08 ivo> */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char rcsid[] = "$Id:  $";

#define DELIM " ^°!\"§$%&/()=?´`<>,;.:-_#'+*~\n\t\v\r\f\b\a"

#define HASHBITS 16
#define HASHSIZE (((unsigned) 1<<HASHBITS)-1)

unsigned long collisions=0;

typedef struct _hash_entry {
  char *word;
  int count;
} hash_entry;

hash_entry hashtab[HASHSIZE+1];

/* stolen from perl source */
char coeff[] = {
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1,
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1,
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1,
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1,
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1,
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1,
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1,
                61,59,53,47,43,41,37,31,29,23,17,13,11,7,3,1};

/* key must not be longer than 128 */
inline unsigned hash_f(char *x)
{ 
  register char *s;
  register int i;
  register int hash;

  s = x;
  for (i=0,    hash = 0;
       /* while */ *s;
       s++,           i++ , hash *= 5 ) {
    hash += *s * coeff[i];
  }
  /* printf("%7d\t", hash); */
  return ((hash) & (HASHSIZE)); /* modulo HASHSIZE for normalization */
}

int hash_add (char *x)   /* returns 1 if x already was in the hash */ 
{
  unsigned int hashval;
  
  hashval=hash_f(x);
  while (hashtab[hashval].word){
    if (strcmp(x,hashtab[hashval].word)==0) {
      hashtab[hashval].count++;;
      return 1;
    }
    hashval = ((hashval+1) & (HASHSIZE));
    collisions++;
  }
  hashtab[hashval].word = strdup(x);
  hashtab[hashval].count = 1;
  return 0;
}

int main(int argc, char *argv[]) {
  char *line;
  int i;
  size_t read = 0;
  while ((read = getline(&line, &read, stdin)) != -1) {
      char *word;
      /* split line into words and add to hash */
      word = strtok(line, DELIM);
      while (word) {
	hash_add(word);
	word = strtok(NULL, DELIM);
      }
  }
  
  /* output */
  for (i=0; i<=HASHSIZE; i++) {
    if (hashtab[i].word) {
      printf("%12s: %d\n", hashtab[i].word, hashtab[i].count);
      free(hashtab[i].word);
    }
  }
  free(line);
  exit(EXIT_SUCCESS);
}
