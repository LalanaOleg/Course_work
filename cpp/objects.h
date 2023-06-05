#pragma once
#include "ray_casting.h"
#include "libraries.h"
#include <algorithm>

typedef std::tuple<double, py::object, pair<int, int>> element_to_render;
typedef vector<element_to_render> type_of_arr_to_render;

class Object {
public:
	Object () {}
	virtual void update() = 0;
};

class Py_Object: public Object {
public:
	void update() override {
        PYBIND11_OVERRIDE_PURE(
            void, /* Return type */
            Object,      /* Parent class */
            update,          /* Name of function in C++ (must match Python name) */
                  /* Argument(s) */
        );
    }
};

class ObjectRenderer {
	py::object sc;

	ObjectRenderer(py::object sc) {
		this->sc = sc;
	}

public:
	ObjectRenderer() {}

	static ObjectRenderer create(py::object sc) {
		return ObjectRenderer(sc);
	}

	void render_game_objects(type_of_arr_to_render& objects_to_render) {
		sort(objects_to_render.begin(), objects_to_render.end(),
			[](element_to_render& a, element_to_render& b) {
				return get<0>(a) > get<0>(b);
			});
		for (auto i: objects_to_render) {
			sc.attr("blit")(get<1>(i), get<2>(i));
		}
	}
};
