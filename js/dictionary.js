import { app } from "../../scripts/app.js";

// Adds an upload button to the nodes

app.registerExtension({
	name: "Comfy.UploadImage",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "LoadImageWithDictionary") {
			nodeData.input.required.upload = ["IMAGEUPLOAD"];
		}
	},
});
