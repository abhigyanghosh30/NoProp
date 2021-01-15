document.body.style.border = "5px solid red";
var spans = document.getElementsByTagName("span");
for (var i = 0; i < spans.length; i++) {
  if (spans[i].innerHTML.includes("propaganda")) {
    spans[i].style.color = "red";
    spans[i].style.backgroundColor = "yellow";
  }
}
var paragraphs = document.getElementsByTagName("p");
for (let i = 0; i < paragraphs.length; i++) {
  checkPara(paragraphs[i].innerHTML);
}

function checkPara(data = "") {
  fetch("http://localhost:5000", {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((res) => {
      res.json();
    })
    .then((res) => {
      console.log(res);
    });
}
