var fs = require('fs');
var cardFolderPath = '';
var cardName = '';
var filePath = '../STP2/DATA/DefinitewinAPP/';
var imgPath = '../STP2/DATA/Resources/';

function onLoadCards() {
  // get parameters from html url query string, including cardFolderPath
  var parameters = location.search.substring(1).split("&");
  var temp = parameters[0].split('=');
  cardFolderPath = unescape(temp[1]).substring(1, unescape(temp[1]).length - 1);
  temp = parameters[1].split('=');
  cardName = unescape(temp[1]).substring(1, unescape(temp[1]).length - 1);
  // console.log(parameters);
  // console.log(temp);
  console.log(cardFolderPath);
  console.log(cardName);
  // append all cards in select options
  const select = document.getElementById('cardsSelect');
  fs.readdir(cardFolderPath, (err, files) => {
    if (err) throw err;
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
    if (!isNewCard) {
      readCard();
    } else {
      // remove select bar and label
      document.getElementById('cardsSelect').remove();
      document.getElementById('cardsSelectLabel').remove();
      // add buff 
      createBuffTable();
    }
  });

  // add eventListenser to write data into json file
  const form = document.getElementById('saveForm');
  form.addEventListener('submit', submitForm);
}

// submit to save into local json file
function submitForm(e) {
  e.preventDefault();
  let data = {
    "name": document.getElementById('name').value,
    "type": document.getElementById('type').value,
    "energy_cost": document.getElementById('energy_cost').value,
    "damage_target": document.getElementById('damage_target').value,
    "description": document.getElementById('description').value,
    // "img_relative_path": document.getElementById('img_relative_path').value,

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


  // image upload
  console.log(document.getElementById("image-file").files[0]);
  let name = document.getElementById('name').value;
  // remove 'Plus' from name if any for reference to the original png.
  let imgName = name.replace(/\s/g, '').replace('Plus', '').toLowerCase();
  // name = name.replace(' Plus', '');
  let uploadImgPath = document.getElementById("image-file").files[0].path;
  let saveImgPath = imgPath + imgName + '.png';
  console.log(saveImgPath);
  if (uploadImgPath != '') {
    fs.copyFile(uploadImgPath, saveImgPath, (err) => {
      if (err) throw err;
      console.log('File was copied to destination');
    });
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
    if (i == 0) {
      continue;
    }
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
    alert('Data written to file');
    location.reload();
  });
}

// get card data from DATA
function readCard() {

  let cardName = document.getElementById('cardsSelect').value;
  console.log(cardName);
  if (cardName == '') {
    cardName = document.getElementById('cardsSelect').firstChild.value;
  }
  cardPath = `${cardFolderPath}${cardName}.json`
  console.log(cardPath);
  fs.readFile(cardPath, (err, data) => {
    if (err) throw err;
    let card = JSON.parse(data);
    read(card);
  });
}

// set card by card json
function read(card) {
  console.log(card);
  let items = ['name', 'type', 'energy_cost', 'damage_target', 'description',
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
  // document.getElementById('img_relative_path').value = card.img_relative_path;
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
  let imgName = card['name'].replace(/\s/g, '').replace('Plus', '').toLowerCase();
  let dest = '../' + imgPath + imgName + '.png';
  console.log(dest);
  imgTag.src = dest;

  // set buff: create htmlDOM tree under table node, then assign value from local json file

  // console.log(typeof(card.buffs_info));
  // console.log(card.buffs_info);
  const table = document.getElementById('buff-table');
  while (table.firstChild) {
    table.removeChild(table.lastChild);
  }
  let tr = document.createElement('tr');
  heads = ['Buff Name', 'Value', 'Target']
  heads.forEach(head => {
    let th = document.createElement('th');
    th.innerHTML = head;
    tr.appendChild(th);
  });
  table.appendChild(tr);

  for (const [buff_name, value_target_pair] of Object.entries(card.buffs_info)) {
    if (value_target_pair['value'] == '0') {
      continue;
    }
    let tr = document.createElement('tr');
    let td = document.createElement('td');
    let label = document.createElement('label');
    let labelText = document.createTextNode(buff_name);
    label.appendChild(labelText);
    td.appendChild(label);
    tr.appendChild(td);

    td = document.createElement('td');
    let input = document.createElement('input');
    input.id = `buff_${buff_name}_value`;
    input.type = 'number';
    input.name = `buff_${buff_name}_value`;
    input.value = `${value_target_pair.value}`;
    input.setAttribute('onchange', 'indicator(this)');
    td.appendChild(input);
    tr.appendChild(td);

    td = document.createElement('td');
    let buff_target_select = document.createElement('select');
    buff_target_select.id = `buff_${buff_name}_target`;
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

    table.appendChild(tr);
  }
}

// if target value is not equal to original value, change background color
function indicator(obj) {
  // console.log(obj);
  // console.log(obj.id);
  // console.log(obj.value);

  // get card values from local json file
  let cardName = document.getElementById('cardsSelect').value;
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

function createBuffTable() {
  const table = document.getElementById('buff-table');
  // remove all previous table elements
  while (table.firstChild) {
    table.removeChild(table.lastChild);
  }
  // add table head to table's table row
  let tr = document.createElement('tr');
  heads = ['Buff Name', 'Value', 'Target']
  heads.forEach(head => {
    let th = document.createElement('th');
    th.innerHTML = head;
    tr.appendChild(th);
  });
  table.appendChild(tr);
}