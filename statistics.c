#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

int main() {
	int maxbits = 100;
	uint8_t* sender_bases = (uint8_t*)malloc(maxbits * sizeof(uint8_t)); //sizeof(uint8_t) is 1
	uint8_t* sender_states = (uint8_t*)malloc(maxbits * sizeof(uint8_t));
	uint8_t* eavesdropper_bases = (uint8_t*)malloc(maxbits * sizeof(uint8_t));
	uint8_t* eavesdropper_states = (uint8_t*)malloc(maxbits * sizeof(uint8_t));
	uint8_t* receiver_bases = (uint8_t*)malloc(maxbits*sizeof(uint8_t));
	uint8_t* receiver_states = (uint8_t*)malloc(maxbits*sizeof(uint8_t));
	uint8_t* sender_key = (uint8_t*)malloc(maxbits * sizeof(uint8_t));
	uint8_t* receiver_key = (uint8_t*)malloc(maxbits * sizeof(uint8_t));
	uint8_t* key = (uint8_t*)malloc(maxbits * sizeof(uint8_t));
	int* equal_positions = (int*)malloc(maxbits*sizeof(int));
	
	if (sender_bases == NULL || sender_states == NULL) {
		fprintf(stderr, "malloc fail");
		return 1;
	}

	int error_bound = 0;
	int count;
	int bad_send;
	float bad_send_percent;
	float test_error_percent;
	float keygen_count_percent;
	int test_errors;
	int errors;
	int keygen_count;
	srand(time(NULL));
	int repeats = 10000;
	for (int eavesdropping=0; eavesdropping<2; ++eavesdropping){
		for (int nbits=3; nbits<=maxbits; ++nbits){
			keygen_count = 0;
			bad_send = 0;
			errors = 0;
			for (int reps=0; reps<repeats; ++reps){
				for (int i=0; i<nbits; ++i){
					sender_bases[i] = rand()&1;
					sender_states[i] = rand()&1+2*sender_bases[i];
				}
				if (eavesdropping){
					for (int i=0; i<nbits; ++i){
					eavesdropper_bases[i] = rand()&1;
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
				count = 0;
				for (int i=0; i<nbits; ++i){
					receiver_bases[i] = rand()&1;
					if (receiver_bases[i] == eavesdropper_bases[i]){
						receiver_states[i] = eavesdropper_states[i];
					} else {
						receiver_states[i] = rand()&1+2*receiver_bases[i];
					}
					if ((sender_bases[i] == receiver_bases[i]) && (sender_states[i]!=receiver_states[i])){
						++errors;
						equal_positions[count] = i;
						++count;
					} else{
						if (sender_bases[i] == receiver_bases[i]){
							equal_positions[count] = i;
							++count;
						}
						if (sender_states[i]!=receiver_states[i]){
							++bad_send;
						}
					}
				}
				if ((count != 0) && (test_errors<=error_bound)){
					for (int i=0; i<count; ++i){
						sender_key[i] = sender_states[equal_positions[i]];
						receiver_key[i] = receiver_states[equal_positions[i]];
						if (sender_key[i] == receiver_key[i]){
							key[i] = sender_key[i]%2;
						} else{
							key[0] = 5;
						}
					}
					if (key[0]!=5){
						++keygen_count;
					}
				}
			}
			keygen_count_percent = 100*(float)keygen_count/repeats;
			printf("%f ", keygen_count_percent);
		}
		printf("\n");
	}
	printf("\n");
	free(sender_bases);
	free(sender_states);

	free(eavesdropper_bases);
	free(eavesdropper_states);

	free(receiver_bases);
	free(receiver_states);

	free(equal_positions);

	free(sender_key);
	free(receiver_key);
	free(key);

	return 0;
}
