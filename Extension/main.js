// document.body.style.border = "5px solid red";
// var spans = document.getElementsByTagName("span");
// for (var i = 0; i < spans.length; i++) {
//   checkPara(spans[i].innerHTML, "s", i);
// }
var paragraphs = document.getElementsByTagName("p");
let full_article = "";
for (let i = 0; i < paragraphs.length; i++) {
  full_article += paragraphs[i].innerText;
}

fetch("http://localhost:5000", {
  method: "POST",
  mode: "cors",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(full_article),
})
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    if (data["bool"] == "1") {
      window.alert(
        "This page may contain malicious content. Use your discretion"
      );
    }
  });
