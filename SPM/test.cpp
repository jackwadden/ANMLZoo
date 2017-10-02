#include <iostream>
#include <fstream>
using namespace std;

int main()
{
	ifstream ifs;
	ifs.open("inputs/SPM_1MB.input");
	unsigned char c;
	int cnt = 0;
	while(ifs >> c) {
		cnt++;
		if (cnt == 400)
			break;
		cout << hex << (unsigned)c << ' ';
	}
	cout << "wowow" << endl;
	ifs.close();
	return 0;
}
