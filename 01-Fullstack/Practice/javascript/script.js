let player = {
    name : "Kalana",
    fun : 0,
    health : 100,
    eatApple : function () {
       this.health += 10;
    },
    eatCandy : function() {
        this.health += 10;
        this.fun -= 10;
    },
    play : function () {
        this.fun += 10;
    },
    getStat : function() {
        console.log("player name : "+this.name);
        console.log("Player health = "+ this.health);
        console.log("Fun = "+ this.fun);
    }

};

player.eatApple();
player.eatCandy();
player.play();
player.play();
player.eatApple();
player.eatApple();

player.getStat();