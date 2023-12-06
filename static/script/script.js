(function() {
  var lastTime = 0;
  var vendors = ['webkit', 'moz'];
  for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
      window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
      window.cancelAnimationFrame =
        window[vendors[x]+'CancelAnimationFrame'] || window[vendors[x]+'CancelRequestAnimationFrame'];
  }

  if (!window.requestAnimationFrame)
      window.requestAnimationFrame = function(callback, element) {
          var currTime = new Date().getTime();
          var timeToCall = Math.max(0, 16 - (currTime - lastTime));
          var id = window.setTimeout(function() { callback(currTime + timeToCall); },
            timeToCall);
          lastTime = currTime + timeToCall;
          return id;
      };

  if (!window.cancelAnimationFrame)
      window.cancelAnimationFrame = function(id) {
          clearTimeout(id);
      };
}());

/*

The code above is from: http://www.paulirish.com/2011/requestanimationframe-for-smart-animating/

For more information go there.

*/
var canvas = document.getElementById("canvas"),
  ctx = canvas.getContext("2d");

canvas.width = 700;
canvas.height = 350;

var iNumber = 0, 
  iPlayer_1Hei = 90,
  iPlayer_1YPos = 25,
  iPlayer_1XPos = 20,
  iPlayer_1Speed = 15,
  bPlayer_1MovingUp = false,
  bPlayer_1MovingDown = false,
  iPlayer_2Hei = 90,
  iPlayer_2YPos = 25,
  iPlayer_2XPos = canvas.width - 20,
  iPlayer_2Speed = 15,
  bPlayer_2MovingUp = false,
  bPlayer_2MovingDown = false,
  iBallX = 50,
  iBallY = 150,
  iBallStartSpeed = 6,
  iXBallSpeed = iBallStartSpeed,
  iYBallSpeed = iXBallSpeed,
  iPoints_1 = 0,
  iPoints_2 = 0;

fnGamePlay();
function fnGamePlay(){
canvas.width = canvas.width;
fnDrawPlayer_1();
fnDrawPlayer_2();
fnDrawBall();
fnCalc();
fnPoints();
window.requestAnimationFrame(fnGamePlay);
}

window.addEventListener("keydown", function(ev){
if(ev.keyCode == 87) {
  if(bPlayer_1MovingUp === false) {
    if(bPlayer_1MovingDown === true) {
      clearInterval(Player_1MoveInterval);
    }
    bPlayer_1MovingUp = true;
    Player_1MoveInterval = setInterval(function(){
      iPlayer_1YPos -= iPlayer_1Speed;
      if(iPlayer_1YPos < 15) {
        iPlayer_1YPos = 15;
      }
    }, 23);
  }
}
if(ev.keyCode == 83) {
  if(bPlayer_1MovingDown === false) {
    if(bPlayer_1MovingUp === true) {
      clearInterval(Player_1MoveInterval);
    }
    bPlayer_1MovingDown = true;
    Player_1MoveInterval = setInterval(function(){
      iPlayer_1YPos += iPlayer_1Speed;
      if(iPlayer_1YPos + iPlayer_1Hei >= canvas.height - 15) {
        iPlayer_1YPos = canvas.height - iPlayer_1Hei - 15;
      }
    }, 23);
  }
}
if(ev.keyCode == 38) {
  if(bPlayer_2MovingUp === false) {
    if(bPlayer_2MovingDown === true) {
      clearInterval(Player_2MoveInterval);
    }
    bPlayer_2MovingUp = true;
    Player_2MoveInterval = setInterval(function(){
      iPlayer_2YPos -= iPlayer_2Speed;
      if(iPlayer_2YPos < 15) {
        iPlayer_2YPos = 15;
      }
    }, 23);
  }
}
if(ev.keyCode == 40) {
  if(bPlayer_2MovingDown === false) {
    if(bPlayer_2MovingUp === true) {
      clearInterval(Player_2MoveInterval);
    }
    bPlayer_2MovingDown = true;
    Player_2MoveInterval = setInterval(function(){
      iPlayer_2YPos += iPlayer_2Speed;
      if(iPlayer_2YPos + iPlayer_2Hei >= canvas.height - 15) {
        iPlayer_2YPos = canvas.height - iPlayer_2Hei - 15;
      }
    }, 23);
  }
}
}, false);

window.addEventListener("keyup", function(ev){
if(ev.keyCode == 87) {
  bPlayer_1MovingUp = false;
  clearInterval(Player_1MoveInterval);
}
if(ev.keyCode == 83) {
  bPlayer_1MovingDown = false;
  clearInterval(Player_1MoveInterval);
}
if(ev.keyCode == 38) {
  bPlayer_2MovingUp = false;
  clearInterval(Player_2MoveInterval);
}
if(ev.keyCode == 40) {
  bPlayer_2MovingDown = false;
  clearInterval(Player_2MoveInterval);
}
}, false);

