#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <vector>
//#include <unistd.h>
#include <io.h>
#include <time.h>

using namespace std;

char *datafile = NULL;
int signals = -1;
int frequenz = -1;		// sollte 1000 Hz sein
int versatz = -1;		// sollte 50 Samples bei 1000Hz betragen
int feature_len = -1;		// sollte bei 150 Samples bei 1000Hz sein

float max(vector < vector < float >>*data, int spalte, int n)
{
	float m = (*data)[spalte][0];
	for (int i = 1; i < n; i++)
		if ((*data)[spalte][i] > m)
			m = (*data)[spalte][i];
	return m;
}

float min(vector < vector < float >>*data, int spalte, int n)
{
	float m = (*data)[spalte][0];
	for (int i = 1; i < n; i++)
		if ((*data)[spalte][i] < m) {
			m = (*data)[spalte][i];
		}
	return m;
}

void fswap(float *a, float *b)
{
	float c = *a;
	*a = *b;
	*b = c;
}


float medianfilter(float *data, unsigned int len)
{
	if (len > 3) {
		printf("nicht implementiert\n");
		exit(0);
	}
	vector < float >sort(data, data + len);

	if (sort[0] > sort[2])
		fswap(&sort[0], &sort[2]);

	if (sort[0] > sort[1])
		fswap(&sort[0], &sort[1]);

	if (sort[1] > sort[2])
		fswap(&sort[1], &sort[2]);

	return (sort[1]);
}

void remove_peaks(vector < vector < float >>*data, int spalte, int start, int stop)
{

	float med[3];

	for (int i = start; i < stop; i++) {

		if (i <= 0)
			med[0] = (*data)[spalte][0];
		else
			med[0] = (*data)[spalte][i - 1];

		med[1] = (*data)[spalte][i];

		if (i >= (*data)[spalte].size() - 1)
			med[2] = (*data)[spalte][i];
		else
			med[2] = (*data)[spalte][i + 1];

		(*data)[spalte][i] = medianfilter(med, 3);
	}
}

float avg(vector < vector < float >>*data, int spalte, int start, int stop)
{
	double m = 0.0;
	for (int i = start; i < stop; i++)
		m += (*data)[spalte][i];
	return (float) (m / ((float) (stop - start)));
}

void norm(vector < vector < float >>*data, int spalte, int start, int stop)
{
	float fmin = min(data, spalte, (*data)[spalte].size());
	float fmax = max(data, spalte, (*data)[spalte].size());
	float fdif = fmax - fmin;
	float favg = avg(data, spalte, 0, (*data)[spalte].size());

	for (int i = 0; i < (*data)[spalte].size(); i++)
		(*data)[spalte][i] = 2.0 * (((*data)[spalte][i] - fmin) / fdif) - 1.0;

	fmin = min(data, spalte, (*data)[spalte].size());
	fmax = max(data, spalte, (*data)[spalte].size());
	favg = avg(data, spalte, 0, (*data)[spalte].size());
}

void features(vector < vector < float >>*data, int start, int stop)
{

	float DEADZONE = 0.001;

	for (int signl = 0; signl < data->size(); signl++) {

		// first feature: mean average
		float favg = avg(data, signl, start, stop);

		// compute features: wave slope lenght, zero count, slope direction changes
		int flag1 = 1;
		int flag2 = 1;
		int zero_count = 0;
		float len = 0;
		int turns = 0;

		// achtung: in der Orginalversion war n gleich eins
		// um bessere Sensitivität zu erreichen wurde hier n auf zwei gesetzt
		const int n = 2;
		for (int i = start + n; i < (stop - n); i++) {
			float fst = (*data)[signl][i - n];
			float mid = (*data)[signl][i];
			float lst = (*data)[signl][i + n];

			// Compute Zero Crossings
			if ((mid >= 0 && fst >= 0) || (mid <= 0 && fst <= 0))
				flag1 = flag2;
			else if ((mid < DEADZONE) && (mid > (-1.0 * DEADZONE)) && (fst < DEADZONE) && (fst > (-1.0 * DEADZONE)))
				flag1 = flag2;
			else
				flag1 = (-1) * flag2;

			if (flag1 != flag2) {
				zero_count++;
				// printf("Zero count: %d\n", zero_count);
				flag1 = flag2;
			}
			// Compute Turns Slope Changes
			if ((mid > fst && mid > lst) || (mid < fst && mid < lst))
				// turns threshold of 15mV (i.e. 3uV noise)
				if ((fabs(mid - fst) > 0.0015) || (fabs(mid - lst) > 0.0015)) {
					turns++;
					//printf("Turns: %d\n", turns);
				}
			// Compute Waveform Length
			len += fabs(fst - mid);
		}

		//printf("\nraw features\n");
		//printf("Kanal=%i mav=%f len=%f zc=%d turns=%d\n", signl, favg, len, zero_count, turns);
		// normiere Features
		float framelen = stop - start;
		len = len / framelen;
		float fturns = ((float) turns) / framelen;
		float f_zero_count = ((float) zero_count) / framelen;
		//printf("normalized features\n");
		//printf("mav=%f len=%f zc=%f turns=%f ", favg, len, f_zero_count, fturns);
		//printf("%1.6f %1.6f %1.6f %1.6f ", favg, len, f_zero_count, fturns);
	}
}

