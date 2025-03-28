#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

static int nbits = 10;

void sendsignal(uint8_t* sender_bases, uint8_t* sender_states){
	for (int i=0; i<nbits; ++i){
		sender_bases[i] = rand()&1;
		sender_states[i] = rand()&1+2*sender_bases[i];
	}
}

void eavesdrop(uint8_t eavesdropping, uint8_t* sender_bases, uint8_t* sender_states, uint8_t* eavesdropper_bases, uint8_t* eavesdropper_states){
	if (eavesdropping){
		for (int i=0; i<nbits; ++i){
		eavesdropper_bases[i] = rand()&1;
			//eavesdropper_states
			if (eavesdropper_bases[i] == sender_bases[i]){
				eavesdropper_states[i] = sender_states[i];
			} else{
				eavesdropper_states[i] = rand()&1+2*eavesdropper_bases[i];
			}
		}
	} else{
		for (int i=0; i<nbits; ++i){
			eavesdropper_bases[i] = sender_bases[i];
			eavesdropper_states[i] = sender_states[i];
		}
	}
}
			
void receive_signal(uint8_t* eavesdropper_bases, uint8_t* eavesdropper_states, uint8_t* receiver_bases, uint8_t* receiver_states){
	for (int i=0; i<nbits; ++i){
		receiver_bases[i] = rand()&1;
		if (receiver_bases[i] == eavesdropper_bases[i]){
			receiver_states[i] = eavesdropper_states[i];
		} else {
			receiver_states[i] = rand()&1+2*receiver_bases[i];
		}
	}
}

int recognize_error(uint8_t* sender_bases, uint8_t* sender_states, uint8_t* receiver_bases, uint8_t* receiver_states){
	int errors = 0;
	for (int i=0; i<nbits; ++i){
		if ((sender_bases[i] == receiver_bases[i]) && (sender_states[i]!=receiver_states[i])){
			++errors;
		}
	}
	return errors;
}

void generate_key(uint8_t* sender_states, uint8_t* receiver_states, uint8_t* sender_key, uint8_t* receiver_key, int count, int* equal_positions, uint8_t* key){
	for (int i=0; i<count; ++i){
		sender_key[i] = sender_states[equal_positions[i]];
		receiver_key[i] = receiver_states[equal_positions[i]];
		if (sender_key[i] == receiver_key[i]){
			key[i] = sender_key[i]%2;
		} else{
			key[0] = 5;
		}
	}
}

void print_array(uint8_t* array, int size){
	for (int i=0; i<size; ++i){
		printf("%u ", array[i]);
	}
	printf("\n");
}
	

int main() {
	uint8_t* sender_bases = (uint8_t*)malloc(nbits * sizeof(uint8_t)); //sizeof(uint8_t) is 1
	uint8_t* sender_states = (uint8_t*)malloc(nbits * sizeof(uint8_t));
	
	int eavesdropping = 1;
	uint8_t* eavesdropper_bases = (uint8_t*)malloc(nbits * sizeof(uint8_t));
	uint8_t* eavesdropper_states = (uint8_t*)malloc(nbits * sizeof(uint8_t));
	
	uint8_t* receiver_bases = (uint8_t*)malloc(nbits*sizeof(uint8_t));
	uint8_t* receiver_states = (uint8_t*)malloc(nbits*sizeof(uint8_t));

		
	if (sender_bases == NULL || sender_states == NULL) {
		fprintf(stderr, "malloc fail");
		return 1;
	}
	
	srand(time(NULL));


	sendsignal(sender_bases, sender_states);

	eavesdrop(eavesdropping, sender_bases, sender_states, eavesdropper_bases, eavesdropper_states);

	receive_signal(eavesdropper_bases, eavesdropper_states, receiver_bases, receiver_states);

	int test_errors = recognize_error(sender_bases, sender_states, receiver_bases, receiver_states);

	int* equal_positions = (int*)malloc(nbits*sizeof(int));
	int count = 0;
	for (int i=0; i<nbits; ++i){
		if (sender_bases[i] == receiver_bases[i]){
			equal_positions[count] = i;
			++count;
		}
	}
	print_array(sender_bases, nbits);
	print_array(sender_states, nbits);
	print_array(eavesdropper_bases, nbits);
	print_array(eavesdropper_states, nbits);
	print_array(receiver_bases, nbits);
	print_array(receiver_states, nbits);
	
	static int error_bound = 0;
	if ((count != 0) && (test_errors<=error_bound)){
		uint8_t* sender_key = (uint8_t*)malloc(count * sizeof(uint8_t));
                uint8_t* receiver_key = (uint8_t*)malloc(count * sizeof(uint8_t));
                uint8_t* key = (uint8_t*)malloc(count * sizeof(uint8_t));
                generate_key(sender_states, receiver_states, sender_key, receiver_key, count, equal_positions, key);
		print_array(sender_key, count);
		print_array(receiver_key, count);
		if (key[0]!=5){
			print_array(key, count);
		}
		free(sender_key);
                free(receiver_key);
                free(key);
	}
	
	free(sender_bases);
	free(sender_states);

	free(eavesdropper_bases);
	free(eavesdropper_states);

	free(receiver_bases);
	free(receiver_states);
	
	free(equal_positions);
	return 0;
}
