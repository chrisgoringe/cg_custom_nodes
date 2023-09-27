import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "cg.tinynode",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData?.description?.includes('tinynode')) {
            const onDrawBackground = nodeType.prototype.onDrawBackground;
            nodeType.prototype.onDrawBackground = function() {
                if (this.title.length>6) this.title = this.title.substring(5,6);
                this.size = [50,26];
                //this.flags.collapsed = true;
                onDrawBackground?.apply(this,arguments);
                this.onDrawBackground = onDrawBackground;
            }
        }
    }
})
