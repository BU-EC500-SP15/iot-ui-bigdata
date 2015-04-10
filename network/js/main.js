var sigInst, canvas, $GP

//Load configuration file
var config={};

//For debug allow a config=file.json parameter to specify the config
function GetQueryStringParams(sParam,defaultVal) {
    var sPageURL = ""+window.location;//.search.substring(1);//This might be causing error in Safari?
    if (sPageURL.indexOf("?")==-1) return defaultVal;
    sPageURL=sPageURL.substr(sPageURL.indexOf("?")+1);    
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
    return defaultVal;
}


jQuery.getJSON(GetQueryStringParams("config","config.json"), function(data, textStatus, jqXHR) {
	config=data;
	
	if (config.type!="network") {
		//bad config
		alert("Invalid configuration settings.")
		return;
	}
	
	//As soon as page is ready (and data ready) set up it
	$(document).ready(setupGUI(config));
});//End JSON Config load


// FUNCTION DECLARATIONS

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function initSigma(config) {//This function just say that if we do not have a config file for sigma, we can use the default one below.
	var data=config.data
	
	var drawProps, graphProps,mouseProps;
	if (config.sigma && config.sigma.drawingProperties) 
		drawProps=config.sigma.drawingProperties;
	else
		drawProps={
        defaultLabelColor: "#000",
        defaultLabelSize: 14,
        defaultLabelBGColor: "#ddd",
        defaultHoverLabelBGColor: "#002147",
        defaultLabelHoverColor: "#fff",
        labelThreshold: 10,
        defaultEdgeType: "curve",
        hoverFontStyle: "bold",
        fontStyle: "bold",
        activeFontStyle: "bold"
    };
    
    if (config.sigma && config.sigma.graphProperties)	
    	graphProps=config.sigma.graphProperties;
    else
    	graphProps={
        minNodeSize: 1,
        maxNodeSize: 7,
        minEdgeSize: 0.2,
        maxEdgeSize: 0.5
    	};
	
	if (config.sigma && config.sigma.mouseProperties) 
		mouseProps=config.sigma.mouseProperties;
	else
		mouseProps={
        minRatio: 0.75, // How far can we zoom out?
        maxRatio: 20, // How far can we zoom in?
    	};
	
    //draw everything on the canvas that is specified
    var a = sigma.init(document.getElementById("sigma-canvas")).drawingProperties(drawProps).graphProperties(graphProps).mouseProperties(mouseProps);
    sigInst = a;
    a.active = !1;
    a.neighbors = {};
    a.detail = !1;


    dataReady = function() {//This is called as soon as data is loaded
		a.clusters = {};

		a.iterNodes(
			function (b) { //This is where we populate the array used for the group select box

				// note: index may not be consistent for all nodes. Should calculate each time. 
				 // alert(JSON.stringify(b.attr.attributes[5].val));
				// alert(b.x);
				a.clusters[b.color] || (a.clusters[b.color] = []);
				a.clusters[b.color].push(b.id);//SAH: push id not label
			}
		
		);
	
		a.bind("upnodes", function (a) {
		    nodeActive(a.content[0])
		});

		a.draw();
		configSigmaElements(config);
	}

    if (data.indexOf("gexf")>0 || data.indexOf("xml")>0)
        a.parseGexf(data,dataReady);
    else
	    a.parseJson(data,dataReady);
    gexf = sigmaInst = null;
}


