browser.storage.local.get({ NoProp: false }, (items) => {
  if (items.NoProp) {
    var card = document.createElement("div");
    card.id = "NoPropCard";
    card.classList.add("card");
    card.classList.add("w-25");
    card.classList.add("sticky-top");
    card.classList.add("position-absolute");
    card.classList.add("p-3");
    card.innerHTML = "<h2>NoProp Stats</h2><hr/>";

    var sourceName = document.createElement("div");
    sourceName.innerHTML = "Source: " + window.location.origin;
    var sourceBias = document.createElement("div");
    sourceBias.innerHTML = "<strong>Political Bias</strong>: Fetching...";
    var sourceFact = document.createElement("div");
    sourceFact.innerHTML =
      "<strong>MBFC Factuality Label</strong>: Fetching...";

    var closeButton = document.createElement("div");
    closeButton.innerHTML =
      '<button class="btn btn-primary" id="NoPropStatClose">Close</button>';

    card.appendChild(sourceName);
    card.appendChild(sourceBias);
    card.appendChild(sourceFact);
    card.appendChild(closeButton);

    document.body.appendChild(card);

    var paragraphs = document.getElementsByTagName("p");
    let full_article = "";
    for (let i = 0; i < paragraphs.length; i++) {
      full_article += paragraphs[i].innerText;
    }
    console.log(full_article);
    fetch("http://localhost:8000", {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        article: [full_article],
        source: window.location.origin,
      }),
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        if (data["valid"] == false) {
          sourceBias.innerHTML = "Source Bias Not Available";
          sourceFact.innerHTML = "Source Fact Not Available";
          return;
        }

        // alerts here
        sourceFact.innerHTML =
          "<strong>MBFC Factuality Label</strong>: " + data["fact"];
        sourceBias.innerHTML =
          "<strong>Political Bias</strong>: " + data["bias"];
        if (data["prop"] == "1") {
          window.alert(
            "This page may contain Propaganda. Use your discretion before continuing.. You can turn off NoProp in the extension bar if you wish to not see these messages again"
          );
        }

        if (data["liar"] == "1") {
          window.alert(
            "This page may contain Fake News. Use your discretion before continuing.. You can turn off NoProp in the extension bar if you wish to not see these messages again"
          );
        }
      });
  }
});
document.addEventListener("click", (e) => {
  console.log(e.target.id);
  if (e.target.id == "NoPropStatClose") {
    var card = document.getElementById("NoPropCard");
    document.body.removeChild(card);
  }
});