function fnDrawPlayer_1() {
ctx.beginPath();
ctx.moveTo(iPlayer_1XPos, iPlayer_1YPos);
ctx.lineTo(iPlayer_1XPos, iPlayer_1YPos + iPlayer_1Hei);
ctx.lineWidth = 13;
ctx.strokeStyle = "white";
ctx.stroke();
}

function fnDrawPlayer_2() {
ctx.beginPath();
ctx.moveTo(iPlayer_2XPos, iPlayer_2YPos);
ctx.lineTo(iPlayer_2XPos, iPlayer_2YPos + iPlayer_2Hei);
ctx.lineWidth = 13;
ctx.strokeStyle = "white";
ctx.stroke();
}

function fnDrawBall() {
ctx.beginPath();
ctx.moveTo(iBallX, iBallY);
ctx.lineTo(iBallX + 15, iBallY);
ctx.lineWidth = 15;
ctx.stroke();
}

function fnPoints() {
document.getElementById("player_1").innerHTML = iPoints_1;
document.getElementById("player_2").innerHTML = iPoints_2;
}

function fnCalc() {
iBallX += iXBallSpeed;
iBallY += iYBallSpeed;
if(iBallX + 15 > canvas.width) {
  fnWait();
  iPoints_1 += 1;
}
if(iBallY + 22.5 > canvas.height) {
  iYBallSpeed = -iYBallSpeed;
}
if(iBallX < 0) {
  fnWait();
  iPoints_2 += 1;
}
if(iBallY < 22.5) {
  iYBallSpeed = -iYBallSpeed;
}
if(iXBallSpeed < 0 && iBallX < 50 ||
   iXBallSpeed > 0 && iBallX > canvas.width - 50) {
  if ((iBallX < iPlayer_1XPos + 7.5 &&
      iBallX + 15  > iPlayer_1XPos &&
      iBallY < iPlayer_1YPos + iPlayer_1Hei / 3 &&
      iBallY + 15 > iPlayer_1YPos ||
      iBallX < iPlayer_2XPos + 15 &&
      iBallX + 15  > iPlayer_2XPos &&
      iBallY < iPlayer_2YPos + iPlayer_2Hei / 3 &&
      iBallY + 15 > iPlayer_2YPos) &&
      !(iYBallSpeed >= 2 || iYBallSpeed <= -2) &&
      !(iXBallSpeed >= 2 || iXBallSpeed <= -2)) {
    ++iYBallSpeed;
    --iXBallSpeed;
  }
  else if (iBallX < iPlayer_1XPos + 7.5 &&
           iBallX + 15  > iPlayer_1XPos &&
           iBallY < iPlayer_1YPos + 2 * (iPlayer_1Hei / 3) &&
           iBallY + 15 > iPlayer_1YPos + iPlayer_1Hei / 3 ||
           iBallX < iPlayer_2XPos + 15 &&
           iBallX + 15  > iPlayer_2XPos &&
           iBallY < iPlayer_2YPos + 2 * (iPlayer_2Hei / 3) &&
           iBallY + 15 > iPlayer_2YPos + iPlayer_2Hei / 3) {
    --iYBallSpeed;
    ++iXBallSpeed;
  }
  else if ((iBallX < iPlayer_1XPos + 7.5 &&
           iBallX + 15  > iPlayer_1XPos &&
           iBallY < iPlayer_1YPos + 3 * (iPlayer_1Hei / 3) &&
           iBallY + 15 > iPlayer_1YPos + 2 * (iPlayer_1Hei / 3) ||
           iBallX < iPlayer_2XPos + 15 &&
           iBallX + 15  > iPlayer_2XPos &&
           iBallY < iPlayer_2YPos + 3 * (iPlayer_2Hei / 3) &&
           iBallY + 15 > iPlayer_2YPos + 2 * (iPlayer_1Hei / 3)) &&
           !(iYBallSpeed >= 2 || iYBallSpeed <= -2) &&
           !(iXBallSpeed >= 2 || iXBallSpeed <= -2)) {
    ++iYBallSpeed;
    --iXBallSpeed;
  }
  console.log("y: " + iYBallSpeed);
  console.log("x: " + iXBallSpeed);
  if (iBallX < iPlayer_1XPos + 7.5 &&
      iBallX + 15  > iPlayer_1XPos &&
      iBallY < iPlayer_1YPos + iPlayer_1Hei &&
      iBallY + 15 > iPlayer_1YPos ||
      iBallX < iPlayer_2XPos + 15 &&
      iBallX + 15  > iPlayer_2XPos &&
      iBallY < iPlayer_2YPos + iPlayer_2Hei &&
      iBallY + 15 > iPlayer_2YPos) {
    iXBallSpeed = -iXBallSpeed;
  }
}
}

function fnWait() {
iXBallSpeed = -iXBallSpeed;
waitInterval = setInterval(function(){
  iNumber += 1;
  iBallX = canvas.width / 2;
  iBallY = canvas.height / 2;
  if(iNumber >= 100) {
    clearInterval(waitInterval);
    iXBallSpeed = iBallStartSpeed;
    iYBallSpeed = iBallStartSpeed;
    iNumber = 0;
  }
}, 10);
}