/* function  sendSignal(){
    console.log("Help!!!");
}

let i = 0;

while(i<1000){
    sendSignal();
    i++;
} 

let total =0;
let j= 1;
while(j <= 10){
    total +=j;;
    console.log("Total : "+ total);
    j++;

} 

let distance = 0;
let fuel = 1000;

while(fuel > 0){
    if(distance == 500){
        break;
    }

    // Only increase distance if within 100 to 200
    if(distance >= 100 && distance <= 200){
        distance++;   // increment distance only if in range
    }

    fuel--; // always decrease fuel
}

console.log("Distance Traveled: " + distance);
console.log("Fuel Consumed: " + (1000 - fuel)); 

let population = 100;
let years=0;

while(years<10){
    population *= 1.05;
    years++;
}

console.log(years);
console.log(population); */

let population = 100;


for(let years =0; years< 10; years++){
    population *= 1.05;
}

console.log(population);