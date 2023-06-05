#pragma once
#include "map.h"


class RayCast {
private:
	int NUM_RAYS;
	int MAX_DEPTH;
	int SCALE;
	int HALF_HEIGHT;
	double DELTA_ANGLE;
	double SCREEN_DIST;
	double HALF_FOV;
	Map* map;
	vector<std::tuple<double, double, int, double>> ray_casting_result;
	std::tuple<double, double, int, double> result_of_ray;

	RayCast(Map& map) {
		py::module settings = py::module_::import("settings");
		NUM_RAYS = py::cast<int>(settings.attr("NUM_RAYS"));
		MAX_DEPTH = py::cast<int>(settings.attr("MAX_DEPTH"));
		SCALE = py::cast<int>(settings.attr("SCALE"));
		HALF_HEIGHT = py::cast<int>(settings.attr("HALF_HEIGHT"));
		DELTA_ANGLE = py::cast<double>(settings.attr("DELTA_ANGLE"));
		SCREEN_DIST = py::cast<double>(settings.attr("SCREEN_DIST"));
		HALF_FOV = py::cast<double>(settings.attr("HALF_FOV"));
		this->map = &map;
		ray_casting_result.resize(NUM_RAYS);
	}

public:
	static RayCast create(Map& map) {
		return RayCast(map);
	}
	RayCast() {}
	
	vector<std::tuple<double, double, int, double>> ray_cast(double ox, double oy, double angle) {
		int x_map = ox, y_map = oy;
		double ray_angle = angle - HALF_FOV + 0.001;
		this->ray_casting_result.clear();

		for (register int ray = 0; ray < NUM_RAYS; ray++) {
			double sin_a = sin(ray_angle),
					cos_a = cos(ray_angle);

			// Horizontals
			double y_hor = ((sin_a > 0) ? (y_map + 1) : (y_map - 1e-6));
			double dy = ((sin_a > 0) ? 1 : -1);

			double depth_hor = (y_hor - oy) / sin_a;
			double x_hor = ox + depth_hor * cos_a;

			double delta_depth = dy / sin_a;
			double dx = delta_depth * cos_a;

			pair<int, int> buf;
			int texture, texture_hor, texture_vert;

			for (int i = 0; i < MAX_DEPTH; i++) {
				buf.first = x_hor;
				buf.second = y_hor;
				if (map->is_wall(buf)) {
					texture_hor = map->get_cell(buf);
					break;
				}
				x_hor += dx;
				y_hor += dy;
				depth_hor += delta_depth;
			}
			
			// Verticals
			double x_vert = ((cos_a > 0) ? (x_map + 1) : (x_map - 1e-6));
			dx = ((cos_a > 0) ? 1 : -1);

			double depth_vert = (x_vert - ox) / cos_a;
			double y_vert = oy + depth_vert * sin_a;

			delta_depth = dx / cos_a;
			dy = delta_depth * sin_a;

			for (int i = 0; i < MAX_DEPTH; i++) {
				buf.first = x_vert;
				buf.second = y_vert;
				if (map->is_wall(buf)) {
					texture_vert = map->get_cell(buf);
					break;
				}
				x_vert += dx;
				y_vert += dy;
				depth_vert += delta_depth;
			}

			double depth, offset;

			if (depth_vert < depth_hor) {
				texture = texture_vert;
				depth = depth_vert;
				y_vert -= (int)y_vert;
                offset = cos_a > 0 ? y_vert : (1 - y_vert);
			}
			else{
				texture = texture_hor;
				depth = depth_hor;
				x_hor -= (int)x_hor;
                offset = sin_a > 0 ? x_hor : (1 - x_hor);
			}

			depth *= cos(angle - ray_angle);

			// PROJECTION
			double proj_height = SCREEN_DIST / (depth + 0.0001);

			get<0>(result_of_ray) = depth;
			get<1>(result_of_ray) = proj_height;
			get<2>(result_of_ray) = texture - '0';
			get<3>(result_of_ray) = offset;

			this->ray_casting_result.push_back(result_of_ray);

			ray_angle += DELTA_ANGLE;
		}
		return this->ray_casting_result;
	}
};
