
const inputElement = document.getElementById("dataField");

const button = document.getElementById("encode-btn");
button.addEventListener("click", controller);

const treeDiv = document.getElementById("tree-div");

const resultsP = document.getElementById("results");

function controller() {
    while (treeDiv.firstChild) {
        treeDiv.removeChild(treeDiv.firstChild);
    }
    const data = inputElement.value;
    if (data.length < 1) {
        alert("You should write something");
        return;
    }
    const frequency = calculateFrequency(data);
    const root = buildHuffmanTree(frequency);

    const codes = {};
    assignCodesWithDrawing(root, "", codes, 1);

    console.log(encodeData(data, codes));


    var textEncoder = new TextEncoder();
    var encodedBytes = textEncoder.encode(data);
    var spaceOccupied = encodedBytes.length * 8;

    resultsP.innerHTML = "Without encoding: " + spaceOccupied + "bits, with encoding: " + encodeData(data, codes).length + "bits";

    
}

function calculateFrequency(data) {
    const frequency = {};
    for (let i = 0; i < data.length; i++) {
        if (frequency[data[i]]) {
            frequency[data[i]]++;
        } else {
            frequency[data[i]] = 1;
        }
    }
    return frequency;
}

class Node {
    constructor(symbol, frequency) {
        this.symbol = symbol;
        this.frequency = frequency;
        this.left = null;
        this.right = null;
    }
}

function buildHuffmanTree(frequency) {
    const priorityQueue = [];
    // Create a node for each symbol and add it to the priority queue
    for (let symbol in frequency) {
        priorityQueue.push(new Node(symbol, frequency[symbol]));
    }

    // Build the Huffman Tree
    while (priorityQueue.length > 1) {
        priorityQueue.sort((a, b) => a.frequency - b.frequency);

        const leftChild = priorityQueue.shift();
        const rightChild = priorityQueue.shift();

        const parentNode = new Node(null, leftChild.frequency + rightChild.frequency);
        parentNode.left = leftChild;
        parentNode.right = rightChild;

        priorityQueue.push(parentNode);
    }

    // Return the root of the Huffman Tree
    return priorityQueue[0];
}

function assignCodesWithDrawing(root, currentCode, codes, pos) {
    var i = currentCode.length;
    var maxPos = Math.pow(2, i) + 1;

    var point = document.createElement("point");
    point.style.position = "absolute";
    point.style.left = 100 / maxPos * pos + "vw";
    point.style.top = 300 + i * 100 + "px";
    point.style.width = "50px";
    point.style.height = "50px";
    point.style.borderRadius = "50%";
    point.style.backgroundColor = "lightblue";
    point.style.border = "1px solid black";
    point.style.textAlign = "center";
    point.className = "nodePoint";
    point.style.zIndex = '1';

    
    point.addEventListener('mouseover', function() {
        point.style.zIndex = '2'; /* Bring the object to the front */
  });
  
  point.addEventListener('mouseout', function() {
    point.style.zIndex = '1'; /* Restore the original z-index value */
  });

    var text = document.createElement("p");

    if (root.symbol == null) {
        text.innerHTML = root.frequency;
    }
    else {
        text.innerHTML = "<b>'" + root.symbol + "'</b>" + "|" + root.frequency ;
        point.style.backgroundColor = "#D8BFD8";
    } 
    point.append(text);
    treeDiv.appendChild(point);
    if (root.symbol !== null) {
        codes[root.symbol] = currentCode;
        return;
    }

    assignCodesWithDrawing(root.left, currentCode + "0", codes, pos * 2 - 1);
    assignCodesWithDrawing(root.right, currentCode + "1", codes, pos * 2);
}

function assignCodes(root, currentCode, codes) {
    if (root.symbol !== null) {
        codes[root.symbol] = currentCode;
        return;
    }

    assignCodes(root.left, currentCode + "0", codes);
    assignCodes(root.right, currentCode + "1", codes);
}

// Function to encode data using Huffman codes
function encodeData(data, codes) {
    let encodedData = "";
    for (let i = 0; i < data.length; i++) {
        encodedData += codes[data[i]];
    }
    return encodedData;
}

// Function to decode data using Huffman Tree
function decodeData(encodedData, root) {
    let decodedData = "";
    let currentNode = root;

    for (let i = 0; i < encodedData.length; i++) {
        if (encodedData[i] === "0") {
            currentNode = currentNode.left;
        } else {
            currentNode = currentNode.right;
        }

        if (currentNode.symbol !== null) {
            decodedData += currentNode.symbol;
            currentNode = root;
        }
    }

    return decodedData;
}



const addTextBtn = document.getElementById("add-text-btn");
addTextBtn.addEventListener("click", createText);

currentText = -1;
function createText() {

    if (Math.random() < 0.3 && currentText != 1) {
        inputElement.value = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nam aliquam sem et tortor consequat id porta nibh. Eget gravida cum sociis natoque penatibus et magnis. Ut pharetra sit amet aliquam. Purus ut faucibus pulvinar elementum. Et pharetra pharetra massa massa ultricies mi. Non tellus orci ac auctor augue mauris augue neque gravida. Malesuada fames ac turpis egestas sed tempus urna. Sed faucibus turpis in eu mi bibendum neque egestas congue. Tellus rutrum tellus pellentesque eu tincidunt tortor aliquam nulla facilisi. Praesent elementum facilisis leo vel fringilla est. Vulputate mi sit amet mauris commodo quis. Massa eget egestas purus viverra accumsan in.";
        currentText = 1;
    }
    else if (Math.random() < 0.3 && currentText != 2){
        inputElement.value = "artehg8wqtr74g543248hg74w5rhb247/hy3*+97+ 4ef4q1/*1  g43qgfv q43v1q348+-hgbvq3";
        currentText = 2;
    }
    else if (currentText == 4 || (Math.random() < 0.3 && currentText != 3)) {
        inputElement.value = "I started painting as a hobby when I was little. I didn't know I had any talent. I believe talent is just a pursued interest. Anybody can do what I do. Just go back and put one little more happy tree in there. Everybody's different. Trees are different. Let them all be individuals. We'll put some happy little leaves here and there. These things happen automatically. All you have to do is just let them happen. Everyone wants to enjoy the good parts - but you have to build the framework first. Let's do that again. I'm gonna start with a little Alizarin crimson and a touch of Prussian blue. The very fact that you're aware of suffering is enough reason to be overjoyed that you're alive and can experience it. If you do too much it's going to lose its effectiveness. If you don't think every day is a good day - try missing a few. You'll see. In life you need colors. Fluff it up a little and hypnotize it.  We can fix anything. Automatically, all of these beautiful, beautiful things will happen. There we go. Look at them little rascals.";
        
    }
    else {
        inputElement.value = "Arabica Acerbic Affogato Aftertaste Aged Americano And Aroma, bar panna so Barista cortado trifecta extraction, skinny aftertaste filter java cultivar cinnamon. Mazagran trade Barista french and Acerbic acerbic Aged milk cinnamon origin carajillo, mountain coffee roast mug wings Bar single viennese pumpkin go pot, dripper crema flavour mocha At bar sit medium au breve. Espresso Brewed Blue iced Americano robust whipped, bar percolator  grounds go saucer robusta, Au shop Affogato Bar aged coffee, Barista blue strong origin aftertaste. Blue skinny coffee breve Brewed acerbic, siphon steamed And foam, qui Arabica ut latte. Go brewed At aftertaste sweet cinnamon caffeine rich strong caramelization Aftertaste, Body roast body frappuccino Beans extraction sit americano Aroma.";
        currentText = 4;
    }
}

