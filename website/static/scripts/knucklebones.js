container = document.getElementsByClassName('knc-game-container')[0]
    


    function init() {
        spawnMainMenu()
    }

    function spawnMainMenu() {
      container.innerHTML = `
    <h3 class="knc-title" align="center">⚅	⚅	⚅</h3>
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
        <button type="submit" action="joinLobby()">Join</button>  
    `;
    }
    
    function spawnGameMenu() {
      container.innerHTML = `
      <div class="game-flex-container">
      <div class="knc-player-title grid-container">
              <h3 align="center" id="PlayerName1">Waiting for Player to Join</h3>
              <h4 align="center" id="PlayerScore1">0</h4>
              <div class="grid-item player1" id="diceroller">X</div>
      </div>
              <div class="grids-container">
                      <div class="grid-container">
                              <div class="grid-item player1 col1" id=3>3</div>
                              <div class="grid-item player1 col2" id=3>3</div>
                              <div class="grid-item player1 col3" id=3>3</div>
                              <div class="grid-item player1 col1" id=2>2</div>
                              <div class="grid-item player1 col2" id=2>2</div>
                              <div class="grid-item player1 col3" id=2>2</div>
                              <div class="grid-item player1 col1" id=1>1</div>
                              <div class="grid-item player1 col2" id=1>1</div>
                              <div class="grid-item player1 col3" id=1>1</div>
                      </div>
              
                      <div class="grid-container">
                              <div class="grid-item player2 col1" id=1>1</div>
                              <div class="grid-item player2 col2" id=1>1</div>
                              <div class="grid-item player2 col3" id=1>1</div>
                              <div class="grid-item player2 col1" id=2>2</div>
                              <div class="grid-item player2 col2" id=2>2</div>
                              <div class="grid-item player2 col3" id=2>2</div>
                              <div class="grid-item player2 col1" id=3>3</div>
                              <div class="grid-item player2 col2" id=3>3</div>
                              <div class="grid-item player2 col3" id=3>3</div>
                      </div>
              </div>
      <div  class="knc-player-title">
              <div class="grid-item player2" id="diceroller">X</div>
              <h3 align="center" id="PlayerName2">Waiting for Player to Join</h3>
              <h4 align="center" id="PlayerScore2">0</h4>
      </div>
</div>
    `;
    }

    var socket = io();
    function joinLobby() {
      var player = document.getElementById("username").value; 
      var room = document.getElementById("room-id").value;
      spawnGameMenu()
      socket.emit('join', {Player: player, Room: room}, (response) => {
        console.log(response)
        player = response[0]
      });
      }
      socket.on('PlayerJoined', (response) => {
        console.log(response)
        if (response.length > 1) {
          document.getElementById("PlayerName2").innerText = response[1]
        }
        document.getElementById("PlayerName1").innerText = response[0]
      })
      socket.on("newturn", (response) => {
        console.log(response)
        activeplayer = response[0]
        document.getElementsByClassName("player"+activeplayer).getElementById("diceroller").innerText=response[2]
      })

      socket.on("update-board", (response) =>{
        console.log(response)
      })