function setupGUI(config) {
	// Initialise main interface elements
	var logo=""; // Logo elements
	if (config.logo.file) {

		logo = "<img src=\"" + config.logo.file +"\"";
		if (config.logo.text) logo+=" alt=\"" + config.logo.text + "\"";
		logo+=">";
	} else if (config.logo.text) {
		logo="<h1>"+config.logo.text+"</h1>";
	}
	if (config.logo.link) logo="<a href=\"" + config.logo.link + "\">"+logo+"</a>";
	$("#maintitle").html(logo);

	// #title
	$("#title").html("<h2>"+config.text.title+"</h2>");

	// #titletext
	$("#titletext").html(config.text.intro);

	// More information
	if (config.text.more) {
		$("#information").html(config.text.more);
	} else {
		//hide more information link
		$("#moreinformation").hide();
	}

	// Legend

	// Node
	if (config.legend.nodeLabel) {
		$(".node").next().html(config.legend.nodeLabel);
	} else {
		//hide more information link
		$(".node").hide();
	}
	// Edge
	if (config.legend.edgeLabel) {
		$(".edge").next().html(config.legend.edgeLabel);
	} else {
		//hide more information link
		$(".edge").hide();
	}
	// Colours
	if (config.legend.nodeLabel) {
		$(".colours").next().html(config.legend.colorLabel);
	} else {
		//hide more information link
		$(".colours").hide();
	}

	$GP = {
		calculating: !1,
		showgroup: !1
	};
    $GP.intro = $("#intro");
    $GP.minifier = $GP.intro.find("#minifier");
    $GP.mini = $("#minify");
    $GP.info = $("#attributepane");
    $GP.info_edit = $GP.info.find(".editattributes");
    $GP.info_donnees = $GP.info.find(".nodeattributes");
    $GP.info_name = $GP.info.find(".name");
    $GP.info_link = $GP.info.find(".link");
    $GP.info_data = $GP.info.find(".data");
    $GP.info_close = $GP.info.find(".returntext");
    $GP.info_close2 = $GP.info.find(".close");
    $GP.info_p = $GP.info.find(".p");
    $GP.info_close.click(nodeNormal);
    $GP.info_close2.click(nodeNormal);
    $GP.form = $("#mainpanel").find("form");
    $GP.search = new Search($GP.form.find("#search"));
    if (!config.features.search) {
		$("#search").hide();
	}
	if (!config.features.groupSelectorAttribute) {
		$("#attributeselect").hide();
	}
    $GP.cluster = new Cluster($GP.form.find("#attributeselect"));
    config.GP=$GP;
    initSigma(config);
}

