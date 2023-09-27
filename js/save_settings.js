import { $el } from "../../../scripts/ui.js";
import { app } from "../../../scripts/app.js";
const id = "cg.savesettings";

function saveToJsonFile(something) {
    const blobURL = URL.createObjectURL(new Blob([JSON.stringify(something,null,2)]));
    const a = document.createElement('a');
    a.href = blobURL;
    a.download = "settings.json";
    a.style.display = 'none';
    document.body.append(a);
    a.click();
    setTimeout(() => {
      URL.revokeObjectURL(blobURL);
      a.remove();
    }, 1000);
}

async function loadSettings(callback) {
    let input = document.createElement('input');
    input.type = 'file';
    input.onchange = () => {
              let files = Array.from(input.files);
              files[0].text().then(callback);
          };
    input.click();
}

async function saveSettings() {
    var settings = {};
    for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (key.startsWith('Comfy.Settings.')) {
            var id = key.substring(15);
            settings[id] = app.ui.settings.getSettingValue(id);
        }
    }
    saveToJsonFile(settings);
}

async function applySettings(setting_string) {
    const settings = JSON.parse(setting_string);
    for (const [id, value] of Object.entries(JSON.parse(setting_string))) {
        app.ui.settings.setSettingValue(id, value);
    }
    let _ = { ...app.ui.settings.settings.map((s) => {
        if (s.onchange) s.onchange(s);
        if (s.oninput) s.oninput(s);
    } )}
    app.ui.settings.element.close();
    app.ui.settings.show();
}

app.registerExtension({
    name: id,
    async setup() {
        app.ui.settings.addSetting({
            id,
            name: "Settings",
            type: (name, setter, value) => {
				return $el("tr", [
					$el("td", [
						$el("label", {
							textContent: "Settings",
						}),
					]),
					$el("td",  [ 
                        $el("div", {style: {"display": "grid", "gap": "4px", "grid-auto-flow": "column"}}, 
                            [
                                $el("button", {
                                    textContent: "Save Settings",
                                    onclick: () => { saveSettings() },
                                    style: {
                                        fontSize: "14px",
                                        display: "block",
                                        marginTop: "5px",
                                    },
                                }),
                                $el("button", {
                                    textContent: "Load Settings",
                                    onclick: () => { loadSettings(applySettings) },
                                    style: {
                                        fontSize: "14px",
                                        display: "block",
                                        marginTop: "5px",
                                    },
                                }),
                            ],  
                        ),
					]),
				]);
            }
        })
    }
})