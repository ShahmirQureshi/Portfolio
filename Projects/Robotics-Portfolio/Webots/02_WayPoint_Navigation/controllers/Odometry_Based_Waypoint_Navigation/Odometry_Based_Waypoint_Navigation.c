/*
 * Odometry-Based Waypoint Navigation
 * Robot   : e-puck
 * Simulator: Webots
 * Control : FSM + Geometric Control (Odometry only)
 */

#include <stdio.h>
#include <math.h>

#include <webots/robot.h>
#include <webots/motor.h>
#include <webots/position_sensor.h>

/* =========================
 * Constants
 * ========================= */
#define TIME_STEP   32
#define MAX_SPEED   6.28

#define WHEEL_RADIUS 0.0205
#define AXLE_LENGTH  0.0565

#define NUM_WAYPOINTS 4

#define HEADING_TOL  0.001   // rad
#define DIST_TOL     0.001  // meters

/* =========================
 * FSM States
 * ========================= */
typedef enum {
  ROTATE_TO_GOAL,
  MOVE_TO_GOAL,
  WAYPOINT_REACHED,
  STOP
} State;

/* =========================
 * State name helper
 * ========================= */
const char* state_name(State s) {
  switch (s) {
    case ROTATE_TO_GOAL:    return "ROTATE_TO_GOAL";
    case MOVE_TO_GOAL:      return "MOVE_TO_GOAL";
    case WAYPOINT_REACHED:  return "WAYPOINT_REACHED";
    case STOP:              return "STOP";
    default:                return "UNKNOWN";
  }
}

int main() {

  wb_robot_init();

  /* =========================
   * Motors
   * ========================= */
  WbDeviceTag left_motor  = wb_robot_get_device("left wheel motor");
  WbDeviceTag right_motor = wb_robot_get_device("right wheel motor");

  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);

  WbDeviceTag left_enc  = wb_robot_get_device("left wheel sensor");
  WbDeviceTag right_enc = wb_robot_get_device("right wheel sensor");

  wb_position_sensor_enable(left_enc, TIME_STEP);
  wb_position_sensor_enable(right_enc, TIME_STEP);

  /* =========================
   * Initial encoder values
   * ========================= */
  wb_robot_step(TIME_STEP);
  double prev_L = wb_position_sensor_get_value(left_enc);
  double prev_R = wb_position_sensor_get_value(right_enc);

  /* =========================
   * Waypoints (meters)
   * ========================= */
  double waypoints[NUM_WAYPOINTS][2] = {
    { 0.35, 0.0 },
    { 0.35, 0.35 },
    { 0.0, 0.35 },
    { 0.0, 0.0 }
  };

  int current_wp = 0;

  /* =========================
   * Odometry state
   * ========================= */
  double x = 0.0;
  double y = 0.0;
  double theta = 0.0;

  /* =========================
   * FSM state
   * ========================= */
  State state = ROTATE_TO_GOAL;

  /* =========================
   * Logging (Odometry only)
   * ========================= */
  FILE *log = fopen("waypoint_log_odom.csv", "w");
  fprintf(log, "time,state,x,y,theta,wp_x,wp_y,distance\n");

  /* =========================
   * Main loop
   * ========================= */
  while (wb_robot_step(TIME_STEP) != -1) {

    double left_speed  = 0.0;
    double right_speed = 0.0;

    /* -------------------------
     * Navigation math
     * ------------------------- */
    double dx = waypoints[current_wp][0] - x;
    double dy = waypoints[current_wp][1] - y;

    double distance = sqrt(dx*dx + dy*dy);
    double target_theta = atan2(dy, dx);

    double heading_error = target_theta - theta;

    while (heading_error > M_PI)  heading_error -= 2.0*M_PI;
    while (heading_error < -M_PI) heading_error += 2.0*M_PI;

    /* -------------------------
     * FSM
     * ------------------------- */
    switch (state) {

      case ROTATE_TO_GOAL: {
        double w = 3.0 * heading_error;
        if (w >  1.5) w =  1.5;
        if (w < -1.5) w = -1.5;

        left_speed  = -w;
        right_speed =  w;

        if (fabs(heading_error) < HEADING_TOL)
          state = MOVE_TO_GOAL;
        break;
      }

      case MOVE_TO_GOAL: {
        double Kp = 2.0;
        left_speed  = 3.0 - Kp * heading_error;
        right_speed = 3.0 + Kp * heading_error;

        if (distance < DIST_TOL)
          state = WAYPOINT_REACHED;
        break;
      }

      case WAYPOINT_REACHED:
        current_wp++;
        state = (current_wp >= NUM_WAYPOINTS) ? STOP : ROTATE_TO_GOAL;
        break;

      case STOP:
        left_speed  = 0.0;
        right_speed = 0.0;
        break;
    }

    /* -------------------------
     * Speed saturation
     * ------------------------- */
    if (left_speed  >  MAX_SPEED) left_speed  =  MAX_SPEED;
    if (left_speed  < -MAX_SPEED) left_speed  = -MAX_SPEED;
    if (right_speed >  MAX_SPEED) right_speed =  MAX_SPEED;
    if (right_speed < -MAX_SPEED) right_speed = -MAX_SPEED;

    wb_motor_set_velocity(left_motor, left_speed);
    wb_motor_set_velocity(right_motor, right_speed);

    /* -------------------------
     * Odometry (midpoint method)
     * ------------------------- */
    double cur_L = wb_position_sensor_get_value(left_enc);
    double cur_R = wb_position_sensor_get_value(right_enc);

    double dL = (cur_L - prev_L) * WHEEL_RADIUS;
    double dR = (cur_R - prev_R) * WHEEL_RADIUS;

    prev_L = cur_L;
    prev_R = cur_R;

    double ds     = 0.5 * (dL + dR);
    double dtheta = (dR - dL) / AXLE_LENGTH;

    x     += ds * cos(theta + 0.5 * dtheta);
    y     += ds * sin(theta + 0.5 * dtheta);
    theta += dtheta;

    while (theta > M_PI)  theta -= 2.0*M_PI;
    while (theta < -M_PI) theta += 2.0*M_PI;

    /* -------------------------
     * Logging
     * ------------------------- */
    double t = wb_robot_get_time();
    int wp_idx = (current_wp >= NUM_WAYPOINTS) ? NUM_WAYPOINTS - 1 : current_wp;

    fprintf(log, "%f,%s,%f,%f,%f,%f,%f,%f\n",
      t,
      state_name(state),
      x,
      y,
      theta,
      waypoints[wp_idx][0],
      waypoints[wp_idx][1],
      distance
    );

    printf("WP %d | x=%.3f y=%.3f theta=%.1f deg\n",
      current_wp,
      x,
      y,
      theta * 180.0 / M_PI
    );
  }

  /* =========================
   * Cleanup
   * ========================= */
  fclose(log);
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);

  wb_robot_cleanup();
  return 0;
}
