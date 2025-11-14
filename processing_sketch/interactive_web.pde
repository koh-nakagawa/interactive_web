import oscP5.*;
import java.util.ArrayList;

OscP5 osc;
float bass = 0;
float threshold = 0.001;  // デフォルト値（後でOSCで上書きされる）

// ---- 波紋クラス ----
class Ripple {
  float radius;
  float speed;

  Ripple(float s) {
    radius = 0;
    speed = s;         // 一定速度で広がる
  }

  void update() {
    radius += speed;
  }

  boolean isFinished() {
    return radius > max(width, height) * 1.2;
  }

  void draw() {
    ellipse(width/2, height/2, radius, radius);
  }
}

ArrayList<Ripple> ripples = new ArrayList<Ripple>();

void setup() {
  size(1920, 1080, P3D);
  osc = new OscP5(this, 5005);
  noFill();
  stroke(255);
  strokeWeight(10);
}

void oscEvent(OscMessage m) {
  if (m.checkAddrPattern("/bass")) {
    bass = m.get(0).floatValue();
  }

  if (m.checkAddrPattern("/threshold")) {
    threshold = m.get(0).floatValue();
  }
}

void draw() {
  background(0);

  // ---- threshold を使って円を出す ----
  if (bass > threshold) {
    float speed = 30;      // 一定速度
    ripples.add(new Ripple(speed));
  }

  // ---- 全ての波紋を更新 & 描画 ----
  for (int i = ripples.size() - 1; i >= 0; i--) {
    Ripple r = ripples.get(i);
    r.update();
    r.draw();

    if (r.isFinished()) {
      ripples.remove(i);
    }
  }
}
