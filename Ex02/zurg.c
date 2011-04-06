/* Last changed Time-stamp: <2009-03-31 14:40:36 ivo> */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX2(A,B)  ((A)>(B)?(A):(B))

static char rcsid[] = "$Id:  $";

enum toys {
  Buzz,
  Woody,
  Rex,
  Hamm,
  xtof,
  ivo,
  Speedy,
  toynum
};


enum light {
  left,
  right
};

char *names[] = { "Buzz", "Woody", "Rex", "Hamm", "xtof", "ivo", "Speedy" };
int costs[] = {5, 10, 20, 25, 30, 7, 2};


struct state {
  int cost;
  enum light lightpos;
  unsigned int where;  /* bitvector encoding where each toy is */
  enum toys history[3*toynum];
  int histlen;
};

struct move {
  enum toys first, second;
  int cost;
};

struct move *moves(struct state *s);
struct state move_it(struct state *s, struct move *m);

static int maxcost = INT_MAX;

int solve(struct state *s) {
  struct move *mvs, *m;
  int best, curr;
  struct state bstate;

  if (s->where +1 == 1 << toynum) {
    return 0;
  }
  mvs = moves(s);
  best = INT_MAX;
  curr = s->cost;
  for (m=mvs; m->cost>0; m++) {
    int cost;
    struct state test, gstate;
    if (curr + m->cost > maxcost) continue;
    gstate = test = move_it(s, m);
    if (greedy(&gstate) > maxcost) continue;
    cost = m->cost + solve(&test);
    if (best>cost) {
      best = cost;
      bstate = test;
    }
    if (maxcost < best + curr) maxcost = best + curr;
  }
  free(mvs);
  *s = bstate;
  return best;
}

struct move *moves(struct state *s) {
  struct move *m;
  int num=0;
  enum toys i,j;

  m = calloc(sizeof(struct move),(toynum*(toynum+1))/2);

  if (s->lightpos==left) {
    for (i=0; i<toynum; i++) {
      if (s->where & 1 << i) continue;
      for (j=i+1; j<toynum; j++) {
	if (s->where & 1 << j) continue;
	m[num].first = i;
	m[num].second = j;
	m[num++].cost = MAX2(costs[i],costs[j]);
      }
    }
  } else {
    for (i=0; i<toynum; i++) {
      if (s->where & 1 << i) {
	m[num].first = m[num].second = i;
	m[num++].cost = costs[i];
      }
    }
  }
  return m;
}

struct state move_it(struct state *s, struct move *m) {
  struct state new;

  new = *s;
  new.where ^= 1 << m->first;
  new.history[new.histlen++] = m->first;
  new.cost += m->cost;
  if (s->lightpos == left) {
    new.where ^= 1 << m->second;
    new.history[new.histlen++] = m->second;
    new.lightpos = right;
  } else
    new.lightpos = left;
  return new;
}

int greedy(struct state *s) {
  struct move *mvs, *m, *best;

  while (s->where +1 != 1 << toynum) {

    mvs = moves(s);
    best = mvs;
    for (m=mvs+1; m->cost>0; m++) {
      if (m->cost < best->cost)
	best = m;
    }
    
    *s = move_it(s, best);
    free(mvs);
  }
  return s->cost;
}

void printSolution(struct state *s) {
  int i;
  
  printf("Solution with cost\t %2d:\n", s->cost);
  printf("%-5s, %-5s cross the bridge\t(cost %2d)\n",
	 names[s->history[0]], names[s->history[1]],
	 MAX2(costs[s->history[0]],costs[s->history[1]]));
  for (i=2; i<s->histlen; i+=3) {
    printf("%-5s\t     goes back\t\t(cost %2d)\n",
	   names[s->history[i]], costs[s->history[i]]);
  printf("%-5s, %-5s cross the bridge\t(cost %2d)\n",
	 names[s->history[i+1]], names[s->history[i+2]],
	 MAX2(costs[s->history[i+1]],costs[s->history[i+2]]));
  }
  printf("\n");
}

int DP(void) {
  



}

int main() {
  struct state state, gstate;

  state.lightpos=left;
  state.where=0;
  state.histlen=0;
  state.cost=0;

  gstate = state;

  printf("Greedy ");
  maxcost = greedy(&gstate);
  printSolution(&gstate);

  printf("Optimal ");
  solve(&state);
  printSolution(&state);

  exit(EXIT_SUCCESS);
}
