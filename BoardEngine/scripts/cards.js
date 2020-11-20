var fs = require('fs');
const dbmanager = require('../scripts/dbmanager');
const library = require('../scripts/library');

var cardFolderPath = '';
var cardName = '';
var filePath = '../STP2/DATA/DefinitewinAPP/';
var appPath = '../STP2/DATA/Resources/';

function onLoadCards() {
  dbmanager.loadDB(onFinishDBLoad);
}

function onFinishDBLoad() {
  let curGameName = dbmanager.getCurrentGameName();
  let curGameroot = dbmanager.getGameAppRoot(curGameName);
  let curResourcesRoot = dbmanager.getResourceRoot();

  filePath = curGameroot + '/';
  appPath = curResourcesRoot + '/'
  // deckFolderPath = curGameroot + '/Decks/';
  cardFolderPath = curGameroot + '/Cards/';

  // display current app name
  let curapp = document.getElementById('curapp');
  curapp.innerHTML = curGameName;
  curapp.parentElement.style.fontStyle = 'italic';

  // get parameters from html url query string, including cardFolderPath
  var parameters = location.search.substring(1).split("&");
  var temp = parameters[0].split('=');
  cardName = unescape(temp[1]).substring(1, unescape(temp[1]).length - 1);

  // append all cards in select options
  let isNewCard = appendSelectCard();
  console.log(isNewCard);
  // if is new card, remove select element, and change name input readonly to false
  if (isNewCard) {
    document.getElementById('cardsSelect').remove();
    document.getElementById('cardsSelectLabel').remove();
    document.getElementById('name').readOnly = false;
    document.getElementById('name').className = 'form-control';
  }
  // read information
  readCard();

  // add eventListenser to write data into json file
  const form = document.getElementById('saveForm');
  form.addEventListener('submit', submitForm);
}

function readBuff(isNewCard, card) {
  // clean buffList on
  cleanBuffTable();
  // clear buffSelect on
  cleanBuffSelect();
  // append buffList o
  if (!isNewCard) {
    appendBuffList(card);
  }
  // append buffSelect on
  appendSelectBuff();

}
function appendBuffList(card) {
  console.log(card);
  // set buff: create htmlDOM tree under table node, then assign value from local json file

  // console.log(typeof(card.buffs_info));
  // console.log(card.buffs_info);
  const table = document.getElementById('buff-table');

  for (const [buff_name, value_target_pair] of Object.entries(card.buffs_info)) {
    if (value_target_pair['value'] == '0') {
      continue;
    }

    let buff = createBuff(buff_name, value_target_pair);
    table.appendChild(buff);
  }
}

// create buff row by its name and value target pair
// return tr elements
// name:buff name
// map: value, target pair
function createBuff(buff_name, value_target_pair) {
  let tr = document.createElement('tr');
  let td = document.createElement('td');
  let label = document.createElement('label');
  label.className = 'col-form-label';
  let labelText = document.createTextNode(buff_name);
  label.appendChild(labelText);
  td.appendChild(label);
  tr.appendChild(td);

  td = document.createElement('td');
  let input = document.createElement('input');
  input.id = `buff_${buff_name}_value`;
  input.className = 'form-control';
  input.type = 'number';
  input.name = `buff_${buff_name}_value`;
  input.value = `${value_target_pair.value}`;
  input.setAttribute('onchange', 'indicator(this)');
  td.appendChild(input);
  tr.appendChild(td);

  td = document.createElement('td');
  let buff_target_select = document.createElement('select');
  buff_target_select.id = `buff_${buff_name}_target`;
  buff_target_select.className = 'form-control';
  buff_target_select.name = `buff_${buff_name}_target`;
  buff_target_select.setAttribute('onchange', 'indicator(this)');
  options = ['self', 'enemy']
  options.forEach(option => {
    let opt = document.createElement('option');
    opt.value = option;
    opt.innerHTML = option;
    if (option == value_target_pair.target) {
      opt.selected = 'selected';
    }
    buff_target_select.appendChild(opt);
  });

  td.appendChild(buff_target_select)
  tr.appendChild(td);

  // create delete button to remove current row
  // td = document.createElement('td');
  // let 

  return tr;
}

