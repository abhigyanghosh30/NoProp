document.addEventListener("change", (e) => {
  e.preventDefault();
  console.log(e.target.checked);
  browser.storage.local.set({ NoProp: e.target.checked });
  browser.tabs.reload();
});
document.addEventListener("DOMContentLoaded", () => {
  browser.storage.local.get({ NoProp: false }, (items) => {
    document.getElementById("flexSwitchCheckChecked").checked = items.NoProp;
  });
});
