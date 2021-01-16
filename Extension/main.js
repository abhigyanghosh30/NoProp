// document.body.style.border = "5px solid red";
var spans = document.getElementsByTagName("span");
for (var i = 0; i < spans.length; i++) {
  checkPara(spans[i].innerHTML, "s", i);
}
var paragraphs = document.getElementsByTagName("p");
for (let i = 0; i < paragraphs.length; i++) {
  checkPara(paragraphs[i].innerHTML, "p", i);
}

function checkPara(sentence = "", type = "p", index = 0) {
  fetch("http://localhost:5000", {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(sentence),
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (data["bool"] == "1") {
        if (type == "p") {
          paragraphs[index].style.color = "red";
          paragraphs[index].style.backgroundColor = "yellow";
        } else if (type == "s") {
          spans[index].style.color = "red";
          spans[index].style.backgroundColor = "yellow";
        }
      }
    });
}