function configSigmaElements(config) {
	$GP=config.GP;
    
    // Node hover behaviour
    if (config.features.hoverBehavior == "dim") {
        var outTimeoutID;
        var overTimeoutID;
        var greyColor = '#ccc';
        sigInst.bind('overnodes', function(event) {
        var dimIn = function(event) {
            var nodes = event.content;
            var neighbors = {};
            sigInst.iterEdges(function(e){
            if(nodes.indexOf(e.source)<0 && nodes.indexOf(e.target)<0){
                if(!e.attr['grey']){
                    e.attr['true_color'] = e.color;
                    e.color = greyColor;
                    e.attr['grey'] = 1;
                }
            }else{
                e.color = e.attr['grey'] ? e.attr['true_color'] : e.color;
                e.attr['grey'] = 0;

                neighbors[e.source] = 1;
                neighbors[e.target] = 1;
            }
            }).iterNodes(function(n){
                if (!neighbors[n.id]) {
                    if (!n.attr['grey']) {
                        n.attr['true_color'] = n.color;
                        n.color = greyColor;
                        n.attr['grey'] = 1;
                     }
                }else{
                    n.color = n.attr['grey'] ? n.attr['true_color'] : n.color;
                    n.attr['grey'] = 0;
                }
            }).draw(2,2,2);
        };
        window.clearTimeout(overTimeoutID);
        window.clearTimeout(outTimeoutID);
        overTimeoutID = window.setTimeout(function(){dimIn(event);}, 500);
		}).bind('outnodes',function(){
        var dimOut = function () {
            sigInst.iterEdges(function(e){
                e.color = e.attr['grey'] ? e.attr['true_color'] : e.color;
                e.attr['grey'] = 0;
            }).iterNodes(function(n){
                n.color = n.attr['grey'] ? n.attr['true_color'] : n.color;
                n.attr['grey'] = 0;
            }).draw(2,2,2);
        };
        window.clearTimeout(outTimeoutID);
        outTimeoutID = window.setTimeout(function(){dimOut();}, 500);
        });

    } else if (config.features.hoverBehavior == "hide") {

		sigInst.bind('overnodes',function(event){
			var nodes = event.content;
			var neighbors = {};
		sigInst.iterEdges(function(e){
			if(nodes.indexOf(e.source)>=0 || nodes.indexOf(e.target)>=0){
		    	neighbors[e.source] = 1;
		    	neighbors[e.target] = 1;
		  	}
		}).iterNodes(function(n){
		  	if(!neighbors[n.id]){
		    	n.hidden = 1;
		  	}else{
		    	n.hidden = 0;
		  }
		}).draw(2,2,2);
		}).bind('outnodes',function(){
		sigInst.iterEdges(function(e){
		  	e.hidden = 0;
		}).iterNodes(function(n){
		  	n.hidden = 0;
		}).draw(2,2,2);
		});

    }
    $GP.bg = $(sigInst._core.domElements.bg);
    $GP.bg2 = $(sigInst._core.domElements.bg2);
    var a = [],
        b,x=1;
		for (b in sigInst.clusters) a.push('<div style="line-height:12px"><a href="#' + b + '"><div style="width:40px;height:12px;border:1px solid #fff;background:' + b + ';display:inline-block"></div> Group ' + (x++) + ' (' + sigInst.clusters[b].length + ' members)</a></div>');
    //a.sort();
    $GP.cluster.content(a.join(""));
    b = {
        minWidth: 400,
        maxWidth: 800,
        maxHeight: 600
    };//        minHeight: 300,
    $("a.fb").fancybox(b);
    $("#zoom").find("div.z").each(function () {
        var a = $(this),
            b = a.attr("rel");
        a.click(function () {
			if (b == "center") {
				sigInst.position(0,0,1).draw();
			} else {
		        var a = sigInst._core;
	            sigInst.zoomTo(a.domElements.nodes.width / 2, a.domElements.nodes.height / 2, a.mousecaptor.ratio * ("in" == b ? 1.5 : 0.5));		
			}

        })
    });
    $GP.mini.click(function () {
        $GP.mini.hide();
        $GP.intro.show();
        $GP.minifier.show()
    });
    $GP.minifier.click(function () {
        $GP.intro.hide();
        $GP.minifier.hide();
        $GP.mini.show()
    });
    $GP.intro.find("#showGroups").click(function () {
        !0 == $GP.showgroup ? showGroups(!1) : showGroups(!0)
    });
    a = window.location.hash.substr(1);
    if (0 < a.length) switch (a) {
    case "Groups":
        showGroups(!0);
        break;
    case "information":
        $.fancybox.open($("#information"), b);
        break;
    default:
        $GP.search.exactMatch = !0, $GP.search.search(a)
		$GP.search.clean();
    }

}

function Search(a) {
    this.input = a.find("input[name=search]");
    this.state = a.find(".state");
    this.results = a.find(".results");
    this.exactMatch = !1;
    this.lastSearch = "";
    this.searching = !1;
    var b = this;
    this.input.focus(function () {
        var a = $(this);
        a.data("focus") || (a.data("focus", !0), a.removeClass("empty"));
        b.clean()
    });
    this.input.keydown(function (a) {
        if (13 == a.which) return b.state.addClass("searching"), b.search(b.input.val()), !1
    });
    this.state.click(function () {
        var a = b.input.val();
        b.searching && a == b.lastSearch ? b.close() : (b.state.addClass("searching"), b.search(a))
    });
    this.dom = a;
    this.close = function () {
        this.state.removeClass("searching");
        this.results.hide();
        this.searching = !1;
        this.input.val("");//SAH -- let's erase string when we close
        nodeNormal()
    };
    this.clean = function () {
        this.results.empty().hide();
        this.state.removeClass("searching");
        this.input.val("");
    };
    this.search = function (a) {
        var b = !1,
            c = [],
            b = this.exactMatch ? ("^" + a + "$").toLowerCase() : a.toLowerCase(),
            g = RegExp(b);
        this.exactMatch = !1;
        this.searching = !0;
        this.lastSearch = a;
        this.results.empty();
        if (2 >= a.length) this.results.html("<i>You must search for a name with a minimum of 3 letters.</i>");
        else {
	        sigInst.iterNodes(function (a) {
	            if (g.test(a.label.toLowerCase())) {
	            	c.push({
	                	id: a.id,
	                	name: a.label
	            	});
	            } else if (config["search"] && config["search"]["fulltext"]) { //Check attributes for this node if fulltext is on
	            	for (attr in a["attr"]["attributes"]) {
	            		if (g.test((""+a["attr"]["attributes"][attr]).toLowerCase())) {
					    	c.push({
					        	id: a.id,
					        	name: a.label
					    	});
					    	break;//Matched not need to check further
					 	}
					}
	            }
	        });
            c.length ? (b = !0, nodeActive(c[0].id)) : b = showCluster(a);
            a = ["<b>Search Results: </b>"];
            if (1 < c.length) for (var d = 0, h = c.length; d < h; d++) a.push('<a href="#' + c[d].name + '" onclick="nodeActive(\'' + c[d].id + "')\">" + c[d].name + "</a>");
            0 == c.length && !b && a.push("<i>No results found.</i>");
            1 < a.length && this.results.html(a.join(""));
           }
        if(c.length!=1) this.results.show();
        if(c.length==1) this.results.hide();   
    }
}

