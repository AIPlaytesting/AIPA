var fs = require('fs');
// const { disconnect } = require('process');
var filePath = '../STP2/DATA/DefinitewinAPP/';
var appPath = '../../STP2/DATA/Resources/';
var deckFolderPath = '../STP2/DATA/DefinitewinAPP/Decks/';
var cardFolderPath = '../STP2/DATA/DefinitewinAPP/Cards/';
// var cardFolderPath = '';

// load cards and decks information to design page.
function onLoadDesign() {
  // read cards
  onLoadCards();
  // read deck
  onLoadDecks();
}

function onLoadCards() {
  const cards = document.getElementById('cards');
  fs.readdir(cardFolderPath, (err, files) => {
    if (err) throw err;
    files.forEach(file => {
      // div element
      const div = document.createElement('div');
      div.className = 'col-3 mb-5';
      // get image path
      fs.readFile(cardFolderPath + file, (err, data) => {
        if (err) throw err;
        let card = JSON.parse(data);
        console.log(card);
        let imgName = card['name'].replace(/\s/g, '').replace('Plus', '').toLowerCase();
        const imgPath = appPath + imgName + '.png';
        // console.log(imgPath);
        const energyCost = card['energy_cost'];
        const description = card['description'];
        // console.log(imgPath);
        // get image source from json file, then read image

        const imgDiv = document.createElement('div');
        imgDiv.className = 'row imgDiv';
        // const row = document.createElement('div');
        // row.className = 'row justify-content-center';
        const img = document.createElement('img');
        img.src = imgPath;
        img.width = '160';
        imgDiv.appendChild(img);

        const topLeft = document.createElement('div');
        topLeft.className = 'top-left';
        topLeft.innerHTML = energyCost;
        imgDiv.appendChild(topLeft);

        const bottomCenter = document.createElement('div');
        bottomCenter.className = 'bottom-center';
        bottomCenter.innerHTML = description;
        imgDiv.appendChild(bottomCenter);
        
        div.appendChild(imgDiv);
      });

      // Card name
      const row1 = document.createElement('div');
      row1.className = 'row justify-content-center';
      const card_name = file.slice(0, -5);
      const label = document.createElement('label');
      label.innerHTML = card_name;
      row1.appendChild(label);


      div.appendChild(row1);

      // Edit Button
      const row2 = document.createElement('div');
      row2.className = 'row justify-content-center';
      const a = document.createElement('a');
      a.className = 'ml-1 mb-1 btn btn-info';
      a.innerHTML = 'Edit';
      a.href = `cards.html?cardFolderPath="${cardFolderPath}"&cardName="${card_name}"`;
      row2.appendChild(a);

      // Delete card
      const icon = document.createElement('i');
      icon.className = 'material-icons';
      icon.innerHTML = 'delete';
      let btn = document.createElement('button');
      btn.className = 'ml-1 mb-1 btn btn-danger btn-sm';
      btn.onclick = deleteCard;
      btn.appendChild(icon);
      row2.appendChild(btn);

      // Add to deck
      btn = document.createElement('button');
      btn.className = 'ml-1 mb-1 btn btn-success';
      btn.innerHTML = '+ Deck';
      btn.onclick = addToDeck;
      row2.appendChild(btn);

      div.appendChild(row2);


      cards.appendChild(div);
    });
  });
}
function deleteCard() {
  console.log('delete card');
  const cardName = this.parentNode.parentNode.firstChild.firstChild.innerHTML;
  let cardFile = cardFolderPath + cardName + '.json';
  console.log(cardFile);
  try {
    fs.unlinkSync(cardFile)
    location.reload();
    //file removed
  } catch(err) {
    console.error(err)
  }
}
function addToDeck() {
  console.log('add to deck');
  // get card name
  const cardName = this.parentNode.parentNode.firstChild.firstChild.innerHTML;
  console.log(this.parentNode.parentNode.firstChild.firstChild.innerHTML);
  // add to deck
  // if card exist in deck, add amount by 1
  // else if card not exist in deck, create new element with card name and amount 1
  const form = document.getElementById('deckForm');
  console.log(form.children.length-1);
  // length - 1 for deducting save button
  const n = form.children.length
  let cardIsExist = false;
  for (let i = 0; i < n; i++) {
    if (cardIsExist) {
      break;
    }
    if (i == n - 1) {
      break;
    }
    console.log(form.children[i].firstChild.innerHTML);
    if (form.children[i].firstChild.innerHTML == cardName) {
      form.children[i].lastChild.firstChild.value = parseInt(form.children[i].lastChild.firstChild.value) + 1;
      form.children[i].lastChild.firstChild.style.backgroundColor = 'powderblue';
      cardIsExist = true;
    }
  }
  if (!cardIsExist) {
    const div = createDeckCard(cardName, 1);
    div.lastChild.firstChild.style.backgroundColor = 'powderblue';
    form.prepend(div);
  }
  // run saveButton function

}

