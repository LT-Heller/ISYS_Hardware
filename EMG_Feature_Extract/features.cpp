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

void fswap(float *a, float *b){
		float c=*a;
		*a=*b;
		*b=c;
}


float medianfilter(float *data, int len){
	if (len > 3){
		printf("nicht implementiert\n");
		exit(0);
	}
	len=3;
	float sort[len];
	memcpy(sort, data, len*sizeof(float));
 	
	if (sort[0] > sort[2])
		fswap(&sort[0], &sort[2]);
	
	if (sort[0] > sort[1])
		fswap(&sort[0], &sort[1]);
	
	if (sort[1] > sort[2])
		fswap(&sort[1], &sort[2]);
	
	return(sort[1]);
}

void remove_peaks(float *data, int spalte, int start, int stop){
	
	float med[3];

	for (int i =start; i < stop; i++){
		
		if (i<=0)
			med[0]=data[spalte];
		else
			med[0]=data[(i-1)*signals + spalte];
		
		med[1]=data[i*signals + spalte];
		
		if (i>=len-1)
			med[2]=data[i*signals + spalte];
		else
			med[2]=data[(i+1)*signals + spalte];
		
		data[i*signals + spalte] = medianfilter(med, 3);	
	}		
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
	
	float DEADZONE = 0.001;

	for (int signl=0; signl < signals; signl++){
		
		// first feature: mean average
		float favg = avg(data, signl, start, stop);
		
		// compute features: wave slope lenght, zero count, slope direction changes
		int flag1=1;
		int flag2=1;
		int zero_count = 0;
		float len = 0;
		int turns = 0;
	
		// achtung: in der Orginalversion war n gleich eins
		// um bessere Sensitivität zu erreichen wurde hier n auf zwei gesetzt
		const int n=2;
		for (int i=start+n; i < (stop-n); i++){
			float fst = data[((i-n) * signals ) + signl];
			float mid = data[(i *     signals ) + signl];
			float lst = data[((i+n) * signals ) + signl];
			
			// Compute Zero Crossings
			if ((mid>=0 && fst>=0) || (mid<=0 && fst<=0))
				flag1 = flag2;
			else if ((mid<DEADZONE) && (mid>(-1.0*DEADZONE)) && (fst<DEADZONE) && (fst>(-1.0*DEADZONE)))
				flag1 = flag2;
			else
				flag1 = (-1)*flag2;
			
			if (flag1 != flag2){
				zero_count++;
				// printf("Zero count: %d\n", zero_count);
				flag1 = flag2;
			}
       
			// Compute Turns Slope Changes
			if((mid>fst && mid>lst) || (mid<fst && mid<lst))
				// turns threshold of 15mV (i.e. 3uV noise)
				if ((fabs(mid-fst)>0.0015) || (fabs(mid-lst)>0.0015)){
					turns++;
					//printf("Turns: %d\n", turns);
				}
        // Compute Waveform Length
        len += fabs(fst-mid);
		}	
	
	//printf("\nraw features\n");
	//printf("Kanal=%i mav=%f len=%f zc=%d turns=%d\n", signl, favg, len, zero_count, turns);
	// normiere Features
	float framelen=stop-start;
	len = len/framelen;
	float fturns = ((float) turns) /framelen;
	float f_zero_count = ((float) zero_count) / framelen;
	//printf("normalized features\n");
	//printf("mav=%f len=%f zc=%f turns=%f ", favg, len, f_zero_count, fturns);
	printf("%1.6f %1.6f %1.6f %1.6f ", favg, len, f_zero_count, fturns);
	
		
	}
}


int main(){
	
	
	const int frequenz = 1000; // Hz
	const int versatz = frequenz / 20;  // erzeuge pro Sekunde 20 Featurevektoren
	const int feature_len = (int)(0.15 * ((float) frequenz)); // für ein Feature sollen 150ms Daten verwenden
	
	//printf("Daten lesen\n");
	
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
	//printf("%d Zeilen gelesen\n", len);
	float *value = *fdata;
	//printf("%f",value[4]);

	//printf("Peaks löschen\n");
	remove_peaks(*fdata, 0, 0, len);
	remove_peaks(*fdata, 1, 0, len);
	remove_peaks(*fdata, 2, 0, len);
	remove_peaks(*fdata, 3, 0, len);
	
	
	//printf("normieren\n");
	norm(*fdata, 0, 0, len);
	norm(*fdata, 1, 0, len);
	norm(*fdata, 2, 0, len);
	norm(*fdata, 3, 0, len);
	
	//printf("berechnen der Features\n");
	
	// bereche einen Featurevektor mit 150ms Daten
	for (int i=0; i < (len - versatz + 1); i+=versatz){
		features(*fdata, i, i + feature_len);
		printf(" %d\n", labels[i+versatz-1]);
	}
	
	
	return 0;	
}