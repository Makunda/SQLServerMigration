import {io, Socket} from "socket.io-client";
import {ClientToServerEvents, ServerToClientEvents} from "../../interfaces/socket/SocketListener";
import SocketData from "../../interfaces/socket/SocketData";

// Call back type
type socketCallBack = (...args: any[]) => void

/**
 * Wrapper of the Socket IO Class
 */
export default class  SocketImpl {

    private socket: Socket<any, any>;
    private namespace: string;

    /**
     * Declare an action when receiving a message
     * @param message
     * @param callback
     */
    public on(message: string, callback: socketCallBack) : SocketImpl {
        this.socket.on(message, callback)
        return this;
    }

    /**
     * Synchronized on message
     * @param message Message to wait for
     */
    public async syncOn<T>(message: string) : Promise<SocketData<T>> {
        return new Promise(((resolve, reject) => {
            // On message redirect to resolve
            this.socket.on(message, (message: any) => {
                resolve(message as SocketData<T>);
            })

            // Reject if failed
            this.socket.on("error", (message: any) => {
                reject(message as SocketData<T>);
            })
        }))
    }

    /**
     * Disconnect the socket from the endpoint
     */
    public disconnect() : SocketImpl {
        this.socket.disconnect()
        return this;
    }

    /**
     * Emit a message on the current socket
     * @param message Message to send
     * @param data Data to pass
     */
    public emit<T>(message: string, data: SocketData<T>) : SocketImpl {
        this.socket.emit(message, data)
        return this;
    }

    /**
     * Refresh the connection of the socket
     */
    public refresh() : SocketImpl {
        if(!this.socket.active) {
           this.socket.connect()
        }

        return this
    }

    /**
     * Constructor
     * @param namespace
     * @param parameters
     */
    public constructor(namespace: string, parameters: any = null) {
        if(parameters == null) parameters = {};
        this.namespace = namespace;
        this.socket = io(namespace, parameters);
    }
}