/**
 * print error message and exit with error code
 */
void usage(char *command)
{
	printf("usage: %s <options>\n", command);
	printf("\n");
	printf("-i <file>           data file\n");
	printf("-f <frequency>      sample frequency\n");
	printf("-n <signals>        number of signals\n");
	printf("-l <feat. length>   length of a feature[samples]\n");
	printf("-k <shift>          distance between features[samples]\n");
	printf("\n");
	printf("file format: lines with <no. signals> raw signal values followed by the label\n");
	exit(1);
}

/**
 * parse command line parameters
 */
void parse_parameters(int argcc, char **argvv, char **datafile)
{

	if (argcc < 3)
		usage(*argvv);

	*datafile = NULL;	// set data file name to empty
	signals = -1;		// set signals to an invalid values
	frequenz = -1;		// sollte 1000 Hz sein
	versatz = -1;		// sollte 50 Samples bei 1000Hz betragen
	feature_len = -1;	// sollte bei 150 Samples bei 1000Hz sein

	//parse command line parameters
	printf("\n");
	char opt;
	//while ((opt = getopt(argcc, argvv, "i:n:f:l:k:")) != -1) {
	for(unsigned int i = argcc - 1; i > 0; i--){
		if(argvv[i][0] != '-') continue;
		opt = argvv[i][1];
		char* optarg = argvv[i+1];
		switch (opt) {

		case 'i':	// read test data set
			*datafile = (char *) malloc(sizeof(char) * (strlen(optarg) + 1));
			strcpy(*datafile, optarg);
			printf("data file:    %s\n", *datafile);
			break;

		case 'n':	// number of signals
			signals = atoi(optarg);
			printf("no. signals:  %d\n", signals);
			break;

		case 'f':	// frequency
			frequenz = atoi(optarg);
			printf("frequency:    %d\n", frequenz);
			break;

		case 'l':	// feature length
			feature_len = atoi(optarg);
			printf("feat. length: %d\n", feature_len);
			break;

		case 'k':	// feature shoft
			versatz = atoi(optarg);
			printf("shift:        %d\n", versatz);
			break;

		default:
			usage(*argvv);
		}
	}
	printf("\n");
	if (signals < 1 || datafile == NULL || frequenz < 1 || feature_len < 1 || versatz < 1)
		usage(*argvv);
}

int main(int argcc, char *argvv[])
{


	parse_parameters(argcc, argvv, &datafile);

	vector < vector < float >>fdata(signals, std::vector < float >());
	vector < unsigned int >labels;



	//printf("Daten lesen\n");

	FILE *f = NULL;
	if ((f = fopen(datafile, "r")) == NULL) {
		printf("Cant open %s for reading\n", datafile);
		exit(1);
	}
#define line_len 2000
	char line[line_len];
	const char s[2] = ";";
	char *token;
	double data_line[signals + 1];	// temporary data
	int j;

	while (fgets(line, line_len, f) != NULL) {

		// skip empty lines
		if (strlen(line) < 2)
			continue;

		// parse line
		token = strtok(line, s);
		for (j = 0; j < signals + 1 && token != NULL; j++) {
			data_line[j] = atof(token);
			token = strtok(NULL, s);
		}
		if (j < (signals + 1))
			continue;	// error, could not read all signals and the label

		// copy data to fdata and labels arrays
		for (j = 0; j < signals; j++)
			fdata[j].push_back(data_line[j]);
		labels.push_back(data_line[signals]);

	}
	fclose(f);

	printf("%ld Zeilen gelesen\n", fdata[0].size());
	printf("Example Row: %2.f %2.f %2.f %2.f\n", fdata[0][1024], fdata[1][1024], fdata[2][1024], fdata[3][1024]);
	printf("size=%ld\n", fdata.size());
	printf("min=%2.f\n", min(&fdata, 0, fdata[0].size()));
	printf("max=%2.f\n", max(&fdata, 0, fdata[0].size()));
	printf("avg=%2.f\n", avg(&fdata, 0, 0, fdata[0].size()));


	printf("Peaks löschen");
	clock_t start = clock();
	remove_peaks(&fdata, 0, 0, fdata[0].size());
	remove_peaks(&fdata, 1, 0, fdata[1].size());
	remove_peaks(&fdata, 2, 0, fdata[2].size());
	remove_peaks(&fdata, 3, 0, fdata[3].size());
	printf(": %2.fs\n",clock() - start / CLOCKS_PER_SEC);

	printf("normieren");
	start = clock();
	norm(&fdata, 0, 0, fdata[0].size());
	norm(&fdata, 1, 0, fdata[1].size());
	norm(&fdata, 2, 0, fdata[2].size());
	norm(&fdata, 3, 0, fdata[3].size());
	printf(": %2.fs\n",clock() - start / CLOCKS_PER_SEC);


	printf("berechnen der Features");
	start = clock();
	// bereche einen Featurevektor mit 150ms Daten
	for (int i = 0; i < (fdata[0].size() - versatz + 1); i += versatz) {
		features(&fdata, i, i + feature_len);
		//printf(" %d\n", labels[i+versatz-1]);
	}
	printf(": %2.fs\n",clock() - start / CLOCKS_PER_SEC);

	return 0;
}
