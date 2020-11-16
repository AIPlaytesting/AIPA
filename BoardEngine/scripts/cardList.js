var fs = require('fs');
const dbmanager = require('../scripts/dbmanager');

var filePath = '';
var appPath = '';
var deckFolderPath = '';
var cardFolderPath = '';

// call load database
function onLoadCardList() {
  dbmanager.loadDB(onFinishDBLoad);
}

// get path
function onFinishDBLoad() {
  let curGameName = dbmanager.getCurrentGameName();
  let curGameroot = dbmanager.getGameAppRoot(curGameName);
  let curResourcesRoot = dbmanager.getResourceRoot();
  filePath = curGameroot + '/';
  appPath = curResourcesRoot + '/'
  deckFolderPath = curGameroot + '/Decks/';
  cardFolderPath = curGameroot + '/Cards/';

  // display current app name
  let curapp = document.getElementById('curapp');
  curapp.innerHTML = curGameName;
  curapp.parentElement.style.fontStyle = 'italic';

  // display card information on load
  onLoadCards();
}

function onLoadCards() {
  const cards = document.getElementById('cards');
  // display card list
  let dir = fs.readdirSync(cardFolderPath);
  console.log(dir);

  // iterate through each card component and display
  for (let i = 0; i < dir.length; i++) {
    const div = document.createElement('div');
    div.className = 'col-3 mb-2';

    // get card object from db
    let data = fs.readFileSync(cardFolderPath + dir[i]);
    let cardObj = JSON.parse(data);
    // console.log(cardObj);

    // get card img path
    let cardImgFullPath = "../static/defaultcard.png";
    if ("img_relative_path" in cardObj) {
      let cardImgRelativePath = cardObj.img_relative_path;
      cardImgFullPath = dbmanager.getResourceRoot() + '\\' + cardImgRelativePath;
    }

    // form a component
    const imgDiv = createCard(
      cardImgFullPath,
      cardObj.name,
      cardObj.description,
      cardObj.energy_cost
    )

    // append to DOM tree
    div.appendChild(imgDiv);
    cards.appendChild(div);
  }

}

function createCard(imgPath, cardName, description, energy, onClickListener = undefined) {
  let frameWidth = '180'
  let textFrameWidth = '130'
  let framwHeight = '220'
  let cardFramePath = "../static/cardframe.png"

  let imgDiv = document.createElement('div');
  imgDiv.style.cursor = 'pointer';
  imgDiv.addEventListener('click', function(e) {
    e.preventDefault();
    window.location = `cards.html?cardName="${cardName}"`;
  })

  let imgElement = document.createElement('img');
  imgElement.id = 'cardImg';
  imgElement.src = imgPath;
  imgElement.width = frameWidth;
  imgElement.height = framwHeight;
  // imgElement.style.position = 'absolute';

  let cardFrame = document.createElement('img');
  cardFrame.id = 'cardFrame';
  cardFrame.src = cardFramePath;
  cardFrame.width = frameWidth;
  cardFrame.height = framwHeight;
  cardFrame.style.position = 'absolute';
  cardFrame.style.left = '10px';
  cardFrame.style.top = '0px';

  let nameText = document.createElement('span');
  nameText.innerText = cardName;
  nameText.className = 'text-center';
  nameText.style.width = textFrameWidth;
  nameText.style.position = 'absolute';
  nameText.style.top = '17px';
  nameText.style.left = '55px';
  nameText.style.color = 'white';
  nameText.style.fontWeight = 'bold';

  let energyText = document.createElement('span');
  energyText.innerText = energy;
  energyText.style.position = 'absolute';
  energyText.style.top = '0px';
  energyText.style.left = '21px';
  energyText.style.color = 'red';
  energyText.style.fontSize = '26px';
  energyText.style.fontWeight = 'bold';


  let descriptionText = document.createElement('p');
  descriptionText.innerText = description;
  descriptionText.className = 'text-center mr-5 ml-4';
  descriptionText.style.position = 'absolute';
  descriptionText.style.top = '120px';
  descriptionText.style.left = '5px';
  descriptionText.style.width = textFrameWidth;
  descriptionText.style.color = 'white';

  let hoverImgPath = '../static/noun_edit.png'
  let hoverSign = document.createElement('img');
  hoverSign.src = hoverImgPath;
  hoverSign.style.position = 'absolute';
  hoverSign.style.width = '70%';
  hoverSign.style.top = '15%';
  hoverSign.style.left = '15%';
  hoverSign.style.opacity = '0';
  hoverSign.addEventListener('mouseover', function() {
    hoverSign.style.opacity = '1';
    hoverSign.style.backgroundColor = 'rgba(1,0,0,0)';
    hoverSign.style.cursor = 'pointer';
  })
  hoverSign.addEventListener('mouseout', function() {
    hoverSign.style.opacity = '0';
    hoverSign.style.backgroundColor = 'rgbs(0,0,0,0)';
    hoverSign.style.cursor = 'default';
  })

  imgDiv.append(cardFrame, imgElement, nameText, energyText, descriptionText, hoverSign);
  return imgDiv
}