function Cluster(a) {
    this.cluster = a;
    this.display = !1;
    this.list = this.cluster.find(".list");
    this.list.empty();
    this.select = this.cluster.find(".select");
    this.select.click(function () {
        $GP.cluster.toggle()
    });
    this.toggle = function () {
        this.display ? this.hide() : this.show()
    };
    this.content = function (a) {
        this.list.html(a);
        this.list.find("a").click(function () {
            var a = $(this).attr("href").substr(1);
            showCluster(a)
        })
    };
    this.hide = function () {
        this.display = !1;
        this.list.hide();
        this.select.removeClass("close")
    };
    this.show = function () {
        this.display = !0;
        this.list.show();
        this.select.addClass("close")
    }
}
function showGroups(a) {
    a ? ($GP.intro.find("#showGroups").text("Hide groups"), $GP.bg.show(), $GP.bg2.hide(), $GP.showgroup = !0) : ($GP.intro.find("#showGroups").text("View Groups"), $GP.bg.hide(), $GP.bg2.show(), $GP.showgroup = !1)
}

function nodeNormal() {
    !0 != $GP.calculating && !1 != sigInst.detail && (showGroups(!1), $GP.calculating = !0, sigInst.detail = !0, $GP.info.delay(400).animate({width:'hide'},350),$GP.cluster.hide(), sigInst.iterEdges(function (a) {
        a.attr.color = !1;
        a.hidden = !1
    }), sigInst.iterNodes(function (a) {
        a.hidden = !1;
        a.attr.color = !1;
        a.attr.lineWidth = !1;
        a.attr.size = !1
    }), sigInst.draw(2, 2, 2, 2), sigInst.neighbors = {}, sigInst.active = !1, $GP.calculating = !1, window.location.hash = "")
}

