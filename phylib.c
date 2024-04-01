#include "phylib.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


phylib_object *phylib_new_still_ball( unsigned char number,phylib_coord *pos ) {
	// allocating memory for the phylib_object
	phylib_object *newObject = (phylib_object *)malloc( sizeof(phylib_object));

	if (newObject == NULL) {
		return NULL;
	}

	//set the type of the object to the phylib still ball
	newObject->type = PHYLIB_STILL_BALL;

	// set the values for the phylib_still_ball structure within the phy_lib object 
	newObject->obj.still_ball.number = number;
	newObject->obj.still_ball.pos = *pos;

	// returning the phylib_object
	return newObject;
}

phylib_object *phylib_new_rolling_ball( unsigned char number,phylib_coord *pos,phylib_coord *vel,phylib_coord *acc ) {
	// allocating memory for the phylib object 
	phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

	if (newObject == NULL) {
		return NULL;
	}
	// set the object to the rolling ball 
	newObject->type = PHYLIB_ROLLING_BALL;
	// set the values for the phylib_rolling_ball within the phy_lib object 
	newObject->obj.rolling_ball.number = number;
	newObject->obj.rolling_ball.pos = *pos;
	newObject->obj.rolling_ball.vel = *vel;
	newObject->obj.rolling_ball.acc = *acc;

	return newObject;
}

phylib_object *phylib_new_hole( phylib_coord *pos ) {

	phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

	if (newObject == NULL) {
		return NULL;
	}
	// set the type of the object to the PHYLIB_HOLE
	newObject->type = PHYLIB_HOLE;
	// set the values for the phylib_hole structure within the phylib_object 
	newObject->obj.hole.pos = *pos;

	return newObject;
}

phylib_object *phylib_new_hcushion( double y ) {
  
	phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

	if (newObject == NULL) {
		return NULL;
	}

	// set the type of the object to the PHYLIB_HCUSHION
	newObject->type = PHYLIB_HCUSHION;
	// set the values for the phylib_hcushion structure within the phylib_object 
	newObject->obj.hcushion.y = y;

	return newObject;
}

phylib_object *phylib_new_vcushion( double x ) {
  
	phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

	if (newObject == NULL) {
		return NULL;
	}
	// set the type of the object to the PHYLIB_VCUSHION
	newObject->type = PHYLIB_VCUSHION;
	// set the values for the phylib_vcushion structure within the phylib_object 
	newObject->obj.vcushion.x = x;

	return newObject;
}

phylib_table *phylib_new_table( void ) {

	phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));

	if (newTable == NULL) {
		return NULL;
	}

	newTable->time = 0.0;

	for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
		newTable->object[i] = NULL;
	}
	// Assigning values to the array elements 
	newTable->object[0] = phylib_new_hcushion(0.0); // Horizontal Cushion at y=0.0
	newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH); // Horizontal Cushion at y=PHYLIB_TABLE_LENGTH
	newTable->object[2] = phylib_new_vcushion(0.0); // Vertical Cushion at x=0.0
	newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH); // Vertical cushion at x=PHYLIB_TABLE_WIDTH

	//Setting the holes
	newTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0}); // Top left hole 
	newTable->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH}); // Top right hole 
	newTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH}); // Bottom left hole 
	newTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0}); // Bottom right hole 
	newTable->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH}); // middle left hole
	newTable->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH}); // middle right hole 

	// set the remaining pointers to null 
	for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
		newTable->object[i] = NULL;
	}
	return newTable; 
	}

	void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
	if (*src == NULL) {
		*dest = NULL;
		return;
	}
	else {
		// allocate memory for the phylib object and save the it to dest
		*dest = (phylib_object *)malloc(sizeof(phylib_object));
		// checking if allocation works 
		if (*dest != NULL) {
		memcpy(*dest, *src, sizeof(phylib_object));
		}
	}
}

phylib_table *phylib_copy_table( phylib_table *table ) {
  
	if (table == NULL) {
		return NULL; 
	}
	else {
		// allocate memory for the phylib table 
		phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
		if (newTable == NULL) {
		return NULL;
		}
		newTable->time = table->time;
		// copy each object 
		for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
		phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
		}
		return newTable;
	}
	}

	void phylib_add_object( phylib_table *table, phylib_object *object ) {
	if (table != NULL & object != NULL) {
		// iterate through the objects on the table 
		for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
		if (table->object[i] == NULL) {
			// if a slot is empty add object to the table 
			table->object[i] = object;
			break;
		}
		}
	}
}

void phylib_free_table( phylib_table *table ) {
	if(table != NULL) {
		// iterating through the object array  
		for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
		if(table->object[i] != NULL) {
			free(table->object[i]);
			// setting the freed pointer to null
			table->object[i] = NULL; 
		}
		}
		free(table);
		table = NULL;
	}
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {
	phylib_coord result;
	result.x = c1.x - c2.x;
	result.y = c1.y - c2.y;
	return result;
}

