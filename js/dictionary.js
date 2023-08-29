import { app } from "../../scripts/app.js";

app.registerExtension({
	name: "Comfy.cg.UploadImageWithDictionary",
	async beforeRegisterNodeDef(node, nodeData, app) {
		if (nodeData.name === "LoadImageWithDictionary") {
// add the image upload control
			nodeData.input.required.upload = ["IMAGEUPLOAD"];
// don't add the extra menu items, because we don't want to confuse things with the MaskEditor, and we don't need save image on a loader
			node.prototype.getExtraMenuOptions = function(_, options) {}
		}	
	},
});