function nodeActive(a) {

	var groupByDirection=false;
	if (config.informationPanel.groupByEdgeDirection && config.informationPanel.groupByEdgeDirection==true)	groupByDirection=true;
	
    sigInst.neighbors = {};
    sigInst.detail = !0;
    var b = sigInst._core.graph.nodesIndex[a];
    showGroups(!1);
	var outgoing={},incoming={},mutual={};//SAH
    sigInst.iterEdges(function (b) {
        b.attr.lineWidth = !1;
        b.hidden = !0;
        
        n={
            name: b.label,
            colour: b.color
        };
        
   	   if (a==b.source) outgoing[b.target]=n;		//SAH
	   else if (a==b.target) {
       incoming[b.source]=n;		//SAH
       parent = sigInst._core.graph.nodesIndex[b.source];
   }
       if (a == b.source || a == b.target) sigInst.neighbors[a == b.target ? b.source : b.target] = n;
       b.hidden = !1, b.attr.color = "rgba(0, 0, 0, 1)";
    });
    var f = [];
    sigInst.iterNodes(function (a) {
        a.hidden = !0;
        a.attr.lineWidth = !1;
        a.attr.color = a.color
    });
    
    if (groupByDirection) {
		//SAH - Compute intersection for mutual and remove these from incoming/outgoing
		for (e in outgoing) {
			//name=outgoing[e];
			if (e in incoming) {
				mutual[e]=outgoing[e];
				delete incoming[e];
				delete outgoing[e];
			}
		}
    }
    
    var createList=function(c) {
        var f = [];
    	var e = [],
      	 	 //c = sigInst.neighbors,
       		 g;
    for (g in c) {
        var d = sigInst._core.graph.nodesIndex[g];
        d.hidden = !1;
        d.attr.lineWidth = !1;
        d.attr.color = c[g].colour;
        a != g && e.push({
            id: g,
            name: d.label,
            group: (c[g].name)? ""+c[g].name:"",
            colour: c[g].colour
        })
    }
    e.sort(function (a, b) {
        var c = a.group.toLowerCase(),
            d = b.group.toLowerCase(),
            e = a.name.toLowerCase(),
            f = b.name.toLowerCase();
        return c != d ? c < d ? -1 : c > d ? 1 : 0 : e < f ? -1 : e > f ? 1 : 0
    });
    d = "";
		for (g in e) {
			c = e[g];
			/*if (c.group != d) {
				d = c.group;
				f.push('<li class="cf" rel="' + c.color + '"><div class=""></div><div class="">' + d + "</div></li>");
			}*/
			f.push('<li class="membership"><a href="#' + c.name + '" onmouseover="sigInst._core.plotter.drawHoverNode(sigInst._core.graph.nodesIndex[\'' + c.id + '\'])\" onclick=\"nodeActive(\'' + c.id + '\')" onmouseout="sigInst.refresh()">' + c.name + "</a></li>");
		}
		return f;
	}

	/*console.log("mutual:");
	console.log(mutual);
	console.log("incoming:");
	console.log(incoming);
	console.log("outgoing:");
	console.log(outgoing);*/
	
	
	var f=[];
	
	//console.log("neighbors:");
	//console.log(sigInst.neighbors);

	if (groupByDirection) {
		/*size=Object.size(mutual);
		f.push("<h2>Mututal (" + size + ")</h2>");
		(size>0)? f=f.concat(createList(mutual)) : f.push("No mutual links<br>");*/
		size=Object.size(incoming);
		f.push("<h2>Parent (" + size + ")</h2>");
		(size>0)? f=f.concat(createList(incoming)) : f.push("No Parent link<br>");
		size=Object.size(outgoing);
		f.push("<h2>Children_List (" + size + ")</h2>");
		(size>0)? f=f.concat(createList(outgoing)) : f.push("No Children links<br>");
	} else {
		f=f.concat(createList(sigInst.neighbors));
	}
	//b is object of active node -- SAH
    b.hidden = !1;
    b.attr.color = b.color;
    b.attr.lineWidth = 6;
    b.attr.strokeStyle = "#000000";
    sigInst.draw(2, 2, 2, 2);

    $GP.info_link.find("ul").html(f.join(""));
    $GP.info_link.find("li").each(function () {
        var a = $(this),
            b = a.attr("rel");
    });
    f = b.attr;
    if (f.attributes) {
  		var image_attribute = false;
  		if (config.informationPanel.imageAttribute) {
  			image_attribute=config.informationPanel.imageAttribute;
  		}
        e = [];
        temp_array = [];
        g = 0;
        for (var attr in f.attributes) {
            var d = f.attributes[attr],
                h = "";
			if (attr!=image_attribute) {
                h = '<span><strong>' + attr + ':</strong> ' + d + '</span><br/>'
			}
            //temp_array.push(f.attributes[g].attr);
            e.push(h)
        }

        if (image_attribute) {
            //image_index = jQuery.inArray(image_attribute, temp_array);
            $GP.info_name.html("<div><img src=" + f.attributes[image_attribute] + " style=\"vertical-align:middle\" /> <span onmouseover=\"sigInst._core.plotter.drawHoverNode(sigInst._core.graph.nodesIndex['" + b.id + '\'])" onmouseout="sigInst.refresh()">' + b.label + "</span></div>");
        } else {
            $GP.info_name.html("<div><span onmouseover=\"sigInst._core.plotter.drawHoverNode(sigInst._core.graph.nodesIndex['" + b.id + '\'])" onmouseout="sigInst.refresh()">' + b.label + "</span></div>");
        }
        // Image field for attribute pane
        $GP.info_data.html(e.join("<br/>"))
    }
    $GP.info_data.show();
    $GP.info_p.html("Connections:");
    $GP.info.animate({width:'show'},350);
	$GP.info_donnees.hide();
	$GP.info_donnees.show();
    sigInst.active = a;
    window.location.hash = b.label;
    //console.log(b.label);
    //console.log(f.attributes);
    initForm(b);
    editForm(b);
    getPath(b);
    updateButton(b);
    createButton(b);
    deleteButton(b);
    addButton(b);

    createTrigger(b);

 

    /*  


//$("select").change(function(){
    //var selIndex = $("#selecttype").selectedIndex;
    //console.log(selIndex)
    //var selValue = $("#selecttype").options(selIndex).val();
    //console.log(selValue);
//})
     
    
    */


}

