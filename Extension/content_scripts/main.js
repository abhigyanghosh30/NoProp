// document.body.style.border = "5px solid red";
// var spans = document.getElementsByTagName("span");
// for (var i = 0; i < spans.length; i++) {
//   checkPara(spans[i].innerHTML, "s", i);
// }
browser.storage.local.get({ NoProp: false }, (items) => {
  if (items.NoProp) {
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
      body: JSON.stringify({
        article: full_article,
        source: window.location.origin,
      }),
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        if (data["bool"] == "1") {
          window.alert(
            "This page may contain propaganda/false news. Use your discretion before continuing.. You can turn off NoProp in the extension bar if you wish to not see these messages again"
          );
        }
      });
  }
});
