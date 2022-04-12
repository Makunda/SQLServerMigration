import io from 'socket.io-client';
import SocketCom from "../../../utils/socket/SocketCom";
import SocketImpl from "../../../utils/socket/SocketImpl";
import Logger from "../../../utils/logging/logger";
import SocketDataBuilder from "../../../utils/socket/data/SocketDataBuilder";
import GetGraphByName from "../../../interfaces/graph/request/GetGraphByName";
import GraphDataBatch from "../../../interfaces/graph/request/GraphDataBatch";
import GraphCharacteristics from "../../../interfaces/graph/request/GraphCharacteristics";
import SocketData from "../../../interfaces/socket/SocketData";
import GraphListeningMode from "../../../interfaces/graph/request/GraphListeningMode";

export default class WsGraphController {

    private socket: SocketImpl;
    private logger: Logger = Logger.getLogger("Graph Socket Controller");

    /**
     * Wait for the graph data
     * @param characteristics Characteristics of the graph
     * @param callback Callback function
     */
    public enterListeningMode(characteristics: GraphCharacteristics, callback: Function) {
        // Received batch
        let batchNumber = 0, errors = 0;

        // Define Callback upfront
        this.socket.on("batch_received", (response: SocketData<GraphDataBatch>) => {
            batchNumber ++;
            this.logger.info(`Batch ${batchNumber} on ${characteristics.batch_size} received. Errors : ${errors} out of ${batchNumber}.`)

            if(response.errors && response.errors.length > 0) {
                errors ++;
                this.logger.error("Faulty batch detected and skipped", response.errors.join("; ") );
                // Ignore the batch
            } else {
                callback(response.data)
            }
        });

        // Build the Listening mode response
        const listeningMode : GraphListeningMode = { mode: "listening", name: "OL2", session: characteristics.session};
        const response = new SocketDataBuilder<GraphListeningMode>("Listening for graph").setData(listeningMode).build();

        // Emit ready to listen
        this.socket.emit("send_graph", response);
        this.logger.info(`Waiting for graph '${listeningMode.name}' to be received.`)
    }

    /**
     * Get a named graph by name in the database
     * @param name Name of the graph to get
     * @param callback Callback function triggered for each batch received
     */
    public getGraph(name: string, callback: Function) {
        // Build Graph Response
        const graphData: GetGraphByName = { name }
        const response = new SocketDataBuilder<GetGraphByName>("get_graph").setData(graphData).build();

        // Emit socket data
        this.socket.emit("get_graph", response, (response: SocketData<GraphCharacteristics>) => {

            if(response.errors.length > 0) throw new Error("Failed to get the graph by name."
                + JSON.stringify(response.errors))

            // Process graph response and init the graph construction on batch
            const batchSize = response.data.batch_size;
            const graphSize = response.data.graph_size;
            const batchNumber = Math.floor(graphSize / batchSize);
            this.logger.info(`Graph Size ${graphSize} will be sent ${batchNumber} in batch ( batch size: ${batchNumber}).`)

            this.enterListeningMode(response.data, callback)

        })
    }

    constructor() {
        this.socket = SocketCom.getSocket("/graph")
    }

}