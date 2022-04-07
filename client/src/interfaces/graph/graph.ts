import GraphNode from "./graphNode";
import GraphEdge from "./graphEdge";

/**
 * Graph interface
 */
export default interface Graph {
    nodes: GraphNode[],
    edges: GraphEdge[]
}