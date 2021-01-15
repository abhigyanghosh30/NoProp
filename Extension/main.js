var paragraphs = document.getElementsByTagName("p");
for (var i = 0; i < paragraphs.length; i++) {
  if (paragraphs[i].innerHTML.includes("hate")) {
    paragraphs[i].style.color = "red";
    paragraphs[i].style.backgroundColor = "yellow";
  }
}
var spans = document.getElementsByTagName("span");
for (var i = 0; i < spans.length; i++) {
  if (spans[i].innerHTML.includes("hate")) {
    spans[i].style.color = "red";
    spans[i].style.backgroundColor = "yellow";
  }
}
