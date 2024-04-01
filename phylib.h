#ifndef _phylib_h
#define _phylib_h

// Constants
#define PHYLIB_BALL_RADIUS (28.5) // mm
#define PHYLIB_BALL_DIAMETER (2*PHYLIB_BALL_RADIUS)
#define PHYLIB_HOLE_RADIUS (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0) // mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH/2.0) // mm
#define PHYLIB_SIM_RATE (0.0001) // s
#define PHYLIB_VEL_EPSILON (0.01) // mm/s
#define PHYLIB_DRAG (150.0) // mm/s^2
#define PHYLIB_MAX_TIME (600) // s
#define PHYLIB_MAX_OBJECTS (26)

// Polymorphic Object types defined as enum 
typedef enum {
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;

//Class representing a vector in 2 dimensions 
typedef struct {
    double x;
    double y;
} phylib_coord;

// Child classes representing objects on the table 
typedef struct {
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

/* A ball that is rolling, it has a number (cue ball is 0) and a position on the table. 
Also has a velocity and a (negative) acceleration (due to friction) */
typedef struct {
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
} phylib_rolling_ball;

// One of the 6 holes on the table. It has a position 
typedef struct {
    phylib_coord pos;
} phylib_hole;

// Horizontal Cushion 
typedef struct {
    double y;
} phylib_hcushion;

// Vertical Cushion 
typedef struct {
    double x;
} phylib_vcushion;

// Polymorphic Parent Class of objects on the table

// C union that can store any of the above classes/structure in the same space
typedef union {
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

/* this union can store an object of any of the above classes/structures, it cannot identify
what the class of the object is, so we need another structure for that */

typedef struct {
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

// The table 
typedef struct {
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

phylib_object *phylib_new_still_ball( unsigned char number,
phylib_coord *pos );

phylib_object *phylib_new_rolling_ball( unsigned char number,
phylib_coord *pos,
phylib_coord *vel,
phylib_coord *acc );

phylib_object *phylib_new_hole( phylib_coord *pos );
phylib_object *phylib_new_hcushion( double y );
phylib_object *phylib_new_vcushion( double x );

phylib_table *phylib_new_table( void );

void phylib_copy_object( phylib_object **dest, phylib_object **src );

phylib_table *phylib_copy_table( phylib_table *table );

void phylib_add_object( phylib_table *table, phylib_object *object );

void phylib_free_table( phylib_table *table );

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 );

double phylib_length( phylib_coord c );

double phylib_dot_product(phylib_coord a, phylib_coord b);

double phylib_distance( phylib_object *obj1, phylib_object *obj2 );

void phylib_roll(phylib_object *new, phylib_object *old, double time);

unsigned char phylib_stopped( phylib_object *object);

void phylib_bounce(phylib_object **a, phylib_object **b);

unsigned char phylib_rolling( phylib_table *t );

phylib_table *phylib_segment( phylib_table *table );

char *phylib_object_string( phylib_object *object );

#endif
