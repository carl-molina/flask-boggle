"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.game_id;
  let board = gameData.board;

  displayBoard(board);
}







/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure

  // TODO: use jQuery to create board
  // For loop y values
  //    for loop x values
}


start();