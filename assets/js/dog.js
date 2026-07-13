(function () {
  "use strict";

  var SPEED = 1.6; // px per frame
  var NAVBAR = 68; // clear the fixed navbar
  var PAD = 55; // viewport edge padding
  var FPS_TARGET = 60;

  var css = `
    #site-dog {
      position: fixed;
      z-index: 9000;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      pointer-events: auto;
      line-height: 1;
    }
    #site-dog.flipped { transform: scaleX(-1); }
    #site-dog-inner {
      display: block;
      font-size: 1.9rem;
      line-height: 1;
      transition: font-size 0.2s;
    }
    #site-dog.walking #site-dog-inner {
      animation: dogBob 260ms ease-in-out infinite alternate;
    }
    @keyframes dogBob {
      from { transform: translateY(0); }
      to   { transform: translateY(-5px); }
    }
    #site-dog.sitting #site-dog-inner {
      animation: dogBreath 2.4s ease-in-out infinite alternate;
    }
    @keyframes dogBreath {
      from { transform: scale(1); }
      to   { transform: scale(1.08); }
    }
    #site-dog.heart #site-dog-inner {
      animation: dogPop 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97);
    }
    @keyframes dogPop {
      0%   { transform: scale(1); }
      40%  { transform: scale(1.5); }
      70%  { transform: scale(0.9); }
      100% { transform: scale(1.2); }
    }
  `;

  var styleEl = document.createElement("style");
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // Outer: position + flip.  Inner: animation + emoji.
  var outer = document.createElement("div");
  outer.id = "site-dog";
  var inner = document.createElement("span");
  inner.id = "site-dog-inner";
  inner.textContent = "🐕";
  outer.appendChild(inner);
  document.body.appendChild(outer);

  var x = PAD + Math.random() * (window.innerWidth - PAD * 2);
  var y = NAVBAR + PAD + Math.random() * (window.innerHeight - NAVBAR - PAD * 2);
  var tx = x,
    ty = y;
  var mode = "idle"; // 'walk' | 'idle' | 'sit'
  var idleLeft = 0;
  var petting = false;

  function vw() {
    return window.innerWidth;
  }
  function vh() {
    return window.innerHeight;
  }

  function pickTarget() {
    tx = PAD + Math.random() * (vw() - PAD * 2);
    ty = NAVBAR + PAD + Math.random() * (vh() - NAVBAR - PAD * 2);
    mode = "walk";
    inner.textContent = "🐕";
    outer.classList.remove("sitting", "heart");
    outer.classList.add("walking");
  }

  function goIdle() {
    outer.classList.remove("walking", "heart");
    if (Math.random() < 0.4) {
      mode = "sit";
      inner.textContent = "🐶";
      outer.classList.add("sitting");
    } else {
      mode = "idle";
      inner.textContent = "🐕";
    }
    idleLeft = FPS_TARGET * (1.5 + Math.random() * 3.5); // 1.5–5 seconds
  }

  function tick() {
    if (!petting) {
      if (mode === "walk") {
        var dx = tx - x;
        var dy = ty - y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (d < SPEED + 0.5) {
          x = tx;
          y = ty;
          goIdle();
        } else {
          x += (dx / d) * SPEED;
          y += (dy / d) * SPEED;
          // face direction of travel
          if (dx < 0) outer.classList.add("flipped");
          else outer.classList.remove("flipped");
        }
      } else {
        if (--idleLeft <= 0) pickTarget();
      }
    }

    outer.style.left = Math.round(x) + "px";
    outer.style.top = Math.round(y) + "px";
    requestAnimationFrame(tick);
  }

  pickTarget();
  requestAnimationFrame(tick);

  // Petting
  outer.addEventListener("click", function () {
    if (petting) return;
    petting = true;
    outer.classList.remove("walking", "sitting");
    outer.classList.add("heart");
    inner.textContent = "❤️";
    setTimeout(function () {
      inner.textContent = "🐕";
      outer.classList.remove("heart");
      petting = false;
      pickTarget();
    }, 900);
  });
})();
