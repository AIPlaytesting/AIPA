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
        const imgPath = appPath + card['img_relative_path'];
        // console.log(imgPath);
        // get image source from json file, then read image
        const row = document.createElement('div');
        row.className = 'row justify-content-center';
        const img = document.createElement('img');
        img.src = imgPath;
        row.appendChild(img);
        div.appendChild(row);
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
      a.className = 'ml-1 btn btn-info';
      a.innerHTML = 'Edit';
      a.href = `cards.html?cardFolderPath="${cardFolderPath}"&cardName="${card_name}"`;
      row2.appendChild(a);

      div.appendChild(row2);

      cards.appendChild(div);
    });
  });
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

// 
function readDeck() {
  let deckName = document.getElementById('decksSelect').value;
  // console.log(deckName);
  if (deckName == '') {
    deckName = document.getElementById('decksSelect').firstChild.value;
  }
  deckJsonPath = `${deckFolderPath}${deckName}.json`
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
  // entries.sort((a, b) => parseInt(a[1]) - parseInt(b[1]));
  // console.log(entries);
  // console.log(entries[0]);
  // console.log(entries[0][1]);
  // console.log(entries[1]);
  // console.log(entries[1][1]);
  // console.log(entries[2]);
  // console.log(entries[2][1]);
  
  for (const [card_name, amount] of entries) {

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
    divInput.appendChild(input);
    div.appendChild(divInput);

    form.prepend(div);

    // input.setAttribute('onchange', 'indicator(this)');
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