function appendSelectCard() {
  const select = document.getElementById('cardsSelect');
  let files = fs.readdirSync(cardFolderPath);
  console.log(files);
  let isNewCard = true;
  files.forEach(file => {
    file = file.slice(0, -5);
    const option = document.createElement('option');
    option.value = file;
    option.innerHTML = file;
    // console.log(file);
    if (file == cardName) {
      // console.log(cardName);
      option.selected = 'selected';
      isNewCard = false;
    }
    select.appendChild(option);
  });
  // console.log(isNewCard);
  return isNewCard;
}

// submit to save into local json file
function submitForm(e) {
  e.preventDefault();

  // text validation check
  let nameElement = document.getElementById('name');
  if (nameElement.value == '') {
    console.log('Card name is required.');
    library.popupWarning('Card name is required. Please type a card name.');
    return;
  }
  if (!textIsValid(nameElement.value)) {
    console.log('Card name can only contain alphabet, number, and space.');
    library.popupWarning('Card name can only contain alphabet, number, and space.');
    nameElement.value = '';
    return;
  }

  // get input to object
  let data = {
    "name": document.getElementById('name').value,
    "type": document.getElementById('type').value,
    "energy_cost": document.getElementById('energy_cost').value,
    "damage_target": document.getElementById('damage_target').value,
    "description": document.getElementById('description').value,
    "img_relative_path": document.getElementById('img_relative_path').value,

    "damage_block_info": {
      "damage": document.getElementById('damage').value,
      "damage_instances": document.getElementById('damage_instances').value,
      "block": document.getElementById('block').value
    },

    "card_life_cycle_info": {
      "copies_in_discard_pile_when_played": document.getElementById('copies_in_discard_pile_when_played').value,
      "draw_card": document.getElementById('draw_card').value
    },
    "buffs_info": {},
    "special_modifiers_info": {
      "unique_damage": document.getElementById('unique_damage').value,
      "strength_multiplier": document.getElementById('strength_multiplier').value,
      "next_attack_count": document.getElementById('next_attack_count').value
    }
  };

  // upload image
  if (document.getElementById("image-file").files[0] !== undefined) {
    imgUpload(data);
  }

  // // image reload
  // let imgInput = document.getElementById("image-file");
  // var fReader = new FileReader();
  // fReader.readAsDataURL(imgInput.files[0]);
  // fReader.onloadend = function(event){
  //     var img = document.getElementById("card-img");
  //     img.src = event.target.result;
  // }

  //set up buff info
  // loop through the table tr, get first, second, and third tr element child's value,
  // form a obj to update data objs.
  let table = document.getElementById('buff-table');
  let trs = table.children;
  console.log(trs);
  for (let i = 0; i < trs.length; i++) {
    // if (i == 0) {
    //   continue;
    // }
    let buff_name = trs[i].firstChild.firstChild.innerHTML;
    console.log('buff_name = ' + buff_name);
    data['buffs_info'][buff_name] = {
      value: document.getElementById(`buff_${buff_name}_value`).value,
      target: document.getElementById(`buff_${buff_name}_target`).value
    }
  }
  // buff_data = fs.readFileSync(filePath + 'buffs.json');
  // buff_data = JSON.parse(buff_data);
  // console.log(buff_data['registered_buffnames']);
  // let registered_buffnames = buff_data['registered_buffnames'];

  // registered_buffnames.forEach(buff_name => {
  //   data['buffs_info'][buff_name] = {
  //     value: document.getElementById(`buff_${buff_name}_value`).value,
  //     target: document.getElementById(`buff_${buff_name}_target`).value
  //   }
  // });


  data = JSON.stringify(data, null, 2);
  const fileName = document.getElementById('name').value
  fs.writeFile(`${cardFolderPath}${fileName}.json`, data, (err) => {
    if (err) throw err;
    console.log('Data written to file');
    library.popupSuccess('Data has written to file.', function(){window.location = `cardList.html`});
  });
}


