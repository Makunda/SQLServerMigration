import React from "react";
import Graph from "graphology";
import { SigmaContainer, useLoadGraph } from "@react-sigma/core";
import "@react-sigma/core/lib/react-sigma.min.css";


export class ApplicationGraph extends React.Component {

    private LoadGraph() {
        // Get Graph from controller

        //
        const graph = new Graph();
        graph.addNode("first", { size: 15, label: "My first node", color: "#FA4F40" });
        useLoadGraph(graph);
    };

   private DisplayGraph() {
        return (
            <SigmaContainer style={{ height: "500px", width: "500px" }}>
                <LoadGraph />
            </SigmaContainer>
        );
    };
}