function onLoadDecks() {
  const select = document.getElementById('decksSelect');
  // fill in deck select bar
  fs.readdir(deckFolderPath, (err, files) => {
    if (err) throw err;
    files.forEach(file => {
      file = file.slice(0, -5);
      const option = document.createElement('option');
      option.value = file;
      option.innerHTML = file;
      select.appendChild(option);
    });
    // read deck data
    readDeck();

    // save deck listener
    const form = document.getElementById('deckForm');
    form.addEventListener('submit', saveDeckBtn);
  });
}

function readDeck() {
  let deckName = document.getElementById('decksSelect').value;
  // console.log(deckName);
  if (deckName == '') {
    deckName = document.getElementById('decksSelect').firstChild.value;
  }
  deckJsonPath = `${deckFolderPath}${deckName}.json`;
  // console.log(deckJsonPath);
  fs.readFile(deckJsonPath, (err, data) => {
    if (err) throw err;
    let deck = JSON.parse(data);
    read(deck);
  });
}

// create html DOM tree under form node,
// then assign value from local json file.
function read(deck) {
  console.log(deck);
  // console.log(form);
  // set deck: create htmlDOM tree under table node, then assign value from local json file
  const form = document.getElementById('deckForm');
  console.log(form.children.length);
  // remove all children in form
  while (form.firstChild) {
    console.log(form.children.length);
    if (form.children.length == 1) {
      break;
    }
    form.removeChild(form.firstChild);
  }

  // create an array of card pair arrays, sort by 
  // 1. amount
  // 2. card name
  let entries = Object.entries(deck);
  entries = entries.sort(compare); 

  for (const [card_name, amount] of entries) {
    if (amount == 0) {
      continue;
    }
    let div = createDeckCard(card_name, amount);
    form.prepend(div);
  }
}

function createDeckCard(card_name, amount) {
  let div = document.createElement('div');
  div.className = 'form-group row pl-3';

  let label = document.createElement('label');
  label.className = 'col-sm-8 col-form-label';
  let labelText = document.createTextNode(card_name);
  label.appendChild(labelText);
  div.appendChild(label);

  let divInput = document.createElement('div');
  divInput.className = 'col-sm-4';
  let input = document.createElement('input');
  input.id = `buff_${card_name}_value`;
  input.type = 'number';
  input.name = `buff_${card_name}_value`;
  input.value = `${amount}`;
  input.className = 'form-control';
  input.setAttribute('onchange', 'indicator(this)');
  divInput.appendChild(input);
  div.appendChild(divInput);
  return div;
}

function indicator(obj) {
  console.log(obj);
  console.log(obj.id.split('_')[1]);
  console.log(obj.value);
  // get original json deck card data
  let deckName = document.getElementById('decksSelect').value;
  let deckJsonPath = `${deckFolderPath}${deckName}.json`;
  let data = fs.readFileSync(deckJsonPath);
  data = JSON.parse(data);
  console.log(data);
  // compare
  let entries = Object.entries(data);
  let isChanged = false;
  for (const [card_name, amount] of entries) {
    // console.log(card_name);
    // console.log(obj.id.split('_')[1]);
    // console.log(amount);
    // console.log(obj.value);
    if (card_name == obj.id.split('_')[1]) {
      if (amount != obj.value) {
        isChanged = true;
      }
    }
  }
  console.log(isChanged);
  if (isChanged) {
    document.getElementById(obj.id).style.backgroundColor = 'powderblue';
  } else {
    document.getElementById(obj.id).style.backgroundColor = 'white';
  }
}

function saveDeckBtn(e) {
  e.preventDefault();
  const form = document.getElementById('deckForm');
  console.log(form.children);
  // Get data from DOM
  let data = {};
  // iterate through deckForm and append key value pair
  let n = form.children.length
  for (let i = 0; i < n; i++) {
    if (i == n - 1) {
      break;
    }
    data[form.children[i].firstChild.innerHTML] = form.children[i].lastChild.firstChild.value;
    console.log(form.children[i]);
    console.log(form.children[i].firstChild.innerHTML);
    console.log(form.children[i].lastChild.firstChild.value);
  }
  console.log(data);
  // save into json
  // get file name from select bar, append to deckPath and write file.
  data = JSON.stringify(data, null, 2);
  const fileName = document.getElementById('decksSelect').value
  fs.writeFile(`${deckFolderPath}${fileName}.json`, data, (err) => {
    if (err) throw err;
    console.log('Deck written to file');
    alert('Deck written to file');
    location.reload();
  });
}

// sort by 1. amount 2. card name
function compare(a, b) {
  if (a[1] < b[1]) {
    return -1;
  }
  if (a[1] > b[1]) {
    return 1;
  }
  else {
    // return b[0] - a[0];
    return a[0] - b[0];
  }
}