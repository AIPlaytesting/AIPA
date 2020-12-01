const dbmanager = require('../scripts/dbmanager')
const rootPath = require('electron-root-path').rootPath
const cardRenderer = require('../scripts/cardRenderer')
const utils = require('../scripts/utils')
const pagePlaytest = require('../scripts/pagePlaytest')
const pageTrain = require('../scripts/pageTrain')

const PythonProcess = require('../Scripts/pythonProcess.js')

var currentGameData = {}
var cardsToAdd = []

function refreshLibraryPage() {
    console.log("refresh!")
    dbmanager.loadDB(onFinishDBLoad)
}

function onFinishDBLoad() {
    let installedGames = dbmanager.getInstalledGameApps()
    // fill game lib list
    let gameEntryList = $("#game-entry-list")
    gameEntryList.text("")
    for (gameName of installedGames) {
        gameEntryList.append(createLibraryEntry(gameName))
    }
    // set game create button
    gameEntryList.append(createNewGameBtn())

    updateGameTemplateList()

    $('#create-new-game-btn').off()
    $('#create-new-game-btn').click(function () { onClickCreateNewGame() })

    // refresh all pages
    updateDesignPage()
    updatePlaytestPage()
    updateTrainPage()

    function updateGameTemplateList() {
        let gameTemplateList = $("#game-template-list");
        gameTemplateList.text("");
        $('#game-template-dropdown').text("please select a template")
        for (gameName of installedGames) {
            // create game template option button
            let templateOptionBtn = $(document.createElement('button'))
            templateOptionBtn.attr('class', 'dropdown-item')
            templateOptionBtn.text(gameName)
            templateOptionBtn.click(function () {
                $('#game-template-dropdown').text($(this).text())
            })
            gameTemplateList.append(templateOptionBtn)
        }
    }
}

function onClickPlay() {
    let child = require('child_process').execFile;
    let executablePath = rootPath + '/executables/unitybuild/AIPA.exe';
    console.log('launch unity at: ' + executablePath)
    child(executablePath, function (err, data) {
        if (err) {
            console.error(err);
            return;
        }

        console.log(data.toString());
    });
}

function onClickTrain() {
    pageTrain.startTrain(dbmanager.getCurrentGameName(), currentGameData.rules.deck)
}

function onClickCreateNewGame() {
    let templateName = $('#game-template-dropdown').text()
    let newGameName = $('#new-game-name-input').val()
    if (newGameName == "") {
        popupWarning("game name cannot be empty!")
        return
    }

    try {
        dbmanager.createNewGame(templateName, newGameName, refreshLibraryPage)
    } catch (error) {
        popupWarning(error)
    }
}

function onClickCreateNewDeck() {
    let templateName = $('#deck-template-dropdown').text()
    let newDeckName = $('#new-deck-name-input').val()
    if (newDeckName == "") {
        popupWarning("deck name cannot be empty!")
        return
    }

    try {
        dbmanager.createNewDeckOnCurrentGame(templateName, newDeckName)
        refreshLibraryPage()
        onSwitchCurrentDeck(newDeckName)
    } catch (error) {
        popupWarning(error)
    }
}

function onClickAddNewCard() {
    let deckname = currentGameData.rules.deck
    for (let cardname of cardsToAdd) {
        let newCardCopies = 1
        if (cardname in currentGameData.decks[deckname]) {
            newCardCopies = currentGameData.decks[deckname][cardname] + 1
            currentGameData.decks[deckname][cardname] = newCardCopies
        }
        dbmanager.modifyDeck(deckname, cardname, newCardCopies)
    }
    refreshLibraryPage()
}

function onClickRemoveCard(cardname) {
    let deckname = currentGameData.rules.deck
    let newCardCopies = 1
    if (cardname in currentGameData.decks[deckname]) {
        newCardCopies = currentGameData.decks[deckname][cardname] - 1
        if (newCardCopies < 0) {
            newCardCopies = 0
        }
        dbmanager.modifyDeck(deckname, cardname, newCardCopies)
        refreshLibraryPage()
    }
    else {
        console.log(cardname + 'doesnt exist!')
    }
}

function onClickLibraryGameEntry(gameName) {
    dbmanager.setCurrentGame(gameName)
    refreshLibraryPage()
}

function onClickRemoveGame() {
    let currentGameName = dbmanager.getCurrentGameName()
    console.log("game to delete: " + currentGameName)
    popupConfirmDialog("Calm down",
        "are you sure to delete: " + currentGameName,
        function () {
            try {
                dbmanager.removeGame(currentGameName, refreshLibraryPage)
            }
            catch (error) {
                popupWarning(error)
            }
        }
    )
}

function onClickPlaytest() {
    pagePlaytest.onClickPlaytest()
}

function viewPlaytestData(gamename, deckname, trainVersion) {
    pagePlaytest.viewPlaytestData(gamename, deckname, trainVersion)
}

function onSwitchCurrentDeck(deckName) {
    console.log("switch to: " + deckName)
    if (deckName != currentGameData.rules.deck) {
        dbmanager.updateGameData(dbmanager.getCurrentGameName(), "currentDeck", deckName, refreshLibraryPage)
    }
}

