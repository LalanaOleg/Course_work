#include "cpp_module.hpp"

PYBIND11_MODULE(cpp_module, m) {
	
	py::class_<RayCast>(m, "RayCast")
		.def(py::init())
		.def(py::init(&RayCast::create))
        .def("ray_cast", &RayCast::ray_cast);
	
	py::class_<Map>(m, "Map")
		.def(py::init(&Map::create))
		.def(py::init())
		.def("get_world_set", &Map::get_world_set)
		.def("get_map", &Map::get_map)
		.def("get_this", &Map::get_this);
	
	py::class_<ObjectRenderer>(m, "ObjectRenderer")
		.def(py::init())
		.def(py::init(&ObjectRenderer::create))
		.def("render_game_objects", &ObjectRenderer::render_game_objects);

	py::class_<Object, Py_Object>(m, "Object")
      .def(py::init())
      .def("update", &Object::update);
}