function showCluster(a) {
    var b = sigInst.clusters[a];
    if (b && 0 < b.length) {
        showGroups(!1);
        sigInst.detail = !0;
        b.sort();
        sigInst.iterEdges(function (a) {
            a.hidden = !1;
            a.attr.lineWidth = !1;
            a.attr.color = !1
        });
        sigInst.iterNodes(function (a) {
            a.hidden = !0
        });
        for (var f = [], e = [], c = 0, g = b.length; c < g; c++) {
            var d = sigInst._core.graph.nodesIndex[b[c]];
            !0 == d.hidden && (e.push(b[c]), 
                d.hidden = !1, d.attr.lineWidth = !1, 
                d.attr.color = d.color, 
                f.push('<li class="membership"><a href="#'+d.label+'" onmouseover="sigInst._core.plotter.drawHoverNode(sigInst._core.graph.nodesIndex[\'' + d.id + "'])\" onclick=\"nodeActive('" + d.id + '\')" onmouseout="sigInst.refresh()">' + d.label + "</a></li>"))
        }
        sigInst.clusters[a] = e;
        sigInst.draw(2, 2, 2, 2);
        $GP.info_name.html("<b>" + a + "</b>");
        $GP.info_data.hide();
        $GP.info_p.html("Group Members:");
        $GP.info_link.find("ul").html(f.join(""));
        $GP.info.animate({width:'show'},350);
        $GP.search.clean();
		$GP.cluster.hide();
        return !0
    }
    return !1
}


function initForm(b){
        $(".createlabel").empty();
        $(".editattributes").empty();
        $(".updatedata").empty();
        $(".createdata").empty();
        $(".updatetrigger").hide();
        $(".createtrigger").hide();
        $(".addattr").hide();
        $(".editattributes").hide();
        $(".updatebutton").show();
        //$(".createbutton").show();
        $(".deletebutton").show();
        if(b.attr.attributes.resourceType=="contentInstance"){
            $(".createbutton").hide();
        }else{
            $(".createbutton").show();
        }

}
function editForm(b){
   $("#editform").ready(function(){
        
        if (b.attr.attributes) {
            var image_attribute = false;
            if (config.informationPanel.imageAttribute) {
                image_attribute=config.informationPanel.imageAttribute;
            }
            e = [];
            temp_array = [];
            g = 0;
            l= '<strong>' + b.label+ ':</strong><br/><br/>'
            //console.log(l)
            $(".editattributes").append(l);
            for (var attr in b.attr.attributes) {
                var d = b.attr.attributes[attr],
                    h = "";
                if (attr!=image_attribute) {
                    h = '<strong>' + attr + ':</strong> ' 
                    t = '<input type="text" id=\"' + attr +'\"  name=\"' + attr + '\" readOnly = true value=\"'+ d +'\" /><br/>'
                }
                //console.log(t)              
                $(".editattributes").append(h);
                $(".editattributes").append(t);
            }
        $(".editattributes").show();
    }
})
}

