let people =[];
function Person(name,id,age,weight,height,iq){
    this.name=name;
    this.id =id;
    this.age=age;
    this.weight=weight;
    this.height=height;
    this.iq=iq;
    people.push(this);
    
};



let p1 = new Person("Kalana",12,23,234,32,1);

console.log(people);






