/*
 * fault.c - Defines the available fault handlers. One example,
 *           fault_random, is provided; be sure to add your handlers 
 	     to fault_handlers[].
 *
 */

#include <vmsim.h>
#include <fault.h>
#include <options.h>
#include <physmem.h>
#include <stdlib.h>
#include <stdio.h>

void fault_random(pte_t *pte, ref_kind_t type);
void fault_clock(pte_t *pte, ref_kind_t type);
void fault_fifo(pte_t *pte, ref_kind_t type);
void fault_lru(pte_t *pte, ref_kind_t type);
void fault_second(pte_t *pte, ref_kind_t type);

fault_handler_info_t fault_handlers[6] = {
  { "random", fault_random },
  { "fifo", fault_fifo },
  { "clock", fault_clock },
  { "lru", fault_lru },
  { NULL, NULL } /* last entry must always be NULL/NULL */
};

void fault_random(pte_t *pte, ref_kind_t type) {
	int frame;
	frame = random() % opts.phys_pages;
	physmem_evict(frame, type);  // if frame is empty, nothing happens
	physmem_load(frame, pte, type);
}

// FIFO replacement 
void fault_fifo(pte_t *pte, ref_kind_t type) {
	//printf("FIFO not implemented yet!\n");
	static int check = 1;
	static int frame = 0;
	int loc =0, i;

	if (check <= opts.phys_pages){
		physmem_load(frame,pte, type);
		check = check +1;
		frame = frame +1 ;
	}
	else { //order
		for (int i =0;i<=opts.phys_pages;i++){
			for (int j=0;j<=opts.phys_pages-1;j++){
				if (physmem[i]>physmem[j+1]){
					temp = physmem[j];
					physmem[j] = physmem[i];
					physmem[i] = temp;

				}

			}
		}
		// go out the fisrt one 
		physmem_evict(loc, type);
		physmem_load(loc, pte, type);

	}

}

// CLOCK replacement, sec 9.4.5.2 in OSC 
void fault_clock(pte_t *pte, ref_kind_t type) {
	//printf("CLOCK not implemented yet!\n");
	static int check = 1;
	static int frame = 0;
	int i,loc=0;
	static int clock_hand = 0;

	if(check <= opts.phys_pages)
	{
		physmem_load(frame, pte, type);
		physmem[frame]->reference = 1;
		frame = frame + 1;
		check = check + 1;
					

	}

	else
	{
		for(i=clock_hand;i<opts.phys_pages;i++)
		{
			if(physmem[i]->reference == 0)
			{
				loc = i;
				break;
			}			
			else
			{
				physmem[i]->reference = 0;
			}

			if((i+1) == opts.phys_pages )
				i=0//i = -1;	


		}

				
		physmem_evict(loc, type);  
		physmem_load(loc, pte, type);

		clock_hand++;

		if(clock_hand == opts.phys_pages)
			clock_hand = 0;
		

		
		
	}

}

// LRU replacement 
void fault_lru(pte_t *pte, ref_kind_t type) {
	//printf("LRU not implemented yet!\n");
	static int check = 1;
	static int frame = 0;
	int loc =0, i;
	if (check <= opts.phys_pages){

		physmem_load(frame,pte, type);
		check = check +1;
		frame = frame +1 ;

	}
	else {

		min = physmem[0]->counter;
		for (i=0;i<opts.phys_pages;i++){

			if (min>physmem[i]->counter){
				min = physmem[i]->counter;
				loc = i;
			
			}
			

		}
		physmem_evict(loc, type);
		physmem_load(loc, pte, type);




	}
}

void fault_second(pte_t *pte, ref_kind_t type){
	static int check = 1;
	static int frame = 0;
	int loc =0, i;
	if (check <= opts.phys_pages){

		physmem_load(frame,pte, type);
		physmem[frame]->reference = 1;
		check = check +1;
		frame = frame +1 ;

	}
	else {
		/*min = physmem[0]->count;
		for (i=0;i<opts.phys_pages;i++){
			if (physmem[i]->count<min)
				min = physmem[i]->count;
		}
		for (i=0;i<opts.phys_pages;i++){
			if (physmem[i]->count==min &&  physmem[i]->referenced==0 ){
				loc = i;
				break;

			}
			else if (physmem[i]->count==min){
				physmem[i]->referenced==1
			}

		}*/
		//order
		for (int i =0;i<=opts.phys_pages;i++){
			for (int j=0;j<=opts.phys_pages-1;j++){
				if (physmem[i]->count>physmem[j+1]->count){
					temp = physmem[j];
					physmem[j] = physmem[i];
					physmem[i] = temp;

				}

			}
		}

		//check bit r 
		for (int i =0;i<opts.phys_pages;i++){
			if (physmem[i]->reference == 0){
				loc = i;
				break;
			}
			else {
				physmem[i]->reference=1;

			}
		}

		physmem_evict(loc, type);
		physmem_load(loc, pte, type);

	}


}
