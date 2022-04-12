import GraphNode from "../graphNode";
import GraphEdge from "../graphEdge";

export default interface GraphDataBatch {
    nodes: GraphNode[],
    edges: GraphEdge[]
}