double phylib_length( phylib_coord c ) {
	return sqrt(c.x * c.x + c.y * c.y);
}

double phylib_dot_product( phylib_coord a, phylib_coord b ) {
  	return (a.x * b.x) + (a.y * b.y);

}

double phylib_distance(phylib_object *obj1, phylib_object *obj2 ){
	// check if obj is a rolling ball 
	if (obj1->type != PHYLIB_ROLLING_BALL){
		return -1.0;
	}
	
	double distance = -1.0;
	phylib_coord pos2; // position of obj2
	// determine the position based on its type 
	if (obj2->type == PHYLIB_STILL_BALL) {
		pos2 = obj2->obj.still_ball.pos;
		phylib_coord diff = phylib_sub(obj1->obj.still_ball.pos, pos2);
		double center_distance = phylib_length(diff);
		distance = center_distance - PHYLIB_BALL_DIAMETER;
	} else if (obj2->type == PHYLIB_ROLLING_BALL) {
		pos2 = obj2->obj.rolling_ball.pos;
		phylib_coord diff = phylib_sub(obj1->obj.rolling_ball.pos, pos2);
		double center_distance = phylib_length(diff);
		distance = center_distance - PHYLIB_BALL_DIAMETER;
	} else if (obj2->type == PHYLIB_HOLE) {
		pos2 = obj2->obj.hole.pos;
		phylib_coord diff = phylib_sub(obj1->obj.rolling_ball.pos, pos2);
		double center_distance = phylib_length(diff);
		distance = center_distance - PHYLIB_HOLE_RADIUS;
	} else if (obj2->type == PHYLIB_HCUSHION) {
		pos2.y = obj2->obj.hcushion.y;
		// calculating the distance 
		distance = fabs(obj1->obj.rolling_ball.pos.y - pos2.y) - PHYLIB_BALL_RADIUS;
	} else if (obj2->type == PHYLIB_VCUSHION) {
		pos2.x = obj2->obj.vcushion.x;
		// calculate the distance
		distance = fabs(obj1->obj.rolling_ball.pos.x - pos2.x) - PHYLIB_BALL_RADIUS;
	} else {
		return -1.0;
	}
		return distance;
}

void phylib_roll(phylib_object *new, phylib_object *old, double time) {
  
	if (new == NULL || old == NULL) {
		return;
	}
	if (old->type != PHYLIB_ROLLING_BALL || new->type != PHYLIB_ROLLING_BALL) {
		return;
	}

	// updating the positions of the new object
	new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.5 * old->obj.rolling_ball.acc.x * (time * time);
	new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.5 * old->obj.rolling_ball.acc.y * (time * time);
	// updating the velocities of the new object
	new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
	new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);


	// checking for sign change and set velocioties and acceleration to zero if needed 
	if ((old->obj.rolling_ball.vel.x > 0 && new->obj.rolling_ball.vel.x < 0) || (old->obj.rolling_ball.vel.x < 0 && new->obj.rolling_ball.vel.x > 0))  {
		new->obj.rolling_ball.vel.x = 0;
		new->obj.rolling_ball.acc.x = 0;
	}
	// checking for sign change and set velocioties and acceleration to zero if needed 
	if ((old->obj.rolling_ball.vel.y > 0 && new->obj.rolling_ball.vel.y < 0) ||  (old->obj.rolling_ball.vel.y < 0 && new->obj.rolling_ball.vel.y > 0)) {
		new->obj.rolling_ball.vel.y = 0;
		new->obj.rolling_ball.acc.y = 0;
	}
}


unsigned char phylib_stopped( phylib_object *object) {

	if (object == NULL || object->type != PHYLIB_ROLLING_BALL) {
		return 0;
	}

	// calculate the speed (length of velocity)
	double speed = phylib_length(object->obj.rolling_ball.vel);

	if (speed < PHYLIB_VEL_EPSILON) {
		// convert the rolling ball to a still ball
		object->type = PHYLIB_STILL_BALL;
		object->obj.still_ball.number = object->obj.rolling_ball.number;
		object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
		object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
		// converted to still ball
		return 1;
	} else {
		return 0;
	}
}

