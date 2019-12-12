ID = Math.round(Math.random() * (999999-99999) + 100000) //genereerib kasutajale suvalise kuuekohalise ID
socket = null
var yhendatud = false

function yhendus(ip){
    console.log(ip)
    try{
        console.log("Üritan ühendada...");
        socket = new WebSocket("ws://"+ip+":8765");
        console.log("Ühendatud");

        socket.onopen = function () {
            socket.send(ID+": Tere server!"); 
        }
        socket.onmessage = function (event) {
            if (event.data == "Tere "+ID){
                document.getElementById("inputkirjeldus").innerText = "Kasutajanimi"
                yhendatud = true}
            console.log(event.data);
        }
    }
    catch (err){
        document.getElementById("inputkirjeldus").innerText = "Error"
        console.log(err)

    }
}



function kasutajanimi(nimi){
    socket.send(ID+": Minu nimi on "+nimi);
}

function submitvajutus(sisend){
    document.getElementById("submitnupp").disabled = true
    setTimeout(() => {
        document.getElementById("submitnupp").disabled = false
    }, 1000);
    if (!yhendatud){
        yhendus(sisend)
    }
    else {kasutajanimi(sisend)}
}
var input = document.getElementById("sisend");

nupuvajutus = function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("submitnupp").click()
    }
};
input.addEventListener("keyup", function(event){
    if (event) {nupuvajutus(event)}})

