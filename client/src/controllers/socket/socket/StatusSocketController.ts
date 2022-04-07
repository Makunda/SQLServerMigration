import SocketImpl from "../../../utils/socket/SocketImpl";
import SocketCom from "../../../utils/socket/SocketCom";
import SocketDataBuilder from "../../../utils/socket/data/SocketDataBuilder";

export default class StatusSocketController {

    private socket: SocketImpl;

    /**
     * Get status of the Websocket
     */
    public async getStatus() : Promise<boolean> {
        // Start listening
        return new Promise(((resolve, reject) => {
            // Listen and resolve / reject
            this.socket.on("status", ()=> {
                resolve(true);
            }).on("error", () => {
                reject(false);
            });

            // Send the message to the status socket
            this.socket.emit("get_status", new SocketDataBuilder("status").build())
        }))

    }

    constructor() {
        this.socket = SocketCom.getSocket("/status")
    }

}