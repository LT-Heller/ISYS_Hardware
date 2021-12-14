#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>


int len=0;
#define maxlen 300000

#define line_len 200
#define signals 4

float fdata[maxlen][4];
unsigned int labels[maxlen];

float max(float *data, int spalte, int n){
	float m = data[spalte];
	for (int i=1; i < n; i++)
		if (data[i * signals + spalte]> m)
			m=data[i * signals + spalte];
	return m;
}

float min(float *data, int spalte, int n){
	float m = data[spalte];
	for (int i=1; i < n; i++)
		if (data[i* signals + spalte] < m){
			m=data[i*signals + spalte];
			//printf("min Zeile=%d\n", i);
		}
	return m;
}





float avg(float *data, int spalte, int start, int stop){
	double m=0.0;
	for (int i=start; i < stop; i++)
		m+=data[i * signals + spalte];
	return (float) (m/((float)(stop-start)));
}

void norm(float *data, int spalte, int start, int stop){
	float fmin = min(data, spalte, len);
	float fmax = max(data, spalte, len);
	float fdif = fmax - fmin;
	float favg = avg(data, spalte, 0, len);
	
	for (int i =0; i < len; i++)
		data[i*signals + spalte] = 2.0*((data[i*signals + spalte]-fmin) / fdif) - 1.0;
		
	fmin = min(data, spalte, len);
	fmax = max(data, spalte, len);
	favg = avg(data, spalte, 0, len);
}



void features(float *data, int start, int stop){
	
	float DEADZONE = 0.000025;

	for (int signl=0; signl < signals; signl++){
		
		// first feature: mean average
		float favg = avg(data, signl, start, stop);
		
		// compute features: wave slope lenght, zero count, slope direction changes
		int flag1=1;
		int flag2=1;
		int zero_count = 0;
		float len = 0;
		int turns = 0;
	
		for (int i=start+1; i < (stop-1); i++){
			float fst = data[((i-1) * signals ) + signl];
			float mid = data[(i *     signals ) + signl];
			float lst = data[((i+1) * signals ) + signl];
			
			// Compute Zero Crossings
			if ((mid>=0 && fst>=0) || (mid<=0 && fst<=0))
				flag1 = flag2;
			else if ((mid<DEADZONE) && (mid>-DEADZONE) && (fst<DEADZONE) && (fst>-DEADZONE))
				flag1 = flag2;
			else
				flag1 = (-1.0)*flag2;
			
			if (flag1 != flag2){
				zero_count++;
				flag1 = flag2;
			}
       
			// Compute Turns Slope Changes
			if((mid>fst && mid>lst) || (mid<fst && mid<lst))
				// turns threshold of 15mV (i.e. 3uV noise)
				if ((fabs(mid-fst)>0.00015) || (fabs(mid-lst)>0.00015))
					turns++;
				
        // Compute Waveform Length
        len += fabs(fst-mid);
		}	
	// normiere Features
	float framelen=stop-start;
	len = len/framelen;
	turns = turns/framelen;
	float f_zero_count = ((float) zero_count) / framelen;
	printf("mav=%f len=%f zc=%f turns=%f\n", favg, len, f_zero_count, turns);
	
	
		
	}
}


int main(){
	
	printf("Daten lesen\n");
	
	FILE *f = fopen("a", "r"); 
	char line[line_len];
	
	
	const char s[2] = ";";
	char *token;
   
	while (fgets(line, line_len, f) != NULL){
		// skip empty lines
		if (strlen(line) < 2)
			continue;
		token = strtok(line, s);
		
		
		for (int j=0; j < 4; j++){
			fdata[len][j] = atof(token);
			token = strtok(NULL, s);
		}
		labels[len]=atoi(token);
		len++;
		
	}
	fclose(f);
	printf("%d Zeilen gelesen\n", len);
	
	printf("normieren\n");
	norm(*fdata, 0, 0, len);
	norm(*fdata, 1, 0, len);
	norm(*fdata, 2, 0, len);
	norm(*fdata, 3, 0, len);
	
	printf("berechnen der Features\n");
	
	// bereche einen Fateruevektro mit 150ms Daten
	features(*fdata, 0, 150);

	
	
	return 0;	
}