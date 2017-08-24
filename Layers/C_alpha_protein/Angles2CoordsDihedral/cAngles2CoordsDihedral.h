#ifndef CANGLES2COORDS_H_
#define CANGLES2COORDS_H_
#include <TH.h>
#include <THC.h>


class cAngles2CoordsDihedral{

	THCudaTensor *d_alpha, *d_beta, *d_A, *d_dalpha, *d_dbeta; // angles derivatives
	THCudaTensor *d_drdalpha, *d_drdbeta;	// coordinates derivatives
	THCState *state;

	int angles_length;
	float R;
    	
public:

	cAngles2CoordsDihedral( THCState *state, 
                    THCudaTensor *A,            //16 x max_angles
                    THCudaTensor *input_angles, //future input
                    THCudaTensor *dr_dangle,    //2 x 3 x max_atoms x max_angles
                    float R,                        //bond length
                    int angles_length              // input actual number of angles in the sequence
                   );
	
    void computeForward(    THCudaTensor *input_angles,     // input angles, 2 x maxlen float tensor
                            THCudaTensor *output_coords      // output coords, 3 x maxlen + 1
                            );
                        
	void computeBackward(   THCudaTensor *gradInput,            //output gradient of the input angles
                            THCudaTensor *gradOutput_coords    //input gradient of the coordinates
                            );
                            
	~cAngles2CoordsDihedral();

};

#endif