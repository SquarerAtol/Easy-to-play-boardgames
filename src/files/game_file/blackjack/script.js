let cards = [];
let suits = ["♣", "♥", "♠", "♦"];
let roundValue = 0;
let playerIsStanding = false;
let comIsStanding = false;
let comRoundValue = 0;
let readyToStart = false;

createDeck();
function createDeck() {
  for (i = 0; i < suits.length; i++) {
    for (j = 2; j < 11; j++) {
      cards.push({
        suit: suits[i],
        value: j
      });
    }
    //face cards
    //a
    cards.push({
      suit: suits[i],
      value: 'A'
    });
    //j
    cards.push({
      suit: suits[i],
      value: 'J'
    });
    //q
    cards.push({
      suit: suits[i],
      value: 'Q'
    });
    //k
    cards.push({
      suit: suits[i],
      value: 'K'
    });
  }
}
function drawCard() {
  if (cards.length == 0) {
    createDeck();
  }
  let index = Math.floor(Math.random() * cards.length);
  let thisCard = cards[index];
  cards.splice(index, 1);

  return thisCard;
}
function addCardToHand(card) {
  let addedValue = 0;
  let newCard = document.createElement("div");
  newCard.setAttribute("class", "card");
  newCard.innerText = card.value + "\n" + card.suit;
  if(card.suit == "♥" || card.suit == "♦"){
    newCard.style.color = "red";
  }

  document.getElementById("myHand").appendChild(newCard);  

  if (card.value == 'J' || card.value == 'Q' || card.value == 'K') {
    addedValue = 10;
  } else if (card.value == 'A') {
    //do ace
    document.getElementById("aceBox").style.display = "flex";
  } else {
    addedValue = card.value;
  }
  roundValue += addedValue;

  checkRound();
}
function setAceValue(val) {
  addedValue = val;
  roundValue += addedValue;
  document.getElementById("aceBox").style.display = "none";

  checkRound();
}
function checkRound() {
  if (roundValue > 21) {
    //player bust
    document.getElementById("outcome").innerText = "You bust!";
    endRound();
    playerIsStanding = true;
    comIsStanding = true;
    document.getElementById("comHand").style.background = "#42e442";
  }
  if(comRoundValue > 21){
    //com bust
    document.getElementById("outcome").innerText = "Computer bust!";
    endRound();
    playerIsStanding = true;
    comIsStanding = true;
    document.getElementById("myHand").style.background = "#42e442";
  }
  document.getElementById("roundValue").innerText = roundValue;

  if (comRoundValue > 16) {
    if (Math.random() < (0.5 + (comRoundValue / 100) + .6)) {
      comIsStanding = true;
    }
  }
  
  if (!comIsStanding) {
    setTimeout(() => {
      comDraw(drawCard());
    }, 500);
  }

  if(playerIsStanding && comIsStanding){
    endRound();
  }
}
function endRound() {
  playerIsStanding = true;
  

  if(comIsStanding){
    if(roundValue > comRoundValue && roundValue < 22){
      //player win
      document.getElementById("outcome").innerText = "You win!";
      document.getElementById("myHand").style.background = "#42e442";
    }
    if(comRoundValue > roundValue && comRoundValue < 22){
      //com win
      document.getElementById("outcome").innerText = "Computer win!";
      document.getElementById("comHand").style.background = "#42e442";
    }
    let comCards = document.getElementsByClassName("comCard");
    for(j = 0; j < 5; j ++){
      for(i = 0; i < comCards.length; i ++){
        comCards[i].classList.remove("comCard");
      }
    }
    document.getElementById("comRoundValue").innerText = comRoundValue;
    if(readyToStart){
      document.getElementById("myHand").innerHTML = "";
      roundValue = 0;
      addedValue = 0;
      document.getElementById("comHand").innerHTML = "";
      comRoundValue = 0;
      comAddedValue = 0;
      document.getElementById("roundValue").innerText = roundValue;
      document.getElementById("comRoundValue").innerText = "?";
      playerIsStanding = false;
      comIsStanding = false;
      readyToStart = false;
      document.getElementById("myHand").style.background = "rgba(255, 255, 255, 0.5)";
      document.getElementById("comHand").style.background = "rgba(255, 255, 255, 0.5)";
    }
  } else {
    comDraw(drawCard());
  }
}
function comDraw(card) {
  let comAddedValue = 0;
  let newCard = document.createElement("div");
  newCard.classList.add("card");
  newCard.innerText = card.value + "\n" + card.suit;
  if(card.suit == "♥" || card.suit == "♦"){
    newCard.style.color = "rgb(194, 35, 35)";
  }
  newCard.classList.add("comCard");

  document.getElementById("comHand").appendChild(newCard);

  if (card.value == 'J' || card.value == 'Q' || card.value == 'K') {
    comAddedValue = 10;
  } else if (card.value == 'A') {
    if (Math.random() < .5) {
      comAddedValue = 1;
    } else {
      comAddedValue = 11;
    }
  } else {
    comAddedValue = card.value;
  }
  comRoundValue += comAddedValue;

  if(playerIsStanding){
    setTimeout(checkRound, 500);
  }
}
function reset(){
  readyToStart = true;
  endRound();
}