function createLibraryEntry(gameName) {
    let entryBtn = $(document.createElement('button'))
    entryBtn.text(gameName)
    entryBtn.attr('class', "btn btn-light tab-v")
    entryBtn.click(function () {
        $(".tab-v").removeClass('active')
        $(this).addClass('active')
        onClickLibraryGameEntry(gameName)
    })
    return entryBtn
}

function createNewGameBtn() {
    let container = $(document.createElement('div'))
    let entryBtn = $(document.createElement('button'))
        .text("+")
        .attr('class', "btn btn-dark")
        .attr('data-toggle', 'modal')
        .attr('data-target', '#create-game-modal')
        .css('width', '50px')
        .css('position', 'absolute')
        .css('right', '0px')
        .addClass('text-center')
    container.append(entryBtn)
    return container;
}

// update main page based on current game in manifest
function updateDesignPage() {
    let gameName = dbmanager.getCurrentGameName()
    currentGameData = dbmanager.loadGameData(gameName)
    let gameData = currentGameData
    // lock the deck edit if it is locked 
    if (gameData.rules.locked_decks.includes(gameData.rules.deck)) {
        $('#game-edit-section-overlay').removeClass('d-none')
    }
    else {
        $('#game-edit-section-overlay').addClass('d-none')
    }
    $('#game-title').text(gameName)
    updateGameSettingSection()

    utils.setupDropdown('newcard-name-list', 'newcard-name-dropdown', Object.keys(gameData.cards))
    utils.setupDropdown('deck-template-list', 'deck-template-dropdown', Object.keys(gameData.decks))

    updateDeckDropdown()

    renderCardGrid()

    function updateGameSettingSection() {
        $('#deck-count').text(Object.keys(gameData.decks).length)
        $('#card-count').text(Object.keys(gameData.cards).length)
        $('#buff-count').text(gameData.buffInfo.registered_buffnames.length)

        // set up playter hp edit
        $('#player-hp-input')
            .val(gameData.rules.player_hp)
            .off()
            .change(function () {
                $('#player-hp-save-btn').removeClass('d-none')
                $('#player-hp-undo-btn').removeClass('d-none')
                $(this).css('background-color', '#f6f7ba').css('color', 'red')
            })

        $('#player-hp-save-btn')
            .off()
            .click(function () {
                dbmanager.updateGameData(currentGameData.gameName, "playerHP", $('#player-hp-input').val())
                $('#player-hp-input').css('color', '').css('background-color', '')
                $('#player-hp-save-btn').addClass('d-none')
                $('#player-hp-undo-btn').addClass('d-none')
            }
            )

        $('#player-hp-undo-btn')
            .off()
            .click(function () {
                $('#player-hp-input').val(gameData.rules.player_hp)
                $('#player-hp-input').css('color', '').css('background-color', '')
                $('#player-hp-save-btn').addClass('d-none')
                $('#player-hp-undo-btn').addClass('d-none')
            }
            )

        // set up boss hp edit
        $('#boss-hp-input')
            .val(gameData.rules.boss_hp)
            .off()
            .change(function () {
                $('#boss-hp-save-btn').removeClass('d-none')
                $('#boss-hp-undo-btn').removeClass('d-none')
                $(this).css('background-color', '#f6f7ba').css('color', 'red')
            })


        $('#boss-hp-save-btn')
            .off()
            .click(function () {
                dbmanager.updateGameData(currentGameData.gameName, "bossHP", $('#boss-hp-input').val())
                $('#boss-hp-input').css('color', '').css('background-color', '')
                $('#boss-hp-save-btn').addClass('d-none')
                $('#boss-hp-undo-btn').addClass('d-none')
            }
            )

        $('#boss-hp-undo-btn')
            .off()
            .click(function () {
                $('#boss-hp-input').val(gameData.rules.boss_hp)
                $('#boss-hp-input').css('color', '').css('background-color', '')
                $('#boss-hp-save-btn').addClass('d-none')
                $('#boss-hp-undo-btn').addClass('d-none')
            }
            )
    }

    function renderCardGrid() {
        let deckImgView = $('#deck-img-view')
        deckImgView.text("")
        let currentDeckinfo = gameData.decks[gameData.rules.deck]
        // create card info
        let currentImgRow = $(document.createElement('div'))
        currentImgRow.attr('class', "row")
        let currentImgRowCount = 0
        let maxImgRowCount = 6
        for (let cardName in currentDeckinfo) {
            if (gameData.cards[cardName] == undefined) {
                console.error(cardName + ' is undefined in cards')
                continue
            }

            let cardCopies = currentDeckinfo[cardName]
            let cardImgFullPath = "../static/defaultcard.png"
            if ("img_relative_path" in gameData.cards[cardName]) {
                let cardImgRelativePath = gameData.cards[cardName].img_relative_path
                cardImgFullPath = dbmanager.getResourceRoot() + '\\' + cardImgRelativePath
            }

            for (i = 0; i < cardCopies; i++) {
                // check row change
                if (currentImgRowCount >= maxImgRowCount) {
                    deckImgView.append(currentImgRow)
                    currentImgRow = $(document.createElement('div'))
                    currentImgRow.attr('class', "row")
                    currentImgRowCount = 0
                }
                currentImgRowCount += 1
                // render card
                let cardObj = gameData.cards[cardName]
                let imgDiv = cardRenderer.createCardElement(
                    cardImgFullPath,
                    cardName,
                    cardObj.description,
                    cardObj.energy_cost,
                    '../static/delete.png',
                    function () { onClickRemoveCard(cardName) })
                currentImgRow.append(imgDiv)
            }
        }
        // add create new card buttons

        // check row change
        if (currentImgRowCount >= maxImgRowCount) {
            deckImgView.append(currentImgRow)
            currentImgRow = $(document.createElement('div'))
            currentImgRow.attr('class', "row")
            currentImgRowCount = 0
        }
        currentImgRow.append(createAddNewCardDiv())

        // add the last row 
        deckImgView.append(currentImgRow)
    }

    function createAddNewCardDiv() {
        let rootDiv = $(document.createElement('div'))
            .attr('class', 'col-2')
        let addCardImg = $(document.createElement('img'))
            .attr('src', '../static/add.png')
            .css('width', '100%')
            .css('height', '70%')
        let addCardBtn = $(document.createElement('button'))
            .attr('class', 'btn')
            .css('width', '160px')
            .css('height', '220px')
            .attr('data-toggle', 'modal')
            .attr('data-target', '#add-card-modal')
            .append(addCardImg)
            .click(function () {
                updateAddCardModal()
            })
        rootDiv.append(addCardBtn)
        return rootDiv
    }

    function updateAddCardModal() {
        // clear previous info
        $('#add-card-modal-grid').text("")
        $("#added-card-pool").text("")
        cardsToAdd = []
        // draw card grid
        for (let cardName of Object.keys(gameData.cards)) {
            let cardElement = cardRenderer.createCardElementByName(
                gameData.gameName,
                cardName,
                "../static/noun_add.png",
                function () {
                    let cardToAdd = cardRenderer.createCardElementByName(gameData.gameName, cardName)
                        .attr("class", "col-1")
                    $("#added-card-pool").append(cardToAdd)
                    cardsToAdd.push(cardName)
                })

            cardElement.attr('class', 'col-3')
            $('#add-card-modal-grid').append(cardElement)
        }
    }

    function updateDeckDropdown() {
        $('#current-deck-name').text(currentGameData.rules.deck)
        let deckList = $('#current-deck-dropdown-list')
        deckList.text("")

        for (let deckName in currentGameData.decks) {
            let deckSwitchBtn = $(document.createElement('button'))
            deckSwitchBtn.text("switch to: " + deckName)
            deckSwitchBtn.click(function () { onSwitchCurrentDeck(deckName) })
            deckSwitchBtn.attr('class', 'dropdown-item')
            deckList.append(deckSwitchBtn)
        }

        // create deck btn
        let createDeckBtn = $(document.createElement('button'))
            .attr('data-toggle', 'modal')
            .attr('data-target', '#create-deck-modal')
            .text('+ New')
            .attr('class', "dropdown-item")
            .css('color', "green")
        deckList.append(createDeckBtn)

        // del deck btn
        let deleteDeckBtn = $(document.createElement('button'))
            .text('+ Delete Current Deck')
            .attr('class', "dropdown-item")
            .css('color', "red")
            .click(function () {
                popupConfirmDialog("Calm down",
                    "are you sure to delete deck: " + currentGameData.rules.deck,
                    function () {
                        try {
                            dbmanager.removeDeckSync(currentGameData.gameName,currentGameData.rules.deck)
                            refreshLibraryPage()
                        }
                        catch (error) {
                            popupWarning(error)
                        }
                    }
                )
            })

        deckList.append(deleteDeckBtn)
    }
}

function updatePlaytestPage() {
    pagePlaytest.updatePlaytestPage()
}

function updateTrainPage() {
    let gameName = dbmanager.getCurrentGameName()
    let deckName = dbmanager.loadGameData(gameName).rules.deck
    pageTrain.updateTrainPageView(gameName, deckName)
}

function popupWarning(message) {
    $('#warning-modal').modal()
    $('#warning-modal-body').text(message)
}

function popupSuccess(message, onConfirmCallback) {
    $('#success-modal').modal()
    $('#success-modal-body').text(message)
    $('#success-modal-confirm-btn').off()
    $('#success-modal-confirm-btn').click(function () {
        console.log("call back!")
        onConfirmCallback()
    })
}

function popupConfirmDialog(title, message, onConfirmCallback) {
    $('#confirm-modal').modal()
    $('#confirm-modal-title').text(title)
    $('#confirm-modal-body').text(message)
    $('#confirm-model-confirm-btn').off()
    $('#confirm-model-confirm-btn').click(function () {
        console.log("call back!")
        onConfirmCallback()
    })
}

module.exports = {
    popupConfirmDialog,
    popupWarning,
    popupSuccess
}