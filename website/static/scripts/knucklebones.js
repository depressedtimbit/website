


function init() {
        container = document.getElementsByClassName('knc-game-container')[0]
        spawnMainMenu()
    }

    function spawnMainMenu() {
      container.innerHTML = 
  `<h3 class="knc-title" align="center">⚅	⚅	⚅</h3>
    <h1 class="knc-title" align="center">Knucklebones</h1>
    <h3 class="knc-title" align="center">A Online game of risk and reward</h3>

        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="Enter username"
          />
        </div>
        <div class="form-group">
          <label for="room-id">Room ID</label>
          <input
            type="text"
            id="room-id"
            name="room-id"
            placeholder="room-id"
          />
        </div>
        <button type="submit" onclick="joinLobby();">Join</button>  
    `;
    }
    
    function spawnGameMenu() {

      container.innerHTML = `
      <div class="game-flex-container">
      <div class="knc-player-title ">
              <h3 align="center" id="PlayerName1">Waiting for Player to Join</h3>
              <h4 class="block" align="center" id="0ps">0</h4>
              <div class="grid-item block player1" id="diceroller0">X</div>
      </div>
        <div class="knc-board">
        <div class="grid-container">
                <div class="knc-col" onclick="progressTurn(0);">
                  <div class="grid-item player1 block col1" id=002>002</div>
                  <div class="grid-item player1 block col1" id=001>001</div>
                  <div class="grid-item player1 block col1" id=000>000</div>
                  <div class="grid-item player1 block col1 score" id=00s>00s</div>
                  <div class="grid-item spacer block col1"></div>
                  <div class="grid-item player2 block col1 score" id=10s>10s</div>
                  <div class="grid-item player2 block col1" id=100>100</div>
                  <div class="grid-item player2 block col1" id=101>101</div>
                  <div class="grid-item player2 block col1" id=102>102</div>
                  </div>
                  <div class="knc-col" onclick="progressTurn(1);">
                  <div class="grid-item player1 block col2" id=012>012</div>
                  <div class="grid-item player1 block col2" id=011>011</div>
                  <div class="grid-item player1 block col2" id=010>010</div>
                  <div class="grid-item player1 block col2 score" id=01s>01s</div>
                  <div class="grid-item spacer block col2"></div>
                  <div class="grid-item player2 block col2 score" id=11s>11s</div>
                  <div class="grid-item player2 block col2" id=110>110</div>
                  <div class="grid-item player2 block col2" id=111>111</div>
                  <div class="grid-item player2 block col2" id=112>112</div>
                  </div>
                  <div class="knc-col" onclick="progressTurn(2);">
                  <div class="grid-item player1 block col3" id=022>022</div>
                  <div class="grid-item player1 block col3" id=021>021</div>
                  <div class="grid-item player1 block col3" id=020>020</div>
                  <div class="grid-item player1 block col3 score" id=02s>02s</div>
                  <div class="grid-item spacer block col3"></div>
                  <div class="grid-item player2 block col3 score" id=12s>12s</div>
                  <div class="grid-item player2 block col3" id=120>120</div>
                  <div class="grid-item player2 block col3" id=121>121</div>
                  <div class="grid-item player2 block col3" id=122>122</div>
                  </div>
            </div>
      </div>
      <div  class="knc-player-title">
      <div class="grid-item block " id="diceroller1">X</div>
      <h3 align="center" id="PlayerName2">Waiting for Player to Join</h3>
      <h4 class="block" align="center" id="1ps">0</h4>
      </div>
    </div>
</div>
    `;
    }

    var socket = io();
    function joinLobby() {
      player = document.getElementById("username").value; 
      room = document.getElementById("room-id").value;
      spawnGameMenu()
      socket.emit('join', {Player: player, Room: room}, (response) => {

        console.log(response)

        player = response
      });
      }
    socket
    socket.on('PlayerJoined', (response) => {
        console.log(response)
        document.getElementById("PlayerName1").innerText = response[0]
        if (response.length > 1) {
          document.getElementById("PlayerName2").innerText = response[1]
          if (player == 0) {startLobby();}
        }
      })
    socket.on("newturn", (response) => {
        activeplayer = response[0]
        document.getElementById('diceroller'+(activeplayer)).innerText=response[1]
        document.getElementById('diceroller'+(-activeplayer+1)).innerText='X'
      })
      
      socket.on("update-board", (response) =>{
        console.log(response)
        for (board = 0; board < response.length; board++) {
          var pscore = 0
          for (row = 0; row < response[board].length; row++) {
            document.getElementById(''+board+row+0).innerText=response[board][row][0]
            document.getElementById(''+board+row+1).innerText=response[board][row][1]
            document.getElementById(''+board+row+2).innerText=response[board][row][2]
            list=[response[board][row][0], response[board][row][1], response[board][row][2]]
            var hist = {};
            var score = 0
            list.map( function (a) { if (a in hist) hist[a] ++; else hist[a] = 1; } );
            console.log(hist)
            for (var key in hist) {
              console.log((key*hist[key])*hist[key]);
              score += (key*hist[key])*hist[key]
            }
            document.getElementById(''+board+row+'s').innerText=score
            pscore += score
          }
        document.getElementById(''+board+'ps').innerText = pscore
        } 
      })
    function startLobby() {
      socket.emit('startLobby', {Player: player, Room: room});
    }
    function progressTurn(choice) {
      socket.emit('progressTurn', {Player: player, Room: room, Choice: choice});
    }