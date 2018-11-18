<template>
    <div id="graph"></div>
</template>
<script>
    import headed from "@/components/headerSection.vue";
    import foot from "@/components/footerSection.vue";

    export default {
        name: "ExploreMovie",
        mounted: function () {
            console.log("ExploreMovie beforeCreate");
            this.getDetails();
        },
        updated: function () {
            console.log("ExploreMovie Updated");
        },
        components: {
            headed,
            foot,
        },
        methods: {
            getDetails: function () {
                this.$http.get(this.endpoint).then(
                    function (response) {
                        let d3 = require("d3");
                        let maxNodeSize = 50, root;
                        let graphDiv = document.getElementById("graph");
                        const width = graphDiv.clientWidth;
                        const height = graphDiv.clientHeight;

                        let force = d3.layout.force()
                            .linkDistance(200)
                            .charge(-4000)
                            .size([width, height])
                            .on("tick", tick);

                        let div = d3.select("#graph").append("div")
                            .attr("class", "tooltip")
                            .style("opacity", 0);

                        let svg = d3.select("#graph").append("svg")
                            .attr("width", width)
                            .attr("height", height);

                        let link = svg.selectAll(".link"),
                            node = svg.selectAll(".node");

                        let defs = svg.insert("svg:defs").data(["end"]);

                        defs.enter().append("svg:path")
                            .attr("d", "M0,-5L10,0L0,5");

                        let filterBlur = defs.append('svg:filter')
                            .attr({id: 'blur'});
                        filterBlur.append('feGaussianBlur')
                            .attr({
                                'in': "SourceGraphic",
                                'stdDeviation': 7
                            });

                        d3.json(process.env.VUE_APP_EXPLORE_ENDPOINT + this.$route.params.id, function (error, json) {
                            if (error) throw error;
                            root = json;
                            createDefs(root);
                            svg.append("rect")
                                .attr("width", "100%")
                                .attr("height", "100%")
                                .attr("class", "myRect")
                                .attr("filter", 'url(#blur)')
                                .style("fill", "url(#" + root.name + root.level + "backdrop)")
                            update(root);
                        });

                        let nodes = [];
                        let links = [];
                        let i = 0;

                        function update(_root) {
                            let _aux = flatten(_root);
                            nodes.push.apply(nodes, _aux[1]);
                            links.push.apply(links, d3.layout.tree().links([_aux[0]]));
                            {
                                let uid = new Set();
                                let nodesNew = [];
                                for (let _i in nodes) {
                                    if (!uid.has(nodes[_i].id)) {
                                        uid.add(nodes[_i].id);
                                        nodesNew.push(nodes[_i]);
                                    }
                                }
                                nodes = nodesNew;
                            }
                            {
                                let uid = new Set();
                                let linksNew = [];
                                for (let _i in links) {
                                    let tmp = links[_i];
                                    let _id = '' + tmp.source.id + '#' + tmp.target.id;
                                    if (!uid.has(_id)) {
                                        uid.add(_id);
                                        linksNew.push(links[_i]);
                                    }
                                }
                                links = linksNew;
                            }

                            force
                                .nodes(nodes)
                                .links(links)
                                .start();

                            link = link.data(links, function (d) {
                                return d.target.id;
                            });

                            link.exit().remove();

                            link.enter().insert("path", ".node")
                                .attr("class", "link");

                            node = node.data(nodes, function (d) {
                                return d.id;
                            });

                            node.exit().remove();

                            let nodeEnter = node.enter().append("g")
                                .attr("class", "node")
                                .on("click", click)
                                .call(force.drag)
                                .on('dragstart', function (d) {
                                    d3.select(this).classed('fixed', d.fixed = true);
                                    force.stop();
                                })
                                .on('dragend', function () {
                                    force.stop();
                                });

                            nodeEnter.append("circle")
                                .attr("r", function (d) {
                                    if (d.level === 0)
                                        return 62;
                                    return 25;
                                    return Math.sqrt(d.size) || 4.5;
                                })
                                .style("fill", "#000")
                                .style("fill", function (d) {
                                    return "url(#" + d.name + d.level + ")";
                                })
                                .style("stroke", "black")
                                .on("mouseover", function (d) {
                                    div.transition()
                                        .duration(200)
                                        .style("opacity", .9);
                                    div.html(d.name)
                                        .style("left", (d3.event.pageX) + "px")
                                        .style("top", (d3.event.pageY - 28) + "px");
                                })
                                .on("mouseout", function (d) {
                                    div.transition()
                                        .duration(500)
                                        .style("opacity", 0);
                                });
                        }

                        function tick() {
                            link.attr("d", function (d) {
                                let dx = d.target.x - d.source.x,
                                    dy = d.target.y - d.source.y,
                                    dr = Math.sqrt(dx * dx + dy * dy);
                                return "M" + d.source.x + ","
                                    + d.source.y
                                    + "A" + dr + ","
                                    + dr + " 0 0,1 "
                                    + d.target.x + ","
                                    + d.target.y;
                            });
                            node.attr("transform", nodeTransform);
                        }

                        // Toggle children on click.
                        function click(d) {
                            console.log("CLICK");
                            if (d3.event.defaultPrevented) return; // ignore drag
                            if (d.visibility === true) {
                                d.visibility = false;
                                if (d.children) {
                                    console.log(nodes);
                                    console.log(links);
                                    let uid = new Set();
                                    {
                                        d.children.forEach(function (node) {
                                            uid.add(node.id);
                                        });
                                        let nodesNew = [];
                                        for (let _i in nodes) {
                                            if (!uid.has(nodes[_i].id)) {
                                                nodesNew.push(nodes[_i]);
                                            }
                                        }
                                        nodes = nodesNew;
                                        console.log(nodes);
                                    }
                                    {
                                        let linksNew = [];
                                        for (let _i in links) {
                                            let tmp = links[_i];
                                            if (!uid.has(tmp.source.id) && !uid.has(tmp.target.id))
                                                linksNew.push(links[_i]);
                                        }
                                        links = linksNew;
                                        console.log(links);
                                    }
                                    d._children = d.children;
                                    d.children = null;
                                } else {
                                    d.children = d._children;
                                    d._children = null;
                                }
                            }
                            else {
                                d.visibility = true;
                            }
                            update(d);
                        }

                        // Returns a list of all nodes under the root.
                        function flatten(_root) {
                            let _nodes = [];
                            console.log("FLATTEN");
                            _root.visibility = true;
                            if (_root.children) {
                                _root.children.forEach(function (node) {
                                    if (!node.id) {
                                        node.id = ++i;
                                    }
                                    node.visibility = false;
                                    _nodes.push(node);
                                });
                            }
                            _root.id = ++i;
                            _nodes.push(root);
                            return [_root, _nodes];
                        }

                        function createDefs(root) {
                            let _w = 500 / 4;
                            let _h = 750 / 4;
                            defs.append("svg:pattern")
                                .attr("id", root.name + root.level)
                                .attr("width", 1)
                                .attr("height", 1)
                                .attr("preserveAspectRatio", "none")
                                .append("svg:image")
                                .attr("href", process.env.VUE_APP_POSTER_BASE + root.img)
                                .attr("preserveAspectRatio", "none")
                                .attr("width", _w)
                                .attr("height", _h)
                                .attr("x", 0)
                                .attr("y", 0);
                            defs.append("svg:pattern")
                                .attr("id", root.name + root.level + 'backdrop')
                                .attr("width", 1)
                                .attr("height", 1)
                                .append("svg:image")
                                .attr("href", process.env.VUE_APP_POSTER_BASE + root.backdrop)
                                .attr("viewBox", "0 0 " + width + " " + height)
                                .attr("preserveAspectRatio", "xMidYMin slice")
                                .attr("width", width)
                                .attr("height", height)
                                .attr("x", 0)
                                .attr("y", 0);

                            let _wx = 50;
                            let _hx = 50;

                            function recurse(node) {
                                if (node.children) node.children.forEach(recurse);
                                defs.append("svg:pattern")
                                    .attr("id", node.name + node.level)
                                    .attr("width", 1)
                                    .attr("height", 1)
                                    .attr("preserveAspectRatio", "none")
                                    .append("svg:image")
                                    .attr("href", node.img)
                                    .attr("preserveAspectRatio", "none")
                                    .attr("width", _wx)
                                    .attr("height", _hx)
                                    .attr("x", 0)
                                    .attr("y", 0);
                            }

                            recurse(root);
                        }

                        function nodeTransform(d) {
                            d.x = Math.max(maxNodeSize, Math.min(width - (d.imgwidth / 2 || 16), d.x));
                            d.y = Math.max(maxNodeSize, Math.min(height - (d.imgheight / 2 || 16), d.y));
                            return "translate(" + d.x + "," + d.y + ")";
                        }
                    })
            },
            function(response) {
            }
        },
        data: function () {
            return {
                endpoint: process.env.VUE_APP_EXPLORE_ENDPOINT + this.$route.params.id,
                imgsrc: process.env.VUE_APP_POSTER_BASE,
                result: "",
                error: "",
                alert: false,
                email: "",
                title: "",
                release_date: "",
            };
        }
    }
</script>
<style>

    @import url(http://fonts.googleapis.com/css?family=Source+Code+Pro:400,600);

    body {
        font-family: "Source Code Pro", Consolas, monaco, monospace;
        line-height: 160%;
        font-size: 16px;
        margin: 0;
    }

    path.link {
        fill: none;
        stroke: #eee;
        stroke-width: 2px;
    }

    a:link {
        color: #EE3124;
        text-decoration: none;
    }

    a:visited {
        color: #EE3124;
    }

    a:hover {
        color: #A4CD39;
        text-decoration: underline;
    }

    a:active {
        color: #EE3124;
    }

    #graph {
        position: fixed;
        left: 0px;
        right: 0px;
        top: 0px;
        bottom: 0px;
    }

    div.tooltip {
        position: absolute;
        text-align: center;
        width: 120px;
        height: 28px;
        padding: 2px;
        background: lightsteelblue;
        border: 0px;
        border-radius: 8px;
        pointer-events: none;
    }
</style>
