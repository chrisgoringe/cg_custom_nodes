import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "cg.tinynode",
    init() {
        LGraphCanvas.prototype.tiny = function(node) {
            const unTiny = node.unTiny;
            if (unTiny) {
                node.title = node.unTinyTitle;
                node.size = unTiny;
                node.flags.collapsed = false;
                node.unTiny = undefined;
            } else {
                node.unTinyTitle = node.title;
                node.title = node.title.substring(0,1);
                node.unTiny = node.size;
                node.size = [50,26];
                node.flags.collapsed = true;
            }
            node.onResize?.(node.size);
        };
        const getNodeMenuOptions = LGraphCanvas.prototype.getNodeMenuOptions;   
        LGraphCanvas.prototype.getNodeMenuOptions = function (node) {           
            const options = getNodeMenuOptions.apply(this, arguments);      
            node.setDirtyCanvas(true, true);                                
            options.splice(options.length - 1, 0,                          
                {
                    content: "Tiny",                                     
                    callback: () => { LGraphCanvas.prototype.tiny(node) ; }  
                },
                null,
            );
            return options;                                                 
        };  
    }
})
