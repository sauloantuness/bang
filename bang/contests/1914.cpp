#include <bits/stdc++.h>

using namespace std;

int main(){
	int n;
	cin >> n;
	while(n--){
		string a, b, c, d;
		cin >> a >> b >> c >> d;
		int x, y;
		cin >> x >> y;

		if(x+y % 2){
			if(b == "IMPAR")
				cout << a << endl;
			else
				cout << c << endl;
		} else {
			if(b == "PAR")
				cout << a << endl;
			else
				cout << c << endl;
		}
	}
}