import React from "react";
import Sigma from "sigma";

import '../../resources/css/graph/Sigma.css';

import EdgesDefaultProgram from "sigma/rendering/webgl/programs/edge";
import EdgesFastProgram from "sigma/rendering/webgl/programs/edge.fast";

import circlepack from "graphology-layout/circlepack";
import clusters from "graphology-generators/random/clusters";
import Graph from "graphology";
import seedrandom from "seedrandom";
import Logger from "../../utils/logging/logger";
import GraphController from "../../controllers/api/graph/GraphController";
import WsGraphController from "../../controllers/socket/graph/WsGraphController";

export class ApplicationGraph extends React.Component {

    private graphController: WsGraphController;
    private graph: Graph = {} as Graph;
    private logger: Logger;

    public state = {
        order: 5000,
        size: 100000,
        clusters: 5,
        edgesRenderer: "edges-fast",
    };

    private renderer: Sigma = {} as Sigma;

    /**
     * Async method , getting the nodes from the WebSocket and refreshing them
     * @private
     */
     private async getNodes() {
        try {
            // Get nodes from the web socket
            this.graphController.getGraph("OL2", (batch: any) => {
                console.log("Batch", batch)
            });

            // Add

            // Refresh
        } catch (e) {
            this.logger.error("Failed to get nodes", e );
        }
    }

    /**
     * Build the Graph and declare how it should behave
     * @private
     */
    private buildGraph() {
        const rng = seedrandom("sigma"); // Random seed for colors

        // Get nodes
        this.getNodes();

        this.graph = clusters(Graph, { ...this.state, rng });
        circlepack.assign(this.graph, {
            hierarchyAttributes: ["cluster"],
        });

        const colors: Record<string, string> = {};
        for (let i = 0; i < this.state.clusters; i++) {
            colors[i] = "#" + Math.floor(rng() * 16777215).toString(16);
        }

        let i = 0;
        this.graph.forEachNode((node, { cluster }) => {
            this.graph.mergeNodeAttributes(node, {
                size: 3,
                label: `Node n°${++i}, in cluster n°${cluster}`,
                color: colors[cluster + ""],
            });
        });

        this.logger.info("Graph built", this.graph)
    }

    /**
     * Launch the rendering of the graph
     */
    componentDidMount() {
        // Get the container
        const container = document.getElementById("sigma-container") as HTMLElement;

        // Build the graph
        this.buildGraph();

        // Re Render the windows
        this.renderer = new Sigma(this.graph, container, {
            defaultEdgeColor: "#000000",
            defaultEdgeType: this.state.edgesRenderer,
            edgeProgramClasses: {
                "edges-default": EdgesDefaultProgram,
                "edges-fast": EdgesFastProgram,
            },
        });



        this.renderer.refresh();
    }

    constructor(props: any) {
        super(props);
        this.logger = Logger.getLogger("Application Graph");
        this.graphController = new WsGraphController();
    }

   render() {
        return (
            <div className="Sigma-Container" id="sigma-container" />
        );
    };
}