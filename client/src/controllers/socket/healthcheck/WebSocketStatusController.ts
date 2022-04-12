import SocketImpl from "../../../utils/socket/SocketImpl";
import SocketCom from "../../../utils/socket/SocketCom";
import SocketDataBuilder from "../../../utils/socket/data/SocketDataBuilder";
import Logger from "../../../utils/logging/logger";
import SocketData from "../../../interfaces/socket/SocketData";

export default class WebSocketStatusController {

    private socket: SocketImpl;
    private logger: Logger = Logger.getLogger("Web Socket Status Controller");

    /**
     * Get status of the Websocket
     */
    public async getStatus() : Promise<boolean> {

        // Start listening
        return new Promise(((resolve, reject) => {
            this.logger.info("Retrieving the status of the Web Socket connection.")

            // Listen and resolve / reject
            this.socket.on("status", ()=> {
                resolve(true);
            }).on("error", () => {
                reject(false);
            });

            // Send the message to the status socket
            this.socket.emit<any>("get_status", new SocketDataBuilder("status").build(), (response) => {
                const res = response as SocketData<boolean>;
                resolve(res.data);
            });
        }))

    }

    constructor() {
        this.socket = SocketCom.getSocket("/status")
    }

}