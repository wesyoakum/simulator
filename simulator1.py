<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>2D Entity Simulator</title>
  <style>
    canvas {
      border: 1px solid black;
      background-color: #f8f8f8;
    }
  </style>
</head>
<body>
  <canvas id="sim" width="500" height="500"></canvas>

  <script>
    const canvas = document.getElementById("sim");
    const ctx = canvas.getContext("2d");

    const simSize = 100;
    const scale = canvas.width / simSize;
    const dt = 1;
    const maxAdjustTries = 8;
    const adjustmentStep = Math.PI / 4;

    const boundary = {
      minX: 0,
      maxX: simSize,
      minY: 0,
      maxY: simSize,
    };

    const entities = [];

    function addEntity(x, y, f1, f2) {
      entities.push({
        x,
        y,
        heading: 0,
        v: 0,
        omega: 0,
        f1,
        f2,
        radius: 1,
      });
    }

    function overlapsAny(e, testX, testY, testHeading) {
      // Check against boundaries
      if (
        testX - e.radius < boundary.minX ||
        testX + e.radius > boundary.maxX ||
        testY - e.radius < boundary.minY ||
        testY + e.radius > boundary.maxY
      ) {
        return true;
      }

      // Check against other entities
      for (let other of entities) {
        if (other === e) continue;
        const dx = testX - other.x;
        const dy = testY - other.y;
        const distSq = dx * dx + dy * dy;
        if (distSq < (2 * e.radius) * (2 * e.radius)) {
          return true;
        }
      }

      return false;
    }

    function simulate() {
      for (let e of entities) {
        const a1 = (e.f1 + e.f2);
        const a2 = (e.f2 - e.f1);

        e.v += a1 * dt;
        e.omega += a2 * dt;

        const originalHeading = e.heading;
        const originalX = e.x;
        const originalY = e.y;

        let foundValid = false;

        for (let i = 0; i <= maxAdjustTries; i++) {
          const delta = Math.floor((i + 1) / 2) * adjustmentStep * (i % 2 === 0 ? 1 : -1);
          const testHeading = originalHeading + delta;
          const testX = originalX + e.v * Math.cos(testHeading) * dt;
          const testY = originalY + e.v * Math.sin(testHeading) * dt;

          if (!overlapsAny(e, testX, testY, testHeading)) {
            e.heading = testHeading;
            e.x = testX;
            e.y = testY;
            foundValid = true;
            break;
          }
        }

        if (!foundValid) {
          e.v = 0;
          e.omega = 0;
        }
      }
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw simulation boundary
      ctx.strokeStyle = "black";
      ctx.strokeRect(0, 0, canvas.width, canvas.height);

      // Draw entities
      for (let e of entities) {
        ctx.beginPath();
        ctx.arc(e.x * scale, canvas.height - e.y * scale, e.radius * scale, 0, 2 * Math.PI);
        ctx.fillStyle = "steelblue";
        ctx.fill();
        ctx.stroke();
      }
    }

    function step() {
      simulate();
      draw();
      requestAnimationFrame(step);
    }

    // Initialize with one entity
    addEntity(10, 10, 2, 3);
    step();
  </script>
</body>
</html>