void phylib_bounce(phylib_object **a, phylib_object **b) {

	if (*a == NULL || *b == NULL) {
		return;
	}

	// check if the object is a rolling ball
	if((*a)->type != PHYLIB_ROLLING_BALL) {
		return;
	}

	switch((*b)->type) {
		case PHYLIB_HCUSHION: {
		// reverse y velocitiy and y acceleration of a
		(*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
		(*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
		break;
		}
		case PHYLIB_VCUSHION:{
		//reverse y velocitiy and y acceleration of a
		(*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
		(*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
		break;
		}
		case PHYLIB_HOLE: {
		// free the memory and set to null
		free(*a);
		*a = NULL;
		break;
		}
		case PHYLIB_STILL_BALL: {
		phylib_coord new_roll = {0.0, 0.0};
		// goes from still ball to rolling ball 
		(*b)->type = PHYLIB_ROLLING_BALL;

		(*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
		(*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
		(*b)->obj.rolling_ball.vel = new_roll;
		(*b)->obj.rolling_ball.acc = new_roll;
		
		}
		case PHYLIB_ROLLING_BALL: {
		// compute the position of a with respect to b
		phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
		//compute the relative velocity with a respect to b
		phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
		// normal vector n
		double r_ab_length = phylib_length(r_ab);
		phylib_coord n = {r_ab.x / r_ab_length, r_ab.y / r_ab_length};

		// compute the relative velocitiy in the direction of n 
		double v_rel_n = phylib_dot_product(v_rel, n);

		// update the velocities of a and b 
		(*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
		(*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

		(*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
		(*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

		// calculate speed
		double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
		double speed_b = phylib_length((*b)->obj.rolling_ball.vel);
		
		// update accelerations if the speeds are greater than PHYLIB_VEL_EPILSON
		if (speed_a > PHYLIB_VEL_EPSILON) {
			(*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / speed_a * PHYLIB_DRAG;
			(*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / speed_a * PHYLIB_DRAG;
		}
		if (speed_b > PHYLIB_VEL_EPSILON) {
			(*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / speed_b * PHYLIB_DRAG;
			(*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / speed_b * PHYLIB_DRAG;
		}
		break;
		}
	}
}


unsigned char phylib_rolling( phylib_table *t ) {
	unsigned char count = 0;
	// iterate through the objects on the table 
	for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
		if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
		// increment the count if conditions are met 
		count++;
		}
	}
	return count;
}

phylib_table *phylib_segment(phylib_table *table) {
  
	if (phylib_rolling(table) == 0) {
		return NULL;
	}
	phylib_table *copyTable = phylib_copy_table(table);
	
	if (copyTable == NULL) {
		return NULL;
	}
	
	for (double time = PHYLIB_SIM_RATE; time < PHYLIB_MAX_TIME; time += PHYLIB_SIM_RATE) {
		for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
		if (copyTable->object[i] != NULL && copyTable->object[i]->type == PHYLIB_ROLLING_BALL) {
			phylib_roll(copyTable->object[i], table->object[i], time);
		}
		}
		for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
		// iterate over each object in the table 
		for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
			if (copyTable->object[j] == NULL || copyTable->object[i] == NULL ||  j == i) {
			continue;
			}
			// check if two rolling balls collide
			if (i != j && copyTable->object[i] != NULL && copyTable->object[i]->type == PHYLIB_ROLLING_BALL && phylib_distance(copyTable->object[i], copyTable->object[j]) < 0.0) {
			// call phylib_bounce if a collision is detected 
			phylib_bounce(&copyTable->object[i], &copyTable->object[j]);
			// update time 
			copyTable->time += time;
			return copyTable;
			}
			// check if rolling ball has stopped moving 
			if (phylib_stopped(copyTable->object[i])) {
			copyTable->time += time;
			return copyTable;
			}
		}
		}
	}
	copyTable->time += PHYLIB_MAX_TIME;
	return copyTable;
}
char *phylib_object_string( phylib_object *object ) {
	static char string[80];
	
	if (object==NULL) {
		snprintf( string, 80, "NULL;" );
		return string;
	}
	
	switch (object->type) {
		case PHYLIB_STILL_BALL:
		snprintf( string, 80,"STILL_BALL (%d,%6.1lf,%6.1lf)",object->obj.still_ball.number, object->obj.still_ball.pos.x, object->obj.still_ball.pos.y );
		break;
		
		case PHYLIB_ROLLING_BALL:snprintf( string, 80,"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",object->obj.rolling_ball.number,
		object->obj.rolling_ball.pos.x,object->obj.rolling_ball.pos.y,object->obj.rolling_ball.vel.x,object->obj.rolling_ball.vel.y,
		object->obj.rolling_ball.acc.x, object->obj.rolling_ball.acc.y );
		break;

		case PHYLIB_HOLE:
		snprintf( string, 80,"HOLE (%6.1lf,%6.1lf)",object->obj.hole.pos.x,object->obj.hole.pos.y );
		break;
		
		case PHYLIB_HCUSHION:
		snprintf( string, 80,"HCUSHION (%6.1lf)",object->obj.hcushion.y );
		break;
		
		case PHYLIB_VCUSHION: 
		snprintf( string, 80,"VCUSHION (%6.1lf)",object->obj.vcushion.x );
		break;
	}
	return string;
}
  