function imgUpload(data) {
  let imgName = data['img_relative_path'];
  let uploadImgPath = document.getElementById("image-file").files[0].path;
  let saveImgPath = appPath + imgName;
  console.log(saveImgPath);
  if (uploadImgPath != '') {
    fs.copyFile(uploadImgPath, saveImgPath, (err) => {
      if (err) throw err;
      console.log('File was copied to destination');
    });
  }
}

// get card data from DATA
function readCard() {
  let isNewCard = false;
  let card = '';
  if (document.getElementById('cardsSelect') == null) {
    console.log('new cards');
    isNewCard = true;
  }
  if (!isNewCard) {
    cardName = document.getElementById('cardsSelect').value;
    console.log(cardName);
    cardPath = `${cardFolderPath}${cardName}.json`;
    console.log(cardPath);
    let data = fs.readFileSync(cardPath);
    card = JSON.parse(data);
    // read by card json
    read(card);
  }

  // read buff
  readBuff(isNewCard, card);

}

// set card by card json
function read(card) {
  console.log(card);
  let items = ['name', 'type', 'energy_cost', 'damage_target', 'description', 'img_relative_path',
    'damage', 'damage_instances', 'block', 'copies_in_discard_pile_when_played',
    'draw_card', 'unique_damage', 'strength_multiplier', 'next_attack_count']
  for (i in items) {
    // console.log(items[i]);
    indicator(document.getElementById(items[i]));
  }
  document.getElementById('name').value = card.name;
  document.getElementById('type').value = card.type;
  document.getElementById('energy_cost').value = card.energy_cost;
  document.getElementById('damage_target').value = card.damage_target;
  document.getElementById('description').value = card.description;
  document.getElementById('img_relative_path').value = card.img_relative_path;
  document.getElementById('damage').value = card.damage_block_info.damage;
  document.getElementById('damage_instances').value = card.damage_block_info.damage_instances;
  document.getElementById('block').value = card.damage_block_info.block;
  document.getElementById('copies_in_discard_pile_when_played').value = card.card_life_cycle_info.copies_in_discard_pile_when_played;
  document.getElementById('draw_card').value = card.card_life_cycle_info.draw_card;
  document.getElementById('unique_damage').value = card.special_modifiers_info.unique_damage;
  document.getElementById('strength_multiplier').value = card.special_modifiers_info.strength_multiplier;
  document.getElementById('next_attack_count').value = card.special_modifiers_info.next_attack_count;

  // show image by setting the path to 
  let imgTag = document.getElementById('card-img');
  let imgName = card['img_relative_path'];
  let dest = appPath + imgName;
  console.log(dest);
  imgTag.src = dest;
}

// initialize selectBuff select bar
// put other buffs that are not added into current card into select bar
function appendSelectBuff() {
  const table = document.getElementById('buff-table');
  let trs = table.children;
  // get all buffs
  let data = fs.readFileSync(filePath + 'buffs.json');
  data = JSON.parse(data);
  let buffs = data['registered_buffnames'];
  // if in current buff table, continue
  // read all current buff from buff table
  let selectBuff = document.getElementById('selectBuff');
  const option = document.createElement('option');
  option.innerHTML = 'select buff to add here';
  option.selected = true;
  selectBuff.appendChild(option);

  for (let i = 0; i < buffs.length; i++) {
    let isExisted = false;
    for (let j = 0; j < trs.length; j++) {
      let buff_name = trs[j].firstChild.firstChild.innerHTML;
      if (buff_name == buffs[i]) {
        isExisted = true;
        break;
      }
    }
    if (!isExisted) {
      // add into select bar
      const option = document.createElement('option');
      option.value = buffs[i];
      option.innerHTML = buffs[i];
      selectBuff.appendChild(option);
    }
  }
}

