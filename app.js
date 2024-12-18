let boxes=document.querySelectorAll(".box");
let reset=document.querySelector("#reset");
let newgame=document.querySelector("#new");
let msgc=document.querySelector(".msgcon");
let msg=document.querySelector("#msg");

let turn0=true;
const winp=[
    [0,1,2],
    [0,3,6],
    [0,4,8],
    [1,4,7],
    [2,5,8],
    [3,4,5],
    [2,4,6],
    [6,7,8]
];
boxes.forEach((box)=>{
    box.addEventListener("click",()=>{
        //console.log("clicked");
        if(turn0){
            box.innerText="0";
            turn0=false;
            

        }
        else{
            box.innerText="X";
            turn0=true;
        }
        box.disabled=true;
        checkwinner();
    });
});
const disable=()=>{
    for(let box of boxes){
        box.disabled=true;
        box.innerText="";
    }
}
const enable=()=>{
    for(let box of boxes){
        box.disabled=false;
        box.innerText = ""; 
    }
}
const showwinner=(winner)=>{
    msg.innerText=`Congratulations Winner is ${winner}`;
    msgc.classList.remove("hide");
    disable();

}
const resetg=()=>{
    turn0=true;
    enable();
    msgc.classList.add("hide");

}


const checkwinner=()=>{
    for(let patterns of winp){
        //console.log(boxes.patterns[0].innerText,boxes.patterns[1].innerText,boxes.patterns[2].innerText);
        let pos1=boxes[patterns[0]].innerText;
        let pos2=boxes[patterns[1]].innerText;
        let pos3=boxes[patterns[2]].innerText;
        if(pos1!="" && pos2!="" && pos3!=""){
            if(pos1===pos2 && pos2===pos3){
                //console.log("Winner");
                showwinner(pos1);
            }
        }
    }
}
newgame.addEventListener("click",resetg);
reset.addEventListener("click",resetg);