function updateButton(b){
    $(".updatebutton").click(function(){
        $(".editattributes").empty();
        $(".updatedata").empty();
        $(".createdata").empty();
        $(".updatebutton").hide();
        $(".createbutton").hide();
        $(".deletebutton").hide();
        $(".addattr").hide();
        $(".updatetrigger").show();
        $(".createtrigger").hide();
        if (b.attr.attributes) {
        var image_attribute = false;
        if (config.informationPanel.imageAttribute) {
            image_attribute=config.informationPanel.imageAttribute;
        }
        e = [];
        temp_array = [];
        g = 0;
        l= '<strong>' + b.label+ ':</strong><br/><br/>'
        //console.log(l)
        $(".updatedata").append(l);
        for (var attr in b.attr.attributes) {
            var d = b.attr.attributes[attr],
                h = "";
            if (attr=="labels") {
                h = '<strong>' + attr + ':</strong> ' 
                t = '<input type="text" id=\"' + attr +'\"  name=\"' + attr + '\" value=\"'+ d +'\" /><br/>'
            }else{
                h = '<strong>' + attr + ':</strong> ' 
                t = '<span>' + d + '</span><br/>'
                
            }
            $(".updatedata").append(h);
            $(".updatedata").append(t);
       }
    }
})
}

function createButton(b){
        $(".createbutton").click(function(){
        $(".createlabel").empty();
        $(".editattributes").empty();
        $(".updatedata").empty();
        $(".createdata").empty();
        $(".updatebutton").hide();
        $(".createbutton").hide();
        $(".deletebutton").hide();
        $(".updatetrigger").hide();
        $(".createtrigger").show();
        $(".addattr").show();
        $(".createdata").show();
        type = '<strong>Choose resourceType: </strong><select id=selecttype><option value="AE">AE</option><option value="container">container</option><option value="contentInstance">contentInstance</option><option value="subscription">subscription</option></select><br/>'
        attr=["resourceName","labels","ontologyRef","appName","expirationTime","maxNrOfInstances","maxByteSize","maxInstanceAge","notificationURI","notificationContentType"]
        $(".createdata").append(type);
        for(var item in attr){
            var h =""
            if(attr[item]=="appName"){
                h ='<strong>' + attr[item] + '(Only_for_AEs): </strong> '
                t = '<input type="text" id=\"' + attr[item] +'\"  name=\"' + attr[item] + '\" value="" /><br/>'
            }else if(attr[item]=="maxNrOfInstances"||attr[item]=="maxByteSize"||attr[item]=="maxInstanceAge"){
                h ='<strong>' + attr[item] + '(Only_for_containers): </strong>'
                t = '<input type="text" id=\"' + attr[item] +'\"  name=\"' + attr[item] + '\" value="" /><br/>'
            }else if(attr[item]=="notificationURI"|| attr[item]=="notificationContentType"){
                h ='<strong>' + attr[item] + 'Required_for_subcriptions): </strong>'
                t = '<input type="text" id=\"' + attr[item] +'\"  name=\"' + attr[item] + '\" value="" /><br/>'
            }else{
                h ='<strong>' + attr[item] + ': </strong>'
                t = '<input type="text" id=\"' + attr[item] +'\"  name=\"' + attr[item] + '\" value="" /><br/>'
            }
            $(".createdata").append(h);
            $(".createdata").append(t);
            
        }
    });
}

function deleteButton(b){
    $(".deletebutton").click(function(){
        resource_url="http://54.68.184.172:8282/";
        resource_url = resource_url + path

        console.log(resource_url)
        $.ajax({
            url:resource_url+'?from=http:localhost:10000&requestIdentifier=12345',
            type:'DELETE',
            success:function(data){
                alert("Delete is sucessfully performed");
            }
            
        });
    });
}