function cleanBuffSelect() {
  const selectBuff = document.getElementById('selectBuff');
  while (selectBuff.firstChild) {
    selectBuff.removeChild(selectBuff.lastChild);
  }
}


// 1. add this buff info from select bar into buff table
// 2. delete this buff option from select bar
function addBuff() {
  // 1. add this buff info from select bar into buff table
  const buffName = document.getElementById('selectBuff').value;
  console.log(buffName);
  const table = document.getElementById('buff-table');
  let buff = createBuff(buffName, { "value": 0, "target": "enemy" });
  table.appendChild(buff);
  // 2. delete this buff option from select bar
  let selectBuff = document.getElementById('selectBuff');
  console.log(selectBuff.children.length);
  for (let i = 0; i < selectBuff.children.length; i++) {
    if (selectBuff.children[i].innerHTML == buffName) {
      selectBuff.children[i].remove();
      return;
    }
  }
}
// if target value is not equal to original value, change background color
function indicator(obj) {
  // console.log(obj);
  // console.log(obj.id);
  // console.log(obj.value);

  // get card values from local json file
  let cardName = '';
  if (document.getElementById('cardsSelect') == null) {
    return;
  }
  cardName = document.getElementById('cardsSelect').value;

  console.log(cardName);
  // console.log(cardName);
  cardPath = `${cardFolderPath}${cardName}.json`
  // console.log(cardPath);
  fs.readFile(cardPath, (err, data) => {
    if (err) throw err;
    let card = JSON.parse(data);
    // console.log(card);
    let defaultVal = card[obj.id];
    // console.log(defaultVal);
    // get default value from deeper in json file
    if (defaultVal === undefined) {
      // console.log(card['damage_block_info']);
      let infos = ['damage_block_info', 'card_life_cycle_info', 'special_modifiers_info']
      for (let i = 0; i < infos.length; i++) {
        if (obj.id in card[infos[i]]) {
          defaultVal = card[infos[i]][obj.id];
          break;
        }
      }
      // get buff default value based on obj.id
      if (obj.id.length >= 4 && obj.id.substring(0, 4) == 'buff') {
        let buff_infos = obj.id.split('_');
        let buff_name = buff_infos[1];
        let buff_value = buff_infos[2];
        defaultVal = card['buffs_info'][buff_name][buff_value];
      }
    }
    // if type is number, if value is text or is negative or is bigger than 100, 
    // alert and clear value
    let message = document.getElementById("message");
    if (obj.type == 'number') {
      try {
        if (obj.value == '') throw 'is Empty';
        if (isNaN(obj.value)) throw "not a number";
        if (obj.value > 100) throw "too high";
        if (obj.value < 0) throw "too low";
      }
      catch (err) {
        message.innerHTML = "Input " + err;
        obj.value = defaultVal;
      }
      // console.log(typeof(obj.value));
    }
    if (defaultVal != obj.value) {
      document.getElementById(obj.id).style.backgroundColor = 'powderblue';
    }
    else {
      document.getElementById(obj.id).style.backgroundColor = 'white';
    }
  });

}

function cleanBuffTable() {
  const table = document.getElementById('buff-table');
  // remove all previous table elements
  while (table.firstChild) {
    table.removeChild(table.lastChild);
  }
}

function addBuffTableHead() {
  const table = document.getElementById('buff-table');
  let tr = document.createElement('tr');
  heads = ['Buff Name', 'Value', 'Target']
  heads.forEach(head => {
    let th = document.createElement('th');
    th.innerHTML = head;
    tr.appendChild(th);
  });
  table.appendChild(tr);
}

function textIsValid(text) {
  let letterNumberSpace = /^[A-Za-z0-9 ]+$/i;
  if (text.match(letterNumberSpace) == null) {
    return false;
  }
  return true;
}