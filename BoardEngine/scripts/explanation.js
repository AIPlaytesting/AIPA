const gameLen =  ['This graph show the distributon of the length of the game',
'x value: how many card played before the game end',
'y value: the probability density of this game length',
'(PS: this probalility density is estimated by treating the card play numbers during playtest as random varibale)']

const endingMargin =  ['This graph show the distributon of how many hp of player/boss left when game end' ,
'x value: the hp value left when game end\n' ,
'y value: the probability density the x value\n' ,
'(PS: this probalility density is estimated by treating the hp left during playtest as random varibale)']


const cardUtil = ['card uilizations:','The value represent the probability of if AI will play this card, when this card is on the hand']

const cardPlayPos = ['card play position:',
'The value represent at which stage the card will be played in average',
'Small value means it will play early in one turn']

const cardPlayCount = ['card play count:',
'The value represent how many times the card is played during the playtest']

const anomalies = ['anomalies:','We record some games played during the playtest and visualize the process']

const pairsRelationship = ['pairs:','Heatmap of card-to-card relationship pairs','More red the block is, more frequent that pair is']

const triplesRelationship = ['triple:','Top 5 triple of cards which played most frequently']

module.exports ={gameLen,endingMargin,cardUtil,cardPlayPos,cardPlayCount,anomalies,pairsRelationship,triplesRelationship}