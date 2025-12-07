#include <iostream>
#include <array>
#include <vector>
#include <cmath>

using Vec2 = std::array<double, 2>;

// vector addition
Vec2 operator+(const Vec2& a, const Vec2& b) {
    return {a[0] + b[0], a[1] + b[1]};
}

// vector subtraction
Vec2 operator-(const Vec2& a, const Vec2& b) {
    return {a[0] - b[0], a[1] - b[1]};
}

// vector divided by scalar
Vec2 operator/(const Vec2& v, double k) {
    if (k == 0.0) {
        throw std::runtime_error("Vector division by zero!");
    }
    return { v[0] / k, v[1] / k };
}

// scalar multiplication  (k * v)
Vec2 operator*(double k, const Vec2& v) {
    return {k * v[0], k * v[1]};
}

// scalar multiplication  (v * k)
Vec2 operator*(const Vec2& v, double k) {
    return {v[0] * k, v[1] * k};
}

double norm(const std::array<double, 2>& r) {
    return sqrt(r[0] * r[0] + r[1] * r[1]);
}

int main() {
    double mu = 1.327e11; // gravitational parameter for the Sun, in km^3/s^2
    double r_earth = 1.496e8; // distance from Sun to Earth, in km
    double r_mars = 1.52 * r_earth; // distance from Sun to Mars, in km
    double T = 450e-6; // thrust in kN = kg*km/s^2, replace value for current property
    double Isp = 9000; // specific impulse in s, replace value for current property
    double m0 = 10000; // initial mass in kg
    double g = 9.81e-3; // gravitational acceleration in km/s^2
    double mdot = T / (Isp * g); // mass flow rate in kg/s

    double m = m0;
    double t = 0.0;
    double dt = 50.0; // time step in seconds
    std::array<double, 2> r{ r_earth, 0.0 }; // initial position in km
    std::array<double, 2> v{ 0.0, sqrt(mu / r_earth) }; // initial velocity in km/s

    std::vector<double> x = { r[0] };
    std::vector<double> y = { r[1] };

    while (norm(r) < r_mars) {
        // acceleration due to gravity
        std::array<double, 2> a_grav = (-mu / std::pow(norm(r), 3)) * r;

        // acceleration due to thrust
        std::array<double, 2> a_thrust{ (T / m) * (v / norm(v)) };

        // total acceleration
        std::array<double, 2> a{ a_grav + a_thrust };

        // update velocity and position
        v = v + a * dt;
        r = r + v * dt;

        // update mass and time
        m = m - mdot * dt;
        t = t + dt;

        // update x and y
        x.push_back(r[0]);
        y.push_back(r[1]);
    }

    // results
    std::cout << "Reached Mars: " << (norm(r) >= r_mars ? "Yes" : "No") << std::endl;
    std::cout << "Final radius: " << norm(r) << " km" << std::endl;
    std::cout << "Final mass: " << m << " kg" << std::endl;
    std::cout << "Travel time: " << t / 3.154e7 << " years" << std::endl;

    return 0;
}
