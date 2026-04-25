/*
 * Comparative Odometry Analysis
 * Modes: Straight, Square, Circle, Line Following
 * Robot: E-Puck
 */

#include <stdio.h>
#include <math.h>

#include <webots/robot.h>
#include <webots/motor.h>
#include <webots/distance_sensor.h>

/* -------------------------
 * Constants
 * ------------------------- */
#define TIME_STEP 32

#define THRESHOLD       500
#define GOAL_THRESHOLD  298

#define MAX_SPEED   3.0
#define TURN_SPEED  1.5

#define WHEEL_RADIUS 0.0205
#define AXLE_LENGTH  0.0565
int circle_state = 0;   // 0 = move forward, 1 = circle

/* -------------------------
 * Motion Modes
 * ------------------------- */
typedef enum {
  MODE_STRAIGHT,
  MODE_SQUARE,
  MODE_CIRCLE,
  MODE_LINE
} MotionMode;

/* -------------------------
 * Main
 * ------------------------- */
int main() {

  wb_robot_init();
  double dt = TIME_STEP / 1000.0;

  /* -------------------------
   * Sensors
   * ------------------------- */
  WbDeviceTag gs[3];
  const char *gs_names[3] = {"gs0", "gs1", "gs2"};

  for (int i = 0; i < 3; i++) {
    gs[i] = wb_robot_get_device(gs_names[i]);
    wb_distance_sensor_enable(gs[i], TIME_STEP);
  }

  /* -------------------------
   * Motors
   * ------------------------- */
  WbDeviceTag left_motor  = wb_robot_get_device("left wheel motor");
  WbDeviceTag right_motor = wb_robot_get_device("right wheel motor");

  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);

  /* -------------------------
   * Odometry State
   * ------------------------- */
  double x = 0.0;
  double y = 0.0;
  double theta = M_PI / 2.0;

  /* -------------------------
   * Experiment Control
   * ------------------------- */
  MotionMode mode = MODE_LINE;   // <<< CHANGE MODE HERE

  double elapsed_time = 0.0;

  int square_side = 0;
  int square_state = 0;
  double state_time = 0.0;
  double turn_start_theta = 0.0;
  
  /* -------------------------
   * Logging
   * ------------------------- */
  FILE *log = fopen("odom_log.csv", "w");
  fprintf(log, "time,mode,state,x,y,theta,error\n");


  /* -------------------------
   * Main Loop
   * ------------------------- */
  while (wb_robot_step(TIME_STEP) != -1) {

    elapsed_time += dt;

    double left_speed = 0.0;
    double right_speed = 0.0;
    const char *action = "";
    const char *mode_name = "";

    /* =========================
     * MODE: STRAIGHT
     * ========================= */
    if (mode == MODE_STRAIGHT) {
      mode_name = "STRAIGHT";
      left_speed = MAX_SPEED;
      right_speed = MAX_SPEED;
      action = "Straight";

      if (elapsed_time > 8.0)
        break;
    }

    /* =========================
     * MODE: CIRCLE
     * ========================= */
    else if (mode == MODE_CIRCLE) {
    mode_name = "CIRCLE";
    if (circle_state == 0) {
      left_speed = MAX_SPEED;
      right_speed = MAX_SPEED;
      action = "Circle Setup Forward";
  
      if (elapsed_time > 5.0) {
        circle_state = 1;
        elapsed_time = 0.0;
      }
    }
    else {
      left_speed = MAX_SPEED;
      right_speed = 0.6 * MAX_SPEED;
      action = "Circle Motion";
  
      if (elapsed_time > 15)
        break;
    }
  }
  

    /* =========================
     * MODE: SQUARE
     * ========================= */
    

    else if (mode == MODE_SQUARE) {
    mode_name = "SQUARE";

    if (square_side >= 4)
      break;
  
    if (square_state == 0) {
      left_speed = MAX_SPEED;
      right_speed = MAX_SPEED;
      action = "Square Forward";
  
      state_time += dt;
      if (state_time > 6.0) {
        square_state = 1;
        state_time = 0.0;
      }
    }
    else {
      if (state_time == 0.0) {
        turn_start_theta = theta;
        state_time = dt;   // mark init
      }
  
      left_speed  =  TURN_SPEED;
      right_speed = -TURN_SPEED;
      action = "Square Turn (Odometry)";
  
      double angle_diff = atan2(
        sin(theta - turn_start_theta),
        cos(theta - turn_start_theta)
      );
  
      if (fabs(angle_diff) >= M_PI / 2.0) {
        square_state = 0;
        square_side++;
        state_time = 0.0;
      }
    }
  }
  
    /* =========================
     * MODE: LINE FOLLOWING
     * ========================= */
    else if (mode == MODE_LINE) {

      double left_val   = wb_distance_sensor_get_value(gs[0]);
      double center_val = wb_distance_sensor_get_value(gs[1]);
      double right_val  = wb_distance_sensor_get_value(gs[2]);

      left_speed = MAX_SPEED;
      right_speed = MAX_SPEED;
      action = "Line Straight";

      if (center_val < THRESHOLD) {
        action = "Line Straight";
      }
      else if (left_val < THRESHOLD) {
        left_speed  = -0.10 * MAX_SPEED;
        right_speed =  0.25 * MAX_SPEED;
        action = "Line Left";
      }
      else if (right_val < THRESHOLD) {
        left_speed  =  0.25 * MAX_SPEED;
        right_speed = -0.10 * MAX_SPEED;
        action = "Line Right";
      }
      else {
        left_speed  =  TURN_SPEED;
        right_speed = -TURN_SPEED;
        action = "Line Search";
      }

      if (left_val < GOAL_THRESHOLD &&
          center_val < GOAL_THRESHOLD &&
          right_val < GOAL_THRESHOLD) {
        break;
      }
    }

    /* -------------------------
     * Apply speeds
     * ------------------------- */
    wb_motor_set_velocity(left_motor, left_speed);
    wb_motor_set_velocity(right_motor, right_speed);

    /* -------------------------
     * Odometry (MIDPOINT)
     * ------------------------- */
    double dl = left_speed  * WHEEL_RADIUS * dt;
    double dr = right_speed * WHEEL_RADIUS * dt;

    double ds = (dl + dr) / 2.0;
    double dtheta = (dr - dl) / AXLE_LENGTH;

    x += ds * cos(theta + dtheta / 2.0);
    y += ds * sin(theta + dtheta / 2.0);
    theta += dtheta;
    double error = sqrt(x*x + y*y);

    /* -------------------------
     * Log data
     * ------------------------- */
    fprintf(log, "%.2f,%s,%s,%.3f,%.3f,%.3f,%.3f\n",
        elapsed_time,
        mode_name,
        action,
        x,
        y,
        theta,
        error);

    /* -------------------------
     * Debug
     * ------------------------- */
    printf("Action: %s | x=%.3f y=%.3f theta=%.2f deg | Error=%.3f m\n",
       action,
       x,
       y,
       theta * 180.0 / M_PI,
       error);

    }
  /* -------------------------
   * Cleanup
   * ------------------------- */
  fclose(log);
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);
  printf("\n=== FINAL ERROR ===\n");
  printf("Final position error = %.3f m\n", sqrt(x*x + y*y));

  wb_robot_cleanup();

  return 0;
}
