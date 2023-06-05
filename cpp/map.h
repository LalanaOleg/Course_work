#pragma once
#include "libraries.h"

bool operator<(pair<int, int> a, pair<int, int> b) {
	if (a.first < b.first) return true;
	if (a.first > b.first) return false;
	if (a.second < b.second) return true;
	return false;
}

class Map {
	set<pair<int, int>> world_set;
	int rows, colmns;
	vector<string> map;

public:
	Map() {}
	Map(string file_name) {
		ifstream f(file_name);
		if (!f.is_open()) {
			cout << "File is not found";
			exit(0);
		}
		string buf;
		int row = 0, col = 0;
		pair<int, int> coord;
		while (f) {
			getline(f, buf);
			f.tellg();
			row = 0;
			for (auto cell : buf) {
				if (cell != '_') {
					coord.first = row;
					coord.second = col;
					world_set.insert(coord);
				}
				row++;
			}
			map.push_back(buf);
			col++;
		}
		f.close();
		this->colmns = map.size();
		this->rows = map[0].size();
	}

	static Map create(string file_name) {
		return Map(file_name);
	}

	bool is_wall(pair<int, int>& coords) {
		return world_set.count(coords);
	}

	int get_cell(pair<int, int>& coords) {
		return map[coords.second][coords.first];
	}

	set<pair<int, int>> get_world_set() {
		return world_set;
	}

	vector<string> get_map() {
		return map;
	}

	Map& get_this() {
		return *this;
	}
};

