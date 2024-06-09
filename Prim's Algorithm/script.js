

//Prim's algorithm vars
var points = [];
var passedPoints = [];
var isFinished = true;// if false next iteration called
var totalCost = 0;
var startTime;

var canvas = document.getElementById("canvas");
var vecCanvas = document.getElementById("vecCanvas");
canvas.addEventListener("click", handleClick);


function handleClick(event) {
    const headline = document.getElementById('headline');
    var mouseX = event.offsetX;
    var mouseY = event.offsetY;

    headline.classList.add('fly-out-anim');
    points.push(new Point(mouseX, mouseY));
    if (points.length + passedPoints.length > 4) {
        primsAlgorithmStart();
    }
}

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        var point = document.createElement("point");
        point.style.position = "absolute";
        point.style.left = x - 25 + "px";
        point.style.top = y - 25 + "px";
        point.style.width = "50px";
        point.style.height = "50px";
        point.style.borderRadius = "50%";
        point.style.backgroundColor = "white";
        canvas.appendChild(point);
        this.object = point;
        console.log("point added at: " + this.x + ", " + this.y);
    }
}

function dist(point1, point2) {
    return Math.sqrt(Math.pow(point1.x - point2.x, 2) + Math.pow(point1.y - point2.y, 2));
}

function drawLine(point1, point2) {
    var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", point1.x);
    line.setAttribute("y1", point1.y);
    line.setAttribute("x2", point2.x);
    line.setAttribute("y2", point2.y);
    line.setAttribute("stroke", "white");
    line.setAttribute("stroke-width", "5")

    vecCanvas.appendChild(line);
}

function primsAlgorithmController() {
    if (!isFinished) { primsAlgorithm(); }
}

function primsAlgorithmStart() {
    isFinished = true;
    totalCost = 0;
    while (passedPoints.length > 0) {
        points.push(passedPoints.pop());
    }
    passedPoints.push(points.splice(0, 1)[0]);
    
    while (vecCanvas.firstChild) {
        vecCanvas.removeChild(vecCanvas.firstChild);
    }
    
    isFinished = false;
    // Start the timer
    startTime = performance.now();

    primsAlgorithmController();
}

//need to be called every iteration
function primsAlgorithm() {

    minDist = 100000;
    temp = [-1, -1];
    //console.log(passedPoints.length, points.length);
    for (var i = 0; i < passedPoints.length; i++) {
        for (var j = 0; j < points.length; j++) {
            //console.log(i + ", " + j + " d " + dist(passedPoints[i], points[j]));
            if (minDist > dist(passedPoints[i], points[j])) {
                minDist = dist(passedPoints[i], points[j]);
                temp = [i, j];
            }
        }
    }
    //console.log(temp);
    drawLine(passedPoints[temp[0]], points[temp[1]]);
    totalCost += minDist;

    passedPoints.push(points.splice(temp[1], 1)[0]);

    if (points.length < 1) {
        isFinished = true;
        primsAlgorithmFinish();
        return 0;
    }
    primsAlgorithmController();
}


function primsAlgorithmFinish() {
    var resultsP = document.getElementById("results");
    const endTime = performance.now();
    var elapsedTime = endTime - startTime;
    elapsedTime = Math.ceil(elapsedTime * 10 ** 3) / 10 ** 3;
    totalCost = Math.ceil(totalCost);

    console.log("Elapsed time: " + elapsedTime + " milliseconds, " + "total cost: " + totalCost);
    resultsP.innerHTML = ("Elapsed time: " + elapsedTime + " milliseconds, " + "total cost: " + totalCost);
}