function getPath(b){
    if(b.attr.attributes.resourceType=="contentInstance"){
        path =parent.label + "/" + b.label;
        
        //console.log(b)
        path = parent.attr.attributes.parentID + "/" +path;
        //console.log(path)
   
    }else{
        path = b.attr.attributes.parentID + "/" + b.label;
        //console.log(path)
     }
}

function addButton(b){
    $(".addattr").click(function(){
        t = '<input type="text" value="attributeName" /><input type="text" value="attributeValue" /><br/>'
        $(".createdata").append(t);
    });
}


function createTrigger(b){
    $(".createtrigger").click(function(){
        type = $("#selecttype option:selected").val();
        name = $("#resourceName").val();
        labels = $("#labels").val();
        ontologyRef = $("#ontologyRef").val();
        expirationTime=$("#expirationTime").val();
        appName = $("#appName").val();
        maxNrOfInstances = $("#maxNrOfInstances").val();
        maxByteSize = $("#maxByteSize").val();
        maxInstanceAge = $("#maxInstanceAge").val();
        notificationURI = $("#notificationURI").val();
        notificationContentType = $("#notificationContentType").val();


        parentType = b.attr.attributes.resourceType;
//console.log(parentType!="contentInstance")
        if(parentType!="contentInstance"){
            if(type == "AE"){
                label='<strong>You cannot create an AE except in the root node</strong><br/>'
                $(".createlabel").append(label);
                return;
            }else{
                if(name!=""){
                    data = '{\"from\": \"http:localhost: 10000\",\"requestIdentifier\": \"12345\",\"resourceType\": \"' + type +'\",\"content\":{ \"resourceName\":'
                    if(type=="container"){
                        data = data + '\"' + name +'\"';
                        var attrarray={"labels":labels,"ontologyRef":ontologyRef,"expirationTime":expirationTime,"maxNrOfInstances":maxNrOfInstances,"maxByteSize":maxByteSize,"maxInstanceAge":maxInstanceAge};
                        for(item in attrarray){
                            if(attrarray[item]!=""){
                                data = data + ',\"' + item + '\":\"'+ attrarray[item] +'\"';
                            }
                        }
                        data = data + '}}';
                    }else if(type=="contentInstance"){
                        data = data + '\"' + name +'\"';
                        var attrarray={"labels":labels,"ontologyRef":ontologyRef,"expirationTime":expirationTime};     
                        for(item in attrarray){
                            if(attrarray[item]!=""){
                                //console.log(item)
                                //console.log(attrarray[item]=="")
                                 data = data + ',\"' + item + '\":\"'+ attrarray[item] +'\"';
                            }
                        } 
                        data = data + '}}';                
                    }else if(type=="subscription"){
                       data = data + '\"' + name +'\"';
                       var attrarray={"labels":labels,"ontologyRef":ontologyRef,"expirationTime":expirationTime,"notificationURI":notificationURI,"notificationContentType":notificationContentType}; 
                       for(item in attrarray){
                        if(attrarray[item]!=""){
                            data = data + ',\"' + item + '\":\"'+ attrarray[item] +'\"';
                        }
                       } 
                       data = data + '}}'; 
                }else{
                    label='<strong>You must enter a resourceName';
                    $(".createlabel").append(label);
                    return;
                }
            }
        }
    }else{
            label='<strong>You cannot create a node under a contentInstance</strong><br/>';
            $(".createlabel").append(label);
            return;
        }

//console.log(data)



       resource_url = "http://54.68.184.172:8282/" + path;
       //console.log(path)

        headers = "?from=http:localhost:10000&requestIdentifier=12345"
        url= resource_url + headers

        //data = "{\"from\": \"http:localhost: 10000\",\"requestIdentifier\": \"12345\",\"resourceType\": \"container\",\"content\":{\"labels\": \"cookies\" ,\"resourceName\": \"cn11\"}}"
        $.ajax({
            url: url,
            type:'POST',
            dataType:'json',
            //contentType:'application/json',
            data: data,
            success:function(data){
                alert("Create is successfully performed");
            }
